#include <stdio.h>
#include "MEEGA_ErrorDetection.c"

struct DataFrame {
	int flag;
	int sensors[8];
	int householding[2];
};
struct DataPacket {
	int sync;
	int mode;
	int id;
	int payload[4];
	int chksm;
	int crc;
};
struct DataBuffer {
	struct DataPacket incoming[50];
	struct DataPacket outgoing[10];
	struct DataFrame frameStack[10];
};
struct Failsafe {
	int version;
	int dateTime;
	char saveFilePath[100];
	char complete;
	char nominalExit;
	char mode;
	char conn;
	char lang;
};
struct SaveFile {
	int version;
	int dateTime;
	struct SaveFileFrame* firstFrame;
	int frameAmount;
	FILE* file;
	char saveFilePath[100];
};
struct SaveFileFrame {
	int sync;
	struct DataFrame payload;
	struct SaveFileFrame* nextFrame;
};

char* WritePacket(struct DataPacket outgoingData);
struct DataPacket ReadPacket(char* incomingData);
int FormPackets(struct DataBuffer* buffer);
int FormFrames(struct DataBuffer* buffer);
struct DataPacket* GetPacket(struct DataBuffer* buffer, int index);
int AddPacket(struct DataBuffer* buffer, struct DataPacket data);
struct DataFrame* GetFrame(struct DataBuffer* buffer, int index);
int AddFrame(struct DataBuffer* buffer, struct DataFrame frame);

struct Failsafe* CreateFailsafe(char path[]);
struct Failsafe* ReadFailsafe(char path[]);

int WriteSave(struct SaveFile* savefile);
struct SaveFile* CreateSave(char path[]);
struct SaveFile* VirtualSave();
int CheckSave(struct SaveFile* savefile);
struct SaveFile* ReadSave(struct SaveFile* savefile);
struct SaveFile* ReadSave(char path[]);
struct SaveFileFrame* GetFrame(struct SaveFile* savefile, int index);
int AddFrame(struct SaveFile* savefile, struct DataFrame* data);

char VERSION[] = "0.1";
int PACKETLENGTH = 23;
int PACKETNUMBER = 5;