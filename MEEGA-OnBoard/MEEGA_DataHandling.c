#include <stdio.h>
#include <string.h>
#include <time.h>
#include "MEEGA_ErrorDetection.c"

#define NULL (void*)0
#define EOL (char)255



//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
struct DataFrame {
	//Used to chronologically order DataFrames (0 denotes an empty DataFrame)
	char sync[2];
	//Used to mark DataFrames for faulty or missing data
	char flag;
	char data[40];
} emptyDataFrame = {.sync = 0};
//Stores the data contained in one packet of the transmission protocol
struct DataPacket {
	//Used to stitch together DataFrames (= DataFrame.sync)
	char sync[2];
	//Used to denote the current program mode (2 Bits)
	char mode;
	//Used to identify payload data (3 Bits)
	char id;
	char payload[16];
	//Checksum output
	char chksm[2];
	//Cyclic Redundancy Check Output
	char crc[2];
} emptyDataPacket = {.sync = 0};
//This acts as an input/output buffer for transmissions
struct DataBuffer {
	struct DataPacket incoming[50];
	struct DataPacket outgoing[10];
	//Buffer in case multiple frames need to be processed simultanously, direction depends on program
	struct DataFrame frameStack[10];
} emptyBuffer;
//Stores all data saved in the failsafe (backup) document
struct Failsafe {
	char version;
	int dateTime;
	//path used to look up the newest savefile
	char saveFilePath[100];
	//if the experiment run of the newest savefile has been completed (Bool)
	char complete;
	//if the program has exited nominally (Bool)
	char nominalExit;
	//current operating mode of the program (test: "t"/flight: "f")
	char mode;
	//connection mode of the groundstation (unused for onboard)
	char conn;
	//language of the groundstation (unused for onboard)
	char lang;
};
//Stores the header and file-pointer of a savefile document
struct SaveFile {
	char version;
	int dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFileFrame* firstFrame;
	struct SaveFileFrame* lastFrame;
	//total amount of frames currently stored
	int frameAmount;
	//total amount of frames already written to the harddrive
	int savedAmount;
	//path to the associated file
	char saveFilePath[100];
};
//Stores one DataFrame of a savefile, as well as a pointer to the next one
struct SaveFileFrame {
	struct DataFrame data;
	struct SaveFileFrame* nextFrame;
	struct SaveFileFrame* previousFrame;
} emptySaveFileFrame = {.nextFrame = NULL};
//Stores pointers to all top-level Data Storage components of the program
struct StorageHub {
	struct SaveFile* savefile;
	struct Failsafe* failsafe;
	struct DataBuffer* buffer;
};

//WIP
int Update(struct StorageHub* storage);
//Initializes Memory and loads Data from files if possible
struct StorageHub Initialize(char path[]);

//Returns a new empty DataFrame with the specified Sync-Bytes value
static struct DataFrame CreateFrame(int sync);
//Writes data onto a DataFrame according to the ID (see FrameIdentification), returns the old value ({0} if empty)
int WriteFrame(struct DataFrame* frame, int id, int value);
//Returns stored data on a DataFrame according to the ID (see FrameIdentification)
int ReadFrame(struct DataFrame* frame, int id);
//Returns wether a DataFrame contains useful data
int FrameIsEmpty(struct DataFrame* frame);

//Converts a DataPacket into a Byte-Array to be sent via transmission
char* WritePacket(struct DataPacket outgoingData);
//Converts a transmission-input Byte-Array into a DataPacket
struct DataPacket ReadPacket(char* incomingData);

//Converts all buffered DataFrames into buffered outgoing DataPackets, returns the amount converted
int FormPackets(struct DataBuffer* buffer);
//Converts all buffered incoming DataPackets into buffered DataFrames (with {0} values if parts are missing), returns the amount converted
int FormFrames(struct DataBuffer* buffer);

//Returns the latest outgoing DataPacket and removes it from the buffer
struct DataPacket GetOutPacket(struct DataBuffer* buffer);
//Returns the latest incoming DataPacket and removes it from the buffer
struct DataPacket GetInPacket(struct DataBuffer* buffer);
//Adds a DataPacket to the incoming Buffer, returns the number of packets in the buffer
int AddInPacket(struct DataBuffer* buffer, struct DataPacket data);
//Adds a DataPacket to the outgoing Buffer, returns the number of packets in the buffer
int AddOutPacket(struct DataBuffer* buffer, struct DataPacket data);
//Returns the latest buffered DataFrame and removes it from the buffer
struct DataFrame GetBufferFrame(struct DataBuffer* buffer);
//Adds a DataFrame to the Buffer, returns the number of frames in the buffer
int AddBufferFrame(struct DataBuffer* buffer, struct DataFrame frame);

//Creates a new Failsafe structure from default values
struct Failsafe* CreateFailsafe();
//Reads the current Failsafe-file into a structure
struct Failsafe* ReadFailsafe();
//Updates the current Failsafe-file to match the structure or creates a new one if none was found,
//returns {0} if successful, {1} if it created a new file and {-1} if there was an error
int UpdateFailsafe(struct Failsafe data);

//Writes the frames added since the last save onto the harddrive, returns the number of Bytes written or {-1} if unsuccessful
int WriteSave(struct SaveFile* savefile);
//Creates a new SaveFile structure and file
struct SaveFile* CreateSave(char path[]);
//Creates a new SaveFile structure, explicitely without a corresponding file
struct SaveFile* VirtualSave();
//Reloads all frames from the harddrive into the structure, appending excess from the structure, returns the amount of frames loaded
int CheckSave(struct SaveFile* savefile);
//Reads a SaveFile-file into a Savefile-structure, creates a new one if none was found
struct SaveFile* ReadSave(char path[]);
//Returns the Frame of the SaveFile at the corresponding index, defaults to the last one
struct SaveFileFrame* GetSaveFrame(struct SaveFile* savefile, int index);
//Adds a new frame to the end of the SaveFile, returns the amount of stored frames after the operation
int AddSaveFrame(struct SaveFile* savefile, struct DataFrame* data);
//Shortcut to CreateFrame() and AddSaveFrame(), returns the amount of stored frames after the operation
int CreateSaveFrame(struct SaveFile* savefile, int sync);

//INTERNAL, Looks up values to be used by the ReadFrame() and WriteFrame() operations
static void _GetPosition_(int id, int* index, char* bit, char* length);

char VERSION = 1;
char FAILSAFENAME[] = "*\\failsafe.txt";
int PACKETLENGTH = 23;
int PACKETIDNUMBER = 5;

enum FrameIdentifier {
	AmbientPressure, CompareTemperature, HHAmbientPressure, HHCompareTemperature
};

struct StorageHub Initialize(char path[])
{
	struct StorageHub new = {NULL, NULL, NULL};
	struct FailSafe* failsafe = ReadFailsafe();
	if (failsafe == NULL) failsafe = CreateFailsafe();
	new.failsafe = failsafe;
	struct SaveFile* savefile;
	int readExisting = !new.failsafe->nominalExit && new.failsafe->saveFilePath[0] != "";
	if (readExisting) savefile = ReadSave(new.failsafe->saveFilePath);
	else savefile = CreateSave(path);
	if (savefile == NULL) {
		savefile = VirtualSave();
		strcpy(new.failsafe->saveFilePath, "");
	}
	else if (!readExisting) strcpy(new.failsafe->saveFilePath, path);
	new.savefile = savefile;
	struct DataBuffer* buffer = (struct DataBuffer*)malloc(sizeof(struct DataBuffer));
	*buffer = emptyBuffer;
	new.buffer = buffer;
	return new;
}

static struct DataFrame CreateFrame(char sync[2]) {
	if (sync <= 0) return emptyDataFrame;
	struct DataFrame temp = emptyDataFrame;
	temp.sync[0] = sync[0];
	temp.sync[1] = sync[1];
	return temp;
}

static void _GetPosition_(int id, int* index, char* bit, char* length)
{
	switch (id) {
	case AmbientPressure: *index = 0, *length = 2;
	case HHAmbientPressure: *index = 32, *bit = 8, *length = 1;
	case CompareTemperature: *index = 2, *length = 3;
	case HHCompareTemperature: *index = 32, *bit = 7, *length = 1;
	}
	return;
}

int WriteFrame(struct DataFrame* frame, int id, int value)
{
	char former[4] = {0,0,0,0};
	char value32[4] = value;
	int index = 0;
	char bit = 0;
	char length = 0;
	_GetPosition_(id, &index, &bit, &length);
	if (bit == 0) {
		for (int i = 0; i < length; i++) {
			former[i] = frame->data[index + i];
			frame->data[index + i] = value32[i];
		}
	}
	else {
		former[0] = frame->data[index];
		former[0] >>= bit - length;
		former[0] %= 1 << length;
		frame->data[index] -= former[0] << bit - length;
		frame->data[index] += value << bit - length;
	}
	return (int)former;
}

int ReadFrame(struct DataFrame* frame, int id)
{
	int value = 0;
	int index = 0;
	char bit = 0;
	char length = 0;
	_GetPosition_(id, &index, &bit, &length);
	if (bit == 0) {
		for (int i = 1; i <= length; i++) {
			value += (frame->data[index + length - i]) << (i * sizeof(char));
		}
	}
	else {
		value = frame->data[index];
		value >>= bit - length;
		value %= 1 << length;
	}
	return value;
}

int FrameIsEmpty(struct DataFrame* frame) {
	return frame->sync == 0;
}

struct DataPacket GetOutPacket(struct DataBuffer* buffer)
{
	struct DataPacket temp = emptyDataPacket;
	for (int i = length(buffer->outgoing); i > 0; i--) {
		temp = buffer->outgoing[i - 1];
		if (temp.sync != 0) {
			buffer->outgoing[i - 1] = emptyDataPacket;
		}
	}
	return temp;
}

