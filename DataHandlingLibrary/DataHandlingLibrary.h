//Header File of DataHandlingLibrary
#include <stdint.h>
#include <time.h>

#ifndef DATAHANDLINGLIBRARY_H
#define DATAHANDLINGLIBRARY_H

#ifdef DATAHANDLINGLIBRARY_EXPORTS
#define DATAHANDLINGLIBRARY_API __declspec(dllexport)
#else
#define DATAHANDLINGLIBRARY_API __declspec(dllimport)
#endif // DATAHANDLINGLIBRARY_EXPORTS

#define DATAHANDLINGLIBRARY_CONSTANT __declspec(dllexport)

#ifndef NULL
#define NULL (void*)0
#endif //NULL

#define EOL (char)255
#define IDBITS 3
#define MODEBITS 3
#define PACKETLENGTH PAYLOADLENGTH + CHKSMLENGTH * 2 + 3
#define PATHLENGTH 100
#define BUFFERLENGTH 10
#define DATALENGTH 40
#define PAYLOADLENGTH 16
#define CHKSMLENGTH 2

DATAHANDLINGLIBRARY_CONSTANT const int PathLength = PATHLENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int BufferLength = BUFFERLENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int DataLength = DATALENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int PayloadLength = PAYLOADLENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int ChksmLength = CHKSMLENGTH;

DATAHANDLINGLIBRARY_CONSTANT const int VERSION = 1;
DATAHANDLINGLIBRARY_CONSTANT const char FAILSAFENAME[] = "*\\failsafe.txt";

enum DATAHANDLINGLIBRARY_API FrameIdentifier{
	Ambient_Pressure, Compare_Temperature, Tank_Pressure, Tank_Temperature, Chamber_Pressure, Chamber_Temperature,
	Nozzle_Pressure_1, Nozzle_Temperature_1, Nozzle_Pressure_2, Nozzle_Temperature_2, Nozzle_Pressure_3, Nozzle_Temperature_3,
	Ambient_Pressure_Health, Compare_Temperature_Health, Tank_Pressure_Health, Tank_Temperature_Health, Chamber_Pressure_Health, Chamber_Temperature_Health,
	Nozzle_Pressure_1_Health, Nozzle_Temperature_1_Health, Nozzle_Pressure_2_Health, Nozzle_Temperature_2_Health, Nozzle_Pressure_3_Health, Nozzle_Temperature_3_Health,
	Nozzle_Cover, Nozzle_Servo, Reservoir_Valve, Camera, LEDs, Sensorboard_1, Sensorboard_2, Mainboard, System_Time, Lift_Off, Start_Experiment, End_Experiment, Mode
}; //Camera = deprecated

enum DATAHANDLINGLIBRARY_API TCIdentifier {
	Mode, Valve_Delay, Servo_Delay, EoE_Delay, Power_Off_Delay, Nozzle_On_Delay, Dry_Run, LED_Control, Servo_Control, Valve_Control, Camera_Control, Test_Abort, Test_Run
}; //Camera_Control = deprecated

enum DATAHANDLINGLIBRARY_API Flags {
	Source = 0, OK = 1, Partial = 2, Biterror = 3, Overwrite = 4, TeleCommand = 10, Idle = 20, Experiment = 30, Full = 100, Sensor = 200
};

//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
typedef struct DATAHANDLINGLIBRARY_API DataFrame {
	//Used to chronologically order DataFrames (0 denotes an empty DataFrame)
	uint16_t sync;
	//Used to mark DataFrames for faulty or missing data
	unsigned char flag;
	unsigned char data[DATALENGTH];
} DataFrame;

//Stores the data contained in one packet of the transmission protocol
typedef struct DATAHANDLINGLIBRARY_API DataPacket {
	//Used to stitch together DataFrames (= DataFrame.sync)
	uint16_t sync;
	//Used to denote the current program mode (3 Bits)
	unsigned char mode;
	//Used to identify payload data (3 Bits)
	unsigned char id;
	unsigned char payload[PAYLOADLENGTH];
	//Checksum output
	unsigned char chksm[CHKSMLENGTH];
	//Cyclic Redundancy Check Output
	unsigned char crc[CHKSMLENGTH];
} DataPacket;

//This acts as an input/output buffer for transmissions
typedef struct DATAHANDLINGLIBRARY_API DataBuffer {
	struct DataPacket incoming[BUFFERLENGTH];
	struct DataPacket outgoing[BUFFERLENGTH];
	//Buffer in case multiple frames need to be processed simultanously, direction depends on program
	struct DataFrame frameStack[BUFFERLENGTH];
	//Buffer for TeleCommand frames, direction is inverse to frameStack
	struct DataFrame TCStack[BUFFERLENGTH];
} DataBuffer;

//Stores all persistent data needed for a (spontanious) program reboot
typedef struct DATAHANDLINGLIBRARY_API FailSafe {
	unsigned char version;
	time_t dateTime;
	//path used to look up the newest savefile
	char saveFilePath[PATHLENGTH];
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
} FailSafe;

//Stores one DataFrame of a savefile, as well as a pointer to the next one
typedef struct DATAHANDLINGLIBRARY_API SaveFileFrame {
	struct DataFrame data;
	struct SaveFileFrame* nextFrame;
	struct SaveFileFrame* previousFrame;
} SaveFileFrame;

//Stores all data collected/received during the mission
typedef struct DATAHANDLINGLIBRARY_API SaveFile {
	unsigned char version;
	time_t dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFileFrame* firstFrame;
	struct SaveFileFrame* lastFrame;
	//total amount of frames currently stored
	int frameAmount;
	//total amount of frames already written to the harddrive
	int savedAmount;
	//pointer towards a collection of all newest TeleCommands
	struct DataFrame* currentTC;
	//path to the associated file
	char saveFilePath[PATHLENGTH];
} SaveFile;

//Stores pointers to all top-level Data Storage components of the program
typedef struct DATAHANDLINGLIBRARY_API StorageHub {
	struct SaveFile* saveFile;
	struct FailSafe* failSafe;
	struct DataBuffer* buffer;
} StorageHub;

DATAHANDLINGLIBRARY_API int CalculateChecksum(char data[]);

DATAHANDLINGLIBRARY_API int CalculateCRC(char data[]);

//WIP
DATAHANDLINGLIBRARY_API int Update(StorageHub* storage);

//Initializes Memory and loads Data from files if possible
DATAHANDLINGLIBRARY_API StorageHub Initialize(const char path[]);

//Returns a new empty DataFrame with the specified Sync-Bytes value
DATAHANDLINGLIBRARY_API DataFrame CreateFrame(uint16_t sync);

//Returns a new empty TeleCommand-DataFrame with the specified Sync-Bytes value
DATAHANDLINGLIBRARY_API DataFrame CreateTC(uint16_t sync);

//Writes data onto a DataFrame according to the ID (enum FrameIdentifier), returns the old value ({0} if empty)
DATAHANDLINGLIBRARY_API int WriteFrame(DataFrame* frame, int id, int value);

//Writes data onto a TeleCommand-DataFrame according to the ID (enum TCIdentifier), returns the old value ({0} if empty)
DATAHANDLINGLIBRARY_API int WriteTC(DataFrame* frame, int id, int value);

//Returns stored data on a DataFrame according to the ID (enum FrameIdentifier)
DATAHANDLINGLIBRARY_API int ReadFrame(DataFrame* frame, int id);

//Returns stored data on a TeleCommand-DataFrame according to the ID (enum TCIdentifier)
DATAHANDLINGLIBRARY_API int ReadTC(DataFrame* frame, int id);

//Returns wether a DataFrame contains useful data
DATAHANDLINGLIBRARY_API int FrameIsEmpty(DataFrame* frame);

//Returns wether a DataFrame is a TeleCommand-DataFrame
DATAHANDLINGLIBRARY_API int FrameIsTC(DataFrame* frame);

//Converts a DataPacket into a Byte-Array of size {PACKETLENGTH} to be sent via transmission
DATAHANDLINGLIBRARY_API unsigned char* WritePacket(DataPacket packet);

//Converts a transmission-input Byte-Array into a DataPacket struct
DATAHANDLINGLIBRARY_API DataPacket ReadPacket(unsigned char* bytes);

//Converts all buffered DataFrames into buffered outgoing DataPackets, returns the amount converted
DATAHANDLINGLIBRARY_API int FormPackets(DataBuffer* buffer);

//Converts all buffered incoming DataPackets into buffered DataFrames (with {0} values if parts are missing), returns the amount converted
DATAHANDLINGLIBRARY_API int FormFrames(DataBuffer* buffer);

//Returns the latest outgoing DataPacket and removes it from the buffer
DATAHANDLINGLIBRARY_API DataPacket GetOutPacket(DataBuffer* buffer);

//Returns the latest incoming DataPacket and removes it from the buffer
DATAHANDLINGLIBRARY_API DataPacket GetInPacket(DataBuffer* buffer);

//Adds a DataPacket to the incoming Buffer, returns the number of packets in the buffer
DATAHANDLINGLIBRARY_API int AddInPacket(DataBuffer* buffer, DataPacket packet);

//Adds a DataPacket to the outgoing Buffer, returns the number of packets in the buffer
DATAHANDLINGLIBRARY_API int AddOutPacket(DataBuffer* buffer, DataPacket packet);

//Returns the latest buffered DataFrame and removes it from the buffer
DATAHANDLINGLIBRARY_API DataFrame GetBufferFrame(DataBuffer* buffer);

//Adds a DataFrame to the Buffer, returns the number of frames in the buffer
DATAHANDLINGLIBRARY_API int AddBufferFrame(DataBuffer* buffer, DataFrame frame);

//Returns the latest buffered TeleCommand-DataFrame and removes it from the buffer
DATAHANDLINGLIBRARY_API DataFrame GetBufferTC(DataBuffer* buffer);

//Adds a TeleCommand-DataFrame to the Buffer, returns the number of frames in the buffer
DATAHANDLINGLIBRARY_API int AddBufferTC(DataBuffer* buffer, DataFrame frame);

//Initializes new Buffer-Arrays
DATAHANDLINGLIBRARY_API DataBuffer* CreateBuffer();

//Creates a new Failsafe structure from default values
DATAHANDLINGLIBRARY_API FailSafe* CreateFailSafe();

//Reads the current Failsafe-file into a structure
DATAHANDLINGLIBRARY_API FailSafe* ReadFailSafe();

//Updates the current Failsafe-file to match the structure or creates a new one if none was found,
//returns {0} if successful, {1} if it created a new file and {-1} if there was an error
DATAHANDLINGLIBRARY_API int UpdateFailSafe(FailSafe* failsafe);

//Writes the frames added since the last save onto the harddrive, returns the number of Bytes written or {-1} if unsuccessful
DATAHANDLINGLIBRARY_API int WriteSave(SaveFile* savefile);

//Creates a new SaveFile structure and file
DATAHANDLINGLIBRARY_API SaveFile* CreateSave(const char path[]);

//Creates a new SaveFile structure, explicitely without a corresponding file
DATAHANDLINGLIBRARY_API SaveFile* VirtualSave();

//Reloads all frames from the harddrive into the structure, appending excess from the structure, returns the amount of frames loaded
DATAHANDLINGLIBRARY_API int CheckSave(SaveFile* savefile);

//Reads a SaveFile-file into a Savefile-structure, creates a new one if none was found
DATAHANDLINGLIBRARY_API SaveFile* ReadSave(const char path[]);

//Returns the Frame of the SaveFile at the corresponding index, defaults to the last one
DATAHANDLINGLIBRARY_API SaveFileFrame* GetSaveFrame(SaveFile* savefile, int index);

//Updates {currentTC} to represent all saved TeleCommand-DataFrames, returns the updated {currentTC}
DATAHANDLINGLIBRARY_API DataFrame* UpdateTC(SaveFile* savefile);

//Adds a new frame to the end of the SaveFile, returns a pointer to the newly created Frame
DATAHANDLINGLIBRARY_API SaveFileFrame* AddSaveFrame(SaveFile* savefile, DataFrame data);

//Shortcut to CreateFrame() and AddSaveFrame(), returns a pointer to the newly created Frame
DATAHANDLINGLIBRARY_API SaveFileFrame* CreateSaveFrame(SaveFile* savefile, uint16_t sync);

#endif //DATAHANDLINGLIBRARY_H
