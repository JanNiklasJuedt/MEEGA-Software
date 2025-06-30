#include <stdio.h>
#include <string.h>
#include "MEEGA_ErrorDetection.c"

#define NULL (void*)0

//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
struct DataFrame {
	//Used to chronologically order DataFrames, Always > 0 (0 denotes an empty DataFrame)
	int sync;
	//Used to mark DataFrames for faulty or missing data
	int flag;
	int sensors[8];
	int householding[2];
} emptyDataFrame = {.sync = 0};
//Stores the data contained in one packet of the transmission protocol (as "int" for simplicity, actual transmission uses bytes) 
struct DataPacket {
	//Used to stitch together DataFrames (= DataFrame.sync)
	int sync;
	//Used to denote the current program mode
	int mode;
	//Used to denote payload data
	int id;
	int payload[4];
	int chksm;
	int crc;
} emptyDataPacket = {.sync = 0};
//This acts as an input/output buffer for transmissions (use only one!)
struct DataBuffer {
	struct DataPacket incoming[50];
	struct DataPacket outgoing[10];
	//buffer in case multiple frames need to be processed simultanusly, direction depends on program
	struct DataFrame frameStack[10];
};
//Stores all data saved in the failsafe/backup document
struct Failsafe {
	char version[4];
	int dateTime;
	//path used to lookup the newest savefile
	char saveFilePath[100];
	//if the experiment run of the newest savefile has been completed
	char complete;
	//if the program has exited nominally
	char nominalExit;
	//current operating mode of the program (test/flight)
	char mode;
	//connection mode of the groundstation (unused for onboard)
	char conn;
	//language of the groundstation (unused for onboard)
	char lang;
};
//Stores the header and file-pointer of a savefile document
struct SaveFile {
	char version[4];
	int dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFileFrame* firstFrame;
	struct SaveFileFrame* lastFrame;
	//total amount of frames currently stored
	int frameAmount;
	//total amount of frames already written to the harddrive
	int savedAmount;
	FILE* file;
	char saveFilePath[100];
};
//Stores one DataFrame of a savefile, as well as a pointer to the next one
struct SaveFileFrame {
	struct DataFrame payload;
	struct SaveFileFrame* nextFrame;
} emptySaveFileFrame = {.nextFrame = (void*)0};

//Returns a new empty DataFrame with the specified Sync-Bytes value
struct DataFrame CreateFrame(int sync);
//Writes data onto a DataFrame according to the identification-string
int WriteFrame(struct DataFrame* frame, char id[], int value);
//Returns stored data on a DataFrame according to the identification-string
int ReadFrame(struct DataFrame* frame, char id[]);
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

//Writes the frames added since the last save onto the harddrive,
//returns the number of Bytes written or {-1} if unsuccessful
int WriteSave(struct SaveFile* savefile);
//Creates a new SaveFile structure and file
struct SaveFile* CreateSave(char path[]);
//Creates a new SaveFile structure, explicitely without a corresponding file
struct SaveFile* VirtualSave();
//Reloads all frames from the harddrive into the structure, appending excess from the structure, returns the amount of frames checked
int CheckSave(struct SaveFile* savefile);
//Reads a SaveFile-file into a structure
struct SaveFile* ReadSave(char path[]);
//Returns the Frame of the SaveFile at the corresponding index, defaults to the last one
struct SaveFileFrame* GetSaveFrame(struct SaveFile* savefile, int index);
//Adds a new frame to the end of the SaveFile
int AddSaveFrame(struct SaveFile* savefile, struct DataFrame* data);

char VERSION[] = "0.1";
char FAILSAFENAME[] = "\meega.failsafe";
int PACKETLENGTH = 23;
int PACKETIDNUMBER = 5;

struct DataFrame CreateFrame(int sync) {
	if (sync <= 0) return emptyDataFrame;
	struct DataFrame temp = emptyDataFrame;
	temp.sync = sync;
	return temp;
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
struct Failsafe* CreateFailsafe() {
	struct Failsafe* new = (struct Failsafe*) malloc(sizeof(struct Failsafe));
	new->complete = 0;
	new->conn = "a";
	new->lang = "e";
	new->dateTime = 0;
	new->nominalExit = 0;
	strcpy(new->saveFilePath[0], FAILSAFENAME);
	new->version[0] = "";
	new->mode = "f";
	return new;
}

struct SaveFile* VirtualSave()
{
	struct SaveFile* new = (struct Failsafe*)malloc(sizeof(struct SaveFile));
	new->dateTime = 0;
	new->file = NULL;
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = -1;
	new->saveFilePath[0] = "";
	strcpy(new->version[0], VERSION);
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
	newframe->payload = *data;
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
struct SaveFile* CreateSave(char path[]) {
	struct SaveFile* new = (struct Failsafe*)malloc(sizeof(struct SaveFile));
	new->dateTime = 0;
	new->file = fopen(path, "w");
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = 0;
	strcpy(new->saveFilePath, path);
	strcpy(new->version[0], VERSION);
	return new;
}