struct DataPacket GetInPacket(struct DataBuffer* buffer)
{
	struct DataPacket temp = emptyDataPacket;
	for (int i = length(buffer->incoming); i > 0; i--) {
		temp = buffer->incoming[i - 1];
		if (temp.sync != 0) {
			buffer->incoming[i - 1] = emptyDataPacket;
		}
	}
	return temp;
}

struct DataFrame GetBufferFrame(struct DataBuffer* buffer)
{
	struct DataFrame temp = emptyDataFrame;
	for (int i = length(buffer->frameStack); i > 0; i--) {
		temp = buffer->frameStack[i - 1];
		if (temp.sync != 0) {
			buffer->frameStack[i - 1] = emptyDataFrame;
		}
	}
	return temp;
}

int AddBufferFrame(struct DataBuffer* buffer, struct DataFrame frame)
{
	int number = 0;
	for (; number <= length(buffer->frameStack); number++) {
		if (buffer->frameStack[number].sync == 0) {
			buffer->frameStack[number] = frame;
			break;
		}
	}
	return number + 1;
}

int AddInPacket(struct DataBuffer* buffer, struct DataPacket data)
{
	int number = 0;
	for (; number <= length(buffer->incoming); number++) {
		if (buffer->incoming[number].sync == 0) {
			buffer->incoming[number] = data;
			break;
		}
	}
	return number + 1;
}

int AddOutPacket(struct DataBuffer* buffer, struct DataPacket data)
{
	int number = 0;
	for (; number <= length(buffer->outgoing); number++) {
		if (buffer->outgoing[number].sync == 0) {
			buffer->outgoing[number] = data;
			break;
		}
	}
	return number + 1;
}

struct Failsafe* CreateFailsafe() 
{
	struct Failsafe* new = (struct Failsafe*) malloc(sizeof(struct Failsafe));
	new->complete = 0;
	new->conn = "a";
	new->lang = "e";
	new->dateTime = time(NULL);
	new->nominalExit = 0;
	new->saveFilePath[0] = "";
	strcpy(new->version, VERSION);
	new->mode = "f";
	new->conn = "";
	new->lang = "";
	FILE* file = fopen(FAILSAFENAME, "w");
	if (file != NULL) {
		fprintf(file, "Version: %i;\n", VERSION);
		fprintf(file, "Datetime: %i;\n\n", new->dateTime);
		fprintf(file, "Savefile: %s;\n", new->saveFilePath);
		fprintf(file, "Complete: %c;\n\n", (new->complete) ? 'y' : 'n');
		fprintf(file, "Regular Exit: No;\n\n");
		fprintf(file, "Mode: %c;\n", new->mode);
		fprintf(file, "Connection: %c;\n", new->conn);
		fprintf(file, "Language: %c;", new->lang);
		fclose(file);
	}
	else {
		free(new);
		return NULL;
	}
	return new;
}

struct SaveFile* VirtualSave()
{
	struct SaveFile* new = (struct Failsafe*)malloc(sizeof(struct SaveFile));
	new->dateTime = time(NULL);
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = -1;
	new->saveFilePath[0] = "";
	new->version = VERSION;
	return new;
}

struct SaveFileFrame* GetSaveFrame(struct SaveFile* savefile, int index)
{
	if (index >= savefile->frameAmount)	return NULL;
	if (index < 0) return savefile->lastFrame;
	struct SaveFileFrame* frame = savefile->firstFrame;
	for (int i = 0; i < index; i++) {
		if (frame == NULL) return NULL;
		if (frame->nextFrame == NULL) return frame;
		frame = frame->nextFrame;
	}
	return frame;
}

int AddSaveFrame(struct SaveFile* savefile, struct DataFrame* data)
{
	struct SaveFileFrame* newframe = (struct SaveFileFrame*)malloc(sizeof(struct SaveFileFrame));
	newframe->data = *data;
	newframe->nextFrame = NULL;
	if (savefile->firstFrame == NULL) {
		savefile->firstFrame = newframe;
		savefile->lastFrame = newframe;
		savefile->frameAmount = 1;
		return 1;
	}
	savefile->lastFrame->nextFrame = newframe;
	savefile->lastFrame = newframe;
	savefile->frameAmount++;
	return savefile->frameAmount;
}

int CreateSaveFrame(struct SaveFile* savefile, int sync)
{
	struct DataFrame data = CreateFrame(sync);
	return AddSaveFrame(savefile, &data);
}

struct SaveFile* CreateSave(char path[]) 
{
	struct SaveFile* new = (struct Failsafe*)malloc(sizeof(struct SaveFile));
	int tempDateTime = time(NULL);
	FILE* file = fopen(path, "wb");
	if (file != NULL) {
		fprintf(file, VERSION);
		fwrite(&tempDateTime, 4, 1, file);
		fprintf(file, EOL);
		fclose(file);
	}
	else {
		free(new);
		return NULL;
	}
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = 0;
	strcpy(new->saveFilePath, path);
	new->version = VERSION;
	return new;
}
