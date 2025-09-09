//Header File of DataHandlingLibrary
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>

#ifndef DATAHANDLINGLIBRARY_H
#define DATAHANDLINGLIBRARY_H

#define WINDOWS_OS 0
#define LINUX_OS 1
#define MAC_OS 2
#define ANDROID_OS 3

#define NONE -1

#define TERMINAL 0
#define LOGFILE 1

#define LINEAR 0
#define QUADRATIC 1
#define CUBIC 2

//DataHandling Settings
#define DATAHANDLINGLIBRARY_OS WINDOWS_OS
#define CALIBRATION_METHOD LINEAR
#define DEBUG_OUTPUT TERMINAL

const int OS = DATAHANDLINGLIBRARY_OS;
const int METHOD = CALIBRATION_METHOD;
const int OUTPUT = DEBUG_OUTPUT;
//-

#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)

#include <windows.h>

#ifdef DATAHANDLINGLIBRARY_EXPORTS
#define DATAHANDLINGLIBRARY_API __declspec(dllexport)
#else
#define DATAHANDLINGLIBRARY_API __declspec(dllimport)
#endif // DATAHANDLINGLIBRARY_EXPORTS

#define DATAHANDLINGLIBRARY_CONSTANT __declspec(dllexport)
#define DEFAULTCOMPATH "COM1"

#elif (DATAHANDLINGLIBRARY_OS == LINUX)

#include <termios.h>
#include <fcntl.h>
#include <unistd.h>

#define DATAHANDLINGLIBRARY_CONSTANT
#define DATAHANDLINGLIBRARY_API
#define DEFAULTCOMPATH "/dev/ttyUART1"

#endif // DATAHANDLINGLIBRARY_OS


#ifndef NULL
#define NULL (void*)0
#endif // NULL

//DataHandling Constants
#define PACKET_LENGTH (PAYLOAD_LENGTH + CHKSM_LENGTH * 2 + 4)

#define PATH_LENGTH 100 //Chars
#define BUFFER_LENGTH 10 //DataPackets / DataFrames

#define DATA_LENGTH 40 //Bytes
#define PAYLOAD_LENGTH 16 //Bytes
#define CHKSM_LENGTH 2 //Bytes

#define SENSOR_AMOUNT Nozzle_Temperature_3 + 1
#define TELEMETRY_AMOUNT Mode + 1
#define TELECOMMAND_AMOUNT Test_Run + 1
#define CALIBRATION_POINTS 3

#define BASE_RES 10 //Bits
#define HIGH_RES 20 //Bits
#define DELAY_LEN 16 //Bits

#define BAUD_RATE 9600

DATAHANDLINGLIBRARY_CONSTANT const int PathLength = PATH_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int BufferLength = BUFFER_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int DataLength = DATA_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int PayloadLength = PAYLOAD_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int ChksmLength = CHKSM_LENGTH;

DATAHANDLINGLIBRARY_CONSTANT const float FAILSAFE_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char FAILSAFE_NAME[] = "MEEGA_FailSafe.txt";

DATAHANDLINGLIBRARY_CONSTANT const float CALIBRATION_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char CALIBRATION_NAME[] = "MEEGA_Calibration.txt";

DATAHANDLINGLIBRARY_CONSTANT const float SAVEFILE_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char SAVEFILE_NAME[] = "MEEGA_SaveFile.meega";

DATAHANDLINGLIBRARY_CONSTANT const float VERSION = 0.5f;
DATAHANDLINGLIBRARY_CONSTANT const char DEBUGLOG_NAME[] = "MEEGA_DataHandlingLog.txt";
//-

enum DATAHANDLINGLIBRARY_API TMID{
	//Sensors:
	Ambient_Pressure, Compare_Temperature, Tank_Pressure, Tank_Temperature, Chamber_Pressure, Chamber_Temperature,
	Nozzle_Pressure_1, Nozzle_Temperature_1, Nozzle_Pressure_2, Nozzle_Temperature_2, Nozzle_Pressure_3, Nozzle_Temperature_3,
	//Householding Sensors:
	Ambient_Pressure_Health, Compare_Temperature_Health, Tank_Pressure_Health, Tank_Temperature_Health, Chamber_Pressure_Health, Chamber_Temperature_Health,
	Nozzle_Pressure_1_Health, Nozzle_Temperature_1_Health, Nozzle_Pressure_2_Health, Nozzle_Temperature_2_Health, Nozzle_Pressure_3_Health, Nozzle_Temperature_3_Health,
	//Householding Misc:
	Nozzle_Cover, Nozzle_Servo, Reservoir_Valve, Camera, LEDs, Sensorboard_1, Sensorboard_2, Mainboard, System_Time, Lift_Off, Start_Experiment, End_Experiment, Mode
};

enum DATAHANDLINGLIBRARY_API TCID {
	Mode_Change, Valve_Delay, Servo_Delay, EoE_Delay, Power_Off_Delay, Nozzle_On_Delay, Dry_Run, LED_Control, Servo_Control, Valve_Control, Camera_Control, Test_Abort, Test_Run
};

enum DATAHANDLINGLIBRARY_API Flag {
	Source = 0, OK = 1, Partial = 2, Biterror = 3, Overwrite = 4, TeleCommand = 10, Idle = 20, Experiment = 30, Full = 100, Sensor = 200
};

//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
typedef struct DATAHANDLINGLIBRARY_API DataFrame {
	//Used to chronologically order DataFrames (0 denotes an empty DataFrame)
	uint16_t sync;
	//Used to mark DataFrames for faulty or missing data
	unsigned char flag;
	unsigned char data[DATA_LENGTH];
	unsigned char chksm[CHKSM_LENGTH];
} DataFrame;

//Stores the data contained in one packet of the transmission protocol
typedef struct DATAHANDLINGLIBRARY_API DataPacket {
	//Used to stitch together DataFrames (= DataFrame.sync)
	uint16_t sync;
	//Used to denote the current program mode
	unsigned char mode;
	//Used to identify payload data
	unsigned char id;
	unsigned char payload[PAYLOAD_LENGTH];
	//Checksum output
	unsigned char chksm[CHKSM_LENGTH];
	//Cyclic Redundancy Check Output
	unsigned char crc[CHKSM_LENGTH];
} DataPacket;

//This acts as an input/output buffer for transmissions
typedef struct DataBuffer {
	unsigned char* incomingPos;
	unsigned char incomingBytes;
	unsigned char* outgoingPos;
	unsigned char outgoingBytes;
	struct DataPacket inPackets[BUFFER_LENGTH];
	struct DataPacket outPackets[BUFFER_LENGTH];
	struct DataFrame inFrames[BUFFER_LENGTH];
	struct DataFrame outFrames[BUFFER_LENGTH];
} DataBuffer;

//Stores all persistent data needed for a (spontanious) program reboot
typedef struct FailSafe {
	float version;
	time_t dateTime;
	//path used to look up the newest savefile
	char saveFilePath[PATH_LENGTH];
	//if the experiment run of the newest savefile has been completed (Bool)
	char complete;
	//if the program has exited nominally (Bool)
	char nominalExit;
	//current operating mode of the program (test: "t" / flight: "f")
	char mode;
	//connection mode of the groundstation (unused for onboard)
	char conn;
	//language of the groundstation (unused for onboard)
	char lang;
	//identifier of the used input/output path
	char comPath[PATH_LENGTH];
	//path used to look up calibration data
	char calPath[PATH_LENGTH];
	char changed;
} FailSafe;

//Stores one DataFrame of a savefile, as well as a pointer to the next one
typedef struct DATAHANDLINGLIBRARY_API SaveFileFrame {
	struct DataFrame data;
	struct SaveFileFrame* nextFrame;
	struct SaveFileFrame* previousFrame;
} SaveFileFrame;

//Stores all data collected/received during the mission
typedef struct SaveFile {
	float version;
	time_t dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFileFrame* firstFrame;
	struct SaveFileFrame* lastFrame;
	//total amount of frames added to the SaveFile
	int frameAmount;
	//total amount of frames already written to the harddrive
	int savedAmount;
	//amount of frames currently loaded into memory
	int loadedAmount;
	//amount of frames unloaded from memory
	int unloadedAmount;
	//pointer towards a collection of all newest TeleCommands
	struct DataFrame currentTC;
	//path to the associated file
	char saveFilePath[PATH_LENGTH];
} SaveFile;

typedef struct PortHandler {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	DCB options;
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	struct termios options;
#endif
	HANDLE comHandle;
	char comPath[PATH_LENGTH];
} PortHandler;

//Stores one calibration point consisting of the digital ADC output and the corresponding analog calibration measurement
typedef struct DATAHANDLINGLIBRARY_API CalibrationPoint {
	int digital;
	float analog;
	char valid;
} CalibrationPoint;

//Stores all data neccessary for sensor value mapping
typedef struct SensorCalibration {
	float version;
	time_t dateTime;
	char sorted;
	char changed;
	struct CalibrationPoint points[SENSOR_AMOUNT][CALIBRATION_POINTS];
	char calibrationFilePath[PATH_LENGTH];
} SensorCalibration;

typedef struct FrameLookUpTable {
	int telemetry_Pos_Len[TELEMETRY_AMOUNT][2];
	int telecommand_Pos_Len[TELECOMMAND_AMOUNT][2];
} FrameLookUpTable;

//Stores pointers to all top-level Data dataHandling components of the program
typedef struct DataHandlingHub {
	struct SaveFile* saveFile;
	struct FailSafe* failSafe;
	struct DataBuffer* buffer;
	struct PortHandler* handler;
	struct SensorCalibration* calibration; //May be NULL
	struct FrameLookUpTable* frameLookUp;
} DataHandlingHub;

//Core
static struct DataHandlingHub dataHandling = { 0 };

//Logs the message into the Debug Output, uses first character for formatting: ':' Headline, '_' End of HeadLine,  '?' Trying, '!' Error, '.' Success, '-' End of File
DATAHANDLINGLIBRARY_API void DebugLog(const char* message, ...);

//Calculates checksum of given DataPacket
DATAHANDLINGLIBRARY_API int CalculateChecksum(DataPacket data);

//Calculates cyclic redundancy check of given DataPacket
DATAHANDLINGLIBRARY_API int CalculateCRC(DataPacket data);

//Calls necessary functions for saving and transmitting data;
//returns {-1} if there was an error with transmitting, {-2} if there was an error with receiving, {-3} if there was an error with saving, and {1} if succesful
DATAHANDLINGLIBRARY_API int UpdateAll();

DATAHANDLINGLIBRARY_API int UpdateBuffer();

DATAHANDLINGLIBRARY_API int UpdateFiles();

//Returns a pointer to access all DataHandling structures
DATAHANDLINGLIBRARY_API DataHandlingHub* GetDataHandling();

//Maps digital sensor values to returned calibrated measurement values
DATAHANDLINGLIBRARY_API float MapSensorValue(int id, int value);

//Writes a calibration point into the SensorCalibration structure
DATAHANDLINGLIBRARY_API void WritePoint(int id, int number, int digitalValue, float analogValue);

//Writes a calibration point into the SensorCalibration structure
DATAHANDLINGLIBRARY_API void AddPoint(int id, int number, CalibrationPoint point);

//Reads a CalibrationPoint from the SensorCalibration structure
DATAHANDLINGLIBRARY_API CalibrationPoint ReadPoint(int id, int number);

//Reads a SensorCalibration structure from the given filepath
DATAHANDLINGLIBRARY_API int ReadCalibration(const char* path);

//Writes a SensorCalibration structure to a file
DATAHANDLINGLIBRARY_API int WriteCalibration();

//Creates a new SensorCalibration structure
DATAHANDLINGLIBRARY_API int CreateCalibration(const char* path);

//Initializes Memory and loads Data from files if possible
DATAHANDLINGLIBRARY_API int Initialize(const char path[]);

//Returns a new empty DataFrame with the specified Sync-Bytes value
DATAHANDLINGLIBRARY_API DataFrame CreateFrame(uint16_t sync);

//Returns a new empty TeleCommand-DataFrame with the specified Sync-Bytes value
DATAHANDLINGLIBRARY_API DataFrame CreateTC(uint16_t sync);

//Returns an empty DataFrame
DATAHANDLINGLIBRARY_API DataFrame EmptyFrame();

//Returns an empty DataFrame, marked as TeleCommand
DATAHANDLINGLIBRARY_API DataFrame EmptyTC();

//Writes data onto a DataFrame according to the ID (enum FrameIdentifier), returns the old value ({0} if empty)
DATAHANDLINGLIBRARY_API int WriteFrame(DataFrame* frame, int id, int value);

//Returns stored data on a DataFrame according to the ID (enum FrameIdentifier)
DATAHANDLINGLIBRARY_API int ReadFrame(DataFrame frame, int id);

//Returns wether a DataFrame contains useful data
DATAHANDLINGLIBRARY_API int FrameIsEmpty(DataFrame frame);

//Returns wether a DataFrame is a TeleCommand-DataFrame
DATAHANDLINGLIBRARY_API int FrameIsTC(DataFrame frame);

//Returns wether the given frame has the specified flag-ID (enum Flags)
DATAHANDLINGLIBRARY_API int FrameHasFlag(DataFrame frame, int id);

//Sets the given flag-ID (enum Flags) for the given frame
DATAHANDLINGLIBRARY_API void FrameAddFlag(DataFrame* frame, int id);

//Adds an outgoing DataFrame to the Buffer, returns the corresponding index
DATAHANDLINGLIBRARY_API int AddOutFrame(DataFrame frame);

//Shorthand for AddOutFrame() and AddSaveFrame()
DATAHANDLINGLIBRARY_API void AddFrame(DataFrame frame);

//Initializes new Buffer-Arrays
DATAHANDLINGLIBRARY_API int CreateBuffer();

//Creates a new Failsafe structure from default values
DATAHANDLINGLIBRARY_API int CreateFailSafe();

//Reads the current Failsafe-file into a structure
DATAHANDLINGLIBRARY_API int ReadFailSafe();

//Updates the current Failsafe-file to match the structure or creates a new one if none was found,
//returns {0} if successful, {1} if it created a new file and {-1} if there was an error
DATAHANDLINGLIBRARY_API int WriteFailSafe();

//Writes the frames added since the last save onto the harddrive, returns the number of Bytes written or {-1} if unsuccessful
DATAHANDLINGLIBRARY_API int WriteSave();

//Creates a new SaveFile structure and file
DATAHANDLINGLIBRARY_API int CreateSave(const char path[]);

//Reloads all frames from the harddrive into the structure, appending excess from the structure, returns the amount of frames loaded
DATAHANDLINGLIBRARY_API int CheckSave();

//Reads a SaveFile-file into a Savefile-structure, creates a new one if none was found
DATAHANDLINGLIBRARY_API int ReadSave(const char path[]);

//Returns the Frame of the SaveFile at the corresponding index, defaults to the last one
DATAHANDLINGLIBRARY_API SaveFileFrame* GetSaveFrame(int index);

//Updates {currentTC} to represent all saved TeleCommand-DataFrames, returns the updated {currentTC}
DATAHANDLINGLIBRARY_API DataFrame UpdateTC();

//Adds a new frame to the end of the SaveFile, returns a pointer to the newly created Frame
DATAHANDLINGLIBRARY_API SaveFileFrame* AddSaveFrame(DataFrame data);

//Shortcut to CreateFrame() and AddSaveFrame(), returns a pointer to the newly created Frame
DATAHANDLINGLIBRARY_API SaveFileFrame* CreateSaveFrame(uint16_t sync);

//Frees allocated Memory of the passed SaveFile's Frames, does not free SaveFile itself
DATAHANDLINGLIBRARY_API void CloseSave();

//Frees all allocated Memory, including "dataHandling" itself, and closes all open Files and Ports
DATAHANDLINGLIBRARY_API void CloseAll();

//Configures and opens the communication port
int LoadPort();

//Tries to send buffered outgoing data via the configured output path, returns the amount of bytes send
int Send();

//Reads received data via the configured path into the incoming buffer, returns the amount of bytes received
int Receive();

#endif // DATAHANDLINGLIBRARY_H
