#include <stdio.h>
#include "MEEGA_ErrorDetection.c"

//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
struct DataFrame {
	int sync;
	int flag;
	int sensors[8];
	int householding[2];
};
//Stores the data contained in one packet of the transmission protocol (as "int" for simplicity, actual transmission uses bytes) 
struct DataPacket {
	int sync;
	int mode;
	int id;
	int payload[4];
	int chksm;
	int crc;
};
//This acts as an input/output buffer for transmissions (create only one!)
struct DataBuffer {
	struct DataPacket incoming[50];
	struct DataPacket outgoing[10];
	//buffer in case multiple frames need to be processed simultanusly, direction depends on program
	struct DataFrame frameStack[10];
};
//Stores all data saved in the failsafe/backup document
struct Failsafe {
	int version;
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
	int version;
	int dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFileFrame* firstFrame;
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
};

//Converts a DataPacket into a Byte-Array to be sent via transmission
char* WritePacket(struct DataPacket outgoingData);
//Converts a transmission-input Byte-Array into a DataPacket
struct DataPacket ReadPacket(char* incomingData);

//Converts all buffered DataFrames into buffered outgoing DataPackets, returns the amount converted
int FormPackets(struct DataBuffer* buffer);
//Converts all buffered incoming DataPackets into buffered DataFrames (with 0 values if parts are missing), returns the amount converted
int FormFrames(struct DataBuffer* buffer);

//Returns the outgoing DataPacket at an optional index, else it returns the last one
struct DataPacket* GetPacket(struct DataBuffer* buffer, int index);
//Adds a DataPacket to the incoming Buffer, returns the index it was added at
int AddPacket(struct DataBuffer* buffer, struct DataPacket data);
//Returns the buffered DataFrame at an optional index, else it returns the last one
struct DataFrame* GetFrame(struct DataBuffer* buffer, int index);
//Adds a DataFrame to the Buffer, returns the index it was added at
int AddFrame(struct DataBuffer* buffer, struct DataFrame frame);

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
int PACKETLENGTH = 23;
int PACKETNUMBER = 5;