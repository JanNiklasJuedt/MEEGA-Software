//Header File of DataHandlingLibrary
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>

#ifndef DATAHANDLINGLIBRARY_H
#define DATAHANDLINGLIBRARY_H

//DataHandling Constants for Settings
#define WINDOWS_OS 0
#define LINUX_OS 1
#define MAC_OS 2
#define ANDROID_OS 3

#define NONE -1

#define TERMINAL 1
#define LOGFILE 2

#define LINEAR 0
#define QUADRATIC 1
#define CUBIC 2

//DataHandling Settings
#define DATAHANDLINGLIBRARY_OS WINDOWS_OS
#define CALIBRATION_METHOD NONE
#define DEBUG_OUTPUT TERMINAL + LOGFILE
#define USE_DEFAULT_VALUES 1
#define RECEIVE_BLOCKING 1

//OS related stuff
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)

#define WIN32_LEAN_AND_MEAN
#include "windows.h"

#ifdef DATAHANDLINGLIBRARY_EXPORTS
#define DATAHANDLINGLIBRARY_API __declspec(dllexport)
#else
#define DATAHANDLINGLIBRARY_API __declspec(dllimport)
#endif // DATAHANDLINGLIBRARY_EXPORTS

#define DATAHANDLINGLIBRARY_CONSTANT __declspec(dllexport)
#define DEFAULTCOMPATH "COM3"
#define BAUD_RATE 38400

#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)

#include <termios.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

#define DATAHANDLINGLIBRARY_CONSTANT
#define DATAHANDLINGLIBRARY_API
#define DEFAULTCOMPATH "/dev/ttyAMA0"
#define BAUD_RATE B38400
#define INVALID_HANDLE_VALUE -1

#endif // DATAHANDLINGLIBRARY_OS

//Unneccessary null define
#ifndef NULL
#define NULL (void*)0
#endif // NULL

//DataHandling Constants
#define FRAME_LENGTH sizeof(DataFrame)
#define PACKET_LENGTH sizeof(DataPacket)

#define PATH_LENGTH 100 //Chars
#define BUFFER_LENGTH 10 //DataPackets & DataFrames

#define DATA_LENGTH 42 //Bytes
#define PAYLOAD_LENGTH 21 //Bytes

#define RECEIVE_LENGTH (DATA_LENGTH / PAYLOAD_LENGTH * PACKET_LENGTH)

#define CHKSM_TYPE uint16_t
#define SYNC_TYPE uint16_t
typedef unsigned char byte;

#define SENSOR_AMOUNT Nozzle_Temperature_3 + 1
#define TELEMETRY_AMOUNT Experiment_State + 1
#define TELECOMMAND_AMOUNT Test_Run + 1
#define CALIBRATION_POINTS 3

#define LOW_RES 16 //Bits
#define HIGH_RES 24 //Bits
#define DELAY_LEN 16 //Bits
#define BASE_LEN 1 //Bits
#define STM_LEN 2 //Bits
#define EXP_LEN 3 //Bits
#define MAIN_LEN 4 //Bits
#define TIME_LEN 32 //Bits
#define MSG_ID_LEN 6 //Bits

DATAHANDLINGLIBRARY_CONSTANT const int PathLength = PATH_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int BufferLength = BUFFER_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int DataLength = DATA_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int PayloadLength = PAYLOAD_LENGTH;

DATAHANDLINGLIBRARY_CONSTANT const float FAILSAFE_VERSION = 1.1f;
DATAHANDLINGLIBRARY_CONSTANT const char FAILSAFE_NAME[] = "MEEGA_FailSafe.txt";

DATAHANDLINGLIBRARY_CONSTANT const float CALIBRATION_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char CALIBRATION_NAME[] = "MEEGA_Calibration.txt";

DATAHANDLINGLIBRARY_CONSTANT const float SAVEFILE_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char SAVEFILE_NAME[] = "MEEGA_SaveFile.meega";

DATAHANDLINGLIBRARY_CONSTANT const float VERSION = 0.5f;
DATAHANDLINGLIBRARY_CONSTANT const char DEBUGLOG_NAME[] = "MEEGA_DataHandlingLog.txt";

//Enums and Structs

//Telemetry data identifier
enum DATAHANDLINGLIBRARY_API TMID{
	//Sensors:
	Ambient_Pressure, Compare_Temperature, Tank_Pressure, Tank_Temperature, Chamber_Pressure, Chamber_Temperature,
	Nozzle_Pressure_1, Nozzle_Temperature_1, Nozzle_Pressure_2, Nozzle_Temperature_2, Nozzle_Pressure_3, Nozzle_Temperature_3,
	//Householding Sensors:
	Ambient_Pressure_Health, Compare_Temperature_Health, Tank_Pressure_Health, Tank_Temperature_Health, Chamber_Pressure_Health, Chamber_Temperature_Health,
	Nozzle_Pressure_1_Health, Nozzle_Temperature_1_Health, Nozzle_Pressure_2_Health, Nozzle_Temperature_2_Health, Nozzle_Pressure_3_Health, Nozzle_Temperature_3_Health,
	//Householding Misc:
	Nozzle_Open, Nozzle_Closed, Nozzle_Servo, Reservoir_Valve, Camera, LEDs, Sensorboard_P, Sensorboard_T, Mainboard, System_Time, Lift_Off, Start_Experiment, End_Experiment, Mode, Experiment_State
};

//Telecommand data identifier
enum DATAHANDLINGLIBRARY_API TCID {
	Mode_Change, Valve_Delay, Servo_Delay, EoE_Delay, Power_Off_Delay, Nozzle_On_Delay, Dry_Run, LED_Control, Servo_Control, Valve_Control, Camera_Control, Test_Abort, Test_Run
};

//DataFrame annotation flags
enum DATAHANDLINGLIBRARY_API Flag {
	Source, OK, Biterror, Partial, TeleCommand
};

//Stores all data pertaining one timestep (frame), exactly as it will be saved on the harddrive
typedef struct DATAHANDLINGLIBRARY_API DataFrame {
	//Signals the beginning of a new Frame (= -1)
	byte start;
	//Used to form DataPackets (0 denotes an empty DataFrame)
	SYNC_TYPE sync;
	//Used to mark DataFrames for faulty or missing data and TeleCommand
	byte flag;
	//Byte Array for saving data
	byte data[DATA_LENGTH];
	//Checksum to check for complete Frames
	CHKSM_TYPE chksm;
} DataFrame;

//Stores the data contained in one packet of the transmission protocol
typedef struct DATAHANDLINGLIBRARY_API DataPacket {
	//Signals the beginning of a new Packet (= -1)
	byte start;
	//Used to stitch together DataFrames (= DataFrame.sync)
	SYNC_TYPE sync;
	//Used to identify payload data
	byte msg;
	//Byte Array containing a part of the Frame.data
	byte payload[PAYLOAD_LENGTH];
	//Checksum of the corresponding Frame
	CHKSM_TYPE chksm;
	//Cyclic Redundancy Check Output
	CHKSM_TYPE crc;
} DataPacket;

//This acts as an input/output buffer for transmissions
typedef struct DATAHANDLINGLIBRARY_API DataBuffer {
	byte* incomingPos;
	int incomingbytes;
	byte* outgoingPos;
	int outgoingbytes;
	struct DataPacket inPackets[BUFFER_LENGTH];
	struct DataPacket outPackets[BUFFER_LENGTH];
	struct DataFrame inFrames[BUFFER_LENGTH];
	struct DataFrame outFrames[BUFFER_LENGTH];
} DataBuffer;

//Stores all persistent data needed for a (spontanious) program reboot
typedef struct DATAHANDLINGLIBRARY_API FailSafe {
	float version;
	time_t dateTime;
	//path used to look up the newest savefile
	char saveFilePath[PATH_LENGTH];
	//if the experiment run of the newest savefile has been completed (Bool)
	byte complete;
	//if the program has exited nominally (Bool)
	byte nominalExit;
	//current operating mode of the program (test: "0" / flight: "")
	char mode;
	//connection mode of the groundstation (unused for onboard)
	char conn;
	//language of the groundstation (unused for onboard)
	char lang;
	//identifier of the used input/output path
	char comPath[PATH_LENGTH];
	//path used to look up calibration data
	char calPath[PATH_LENGTH];
	byte changed;
} FailSafe;

//Stores one DataFrame of a savefile, as well as a pointer to the next one
typedef struct DATAHANDLINGLIBRARY_API SaveFrame {
	struct DataFrame data;
	struct SaveFrame* nextFrame;
	struct SaveFrame* previousFrame;
} SaveFrame;

//Stores all data collected/received during the mission
typedef struct DATAHANDLINGLIBRARY_API SaveFile {
	float version;
	time_t dateTime;
	//pointer towards the first "DataFrame", subsequent frames are pointed to by themselves
	struct SaveFrame* firstFrame;
	struct SaveFrame* lastFrame;
	//total amount of frames added to the SaveFile
	int frameAmount;
	//total amount of frames already written to the harddrive
	int savedAmount;
	//amount of frames currently loaded into memory
	int loadedAmount;
	//amount of frames unloaded from memory (unimplemented)
	int unloadedAmount;
	//the newest TeleCommand
	struct DataFrame currentTC;
	//path to the associated file
	char saveFilePath[PATH_LENGTH];
} SaveFile;

//Stores all data neccessary for communication devices
typedef struct DATAHANDLINGLIBRARY_API PortHandler {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	DCB options;
	HANDLE comHandle;
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	struct termios options;
	int comHandle;
#else
	int options;
	int comHandle;
#endif
	char comPath[PATH_LENGTH];
} PortHandler;

//Stores one calibration point consisting of the digital ADC output and the corresponding analog calibration measurement
typedef struct DATAHANDLINGLIBRARY_API CalibrationPoint {
	long long digital;
	float analog;
	char valid;
} CalibrationPoint;

//Stores all data neccessary for sensor value mapping
typedef struct DATAHANDLINGLIBRARY_API SensorCalibration {
	float version;
	time_t dateTime;
	byte sorted;
	byte changed;
	struct CalibrationPoint points[SENSOR_AMOUNT][CALIBRATION_POINTS];
	char calibrationFilePath[PATH_LENGTH];
} SensorCalibration;

//Stores data neccessary for reading/writing Frame-data
typedef struct DATAHANDLINGLIBRARY_API FrameLookUpTable {
	int telemetry_Pos_Len[TELEMETRY_AMOUNT][2];
	int telecommand_Pos_Len[TELECOMMAND_AMOUNT][2];
} FrameLookUpTable;

//Stores pointers to all top-level Data dataHandling components of the program
typedef struct DATAHANDLINGLIBRARY_API DataHandlingHub {
	struct SaveFile* saveFile;
	struct FailSafe* failSafe;
	struct DataBuffer* buffer;
	struct PortHandler* handler;
	struct SensorCalibration* calibration; //May be NULL
	struct FrameLookUpTable* frameLookUp;
} DataHandlingHub;

//Function Delcarations

//Logs the message into the Debug Output, uses special characters for formatting (:,-,_,?,!,#,§,@)
DATAHANDLINGLIBRARY_API void DebugLog(const char* message, ...);

//Calculates checksum of given DataFrame
DATAHANDLINGLIBRARY_API CHKSM_TYPE CalculateChecksum(DataFrame data);

//Calculates cyclic redundancy check with given DataPacket, returns whether there are uncorrected errors
DATAHANDLINGLIBRARY_API int CalculateCRC(DataPacket* data);

//Calls necessary functions for saving and transmitting data;
DATAHANDLINGLIBRARY_API int UpdateAll();

//Updates the buffer, handles packet and transmission operations
DATAHANDLINGLIBRARY_API int UpdateBuffer();

//Writes all changes to the corresponding files
DATAHANDLINGLIBRARY_API int UpdateFiles();

//Returns a pointer to access all DataHandling structures
DATAHANDLINGLIBRARY_API DataHandlingHub* GetDataHandling();

//Returns a pointer to the FailSafe structure
DATAHANDLINGLIBRARY_API FailSafe* GetFailSafe();

//Maps digital sensor values to returned calibrated measurement values
DATAHANDLINGLIBRARY_API float MapSensorValue(int id, long long value);

//Writes a calibration point into the SensorCalibration structure
DATAHANDLINGLIBRARY_API void WritePoint(int id, int number, long long digitalValue, float analogValue);

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
DATAHANDLINGLIBRARY_API int Initialize();

//Returns a new DataFrame
DATAHANDLINGLIBRARY_API DataFrame CreateFrame();

//Returns a new empty TeleCommand-DataFrame
DATAHANDLINGLIBRARY_API DataFrame CreateTC();

//Returns an empty DataFrame
DATAHANDLINGLIBRARY_API DataFrame EmptyFrame();

//Returns an empty DataFrame, marked as TeleCommand
DATAHANDLINGLIBRARY_API DataFrame EmptyTC();

//Writes data onto a DataFrame according to the ID (enum TCID / TMID), returns the old value ({0} if empty)
DATAHANDLINGLIBRARY_API long long WriteFrame(DataFrame* frame, int id, long long value);

//Returns stored data on a DataFrame according to the ID (enum TCID / TMID)
DATAHANDLINGLIBRARY_API long long ReadFrame(DataFrame frame, int id);

//Returns wether a DataFrame contains useful data
DATAHANDLINGLIBRARY_API int FrameIsEmpty(DataFrame frame);

//Returns wether a DataFrame is a TeleCommand-DataFrame
DATAHANDLINGLIBRARY_API int FrameIsTC(DataFrame frame);

//Returns wether the given frame has the specified flag-ID (enum Flags)
DATAHANDLINGLIBRARY_API int FrameHasFlag(DataFrame frame, int id);

//Sets the given flag-ID (enum Flags) for the given frame
DATAHANDLINGLIBRARY_API void FrameSetFlag(DataFrame* frame, int id); 

//Removes the given flag-ID (enum Flags) for the given frame
DATAHANDLINGLIBRARY_API void FrameRemoveFlag(DataFrame* frame, int id);

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

//Updates the current Failsafe-file to match the structure, returns whether successful
DATAHANDLINGLIBRARY_API int WriteFailSafe();

//Writes the frames added since the last save onto the harddrive, returns the number of bytes written or {-1} if unsuccessful
DATAHANDLINGLIBRARY_API int WriteSave();

//Creates a new SaveFile structure and file
DATAHANDLINGLIBRARY_API int CreateSave(const char path[]);

//Rewrite Due
DATAHANDLINGLIBRARY_API int CheckSave();

//Reads a SaveFile-file into a Savefile-structure, discarding current memory
DATAHANDLINGLIBRARY_API int ReadSave(const char path[]);

//Returns the Frame of the SaveFile at the corresponding index, defaults to the last one and ignores TC Frames!
DATAHANDLINGLIBRARY_API DataFrame GetSaveFrame(int index);

//Returns the next Frame, counting from the last successful call to GetSaveFrame()
DATAHANDLINGLIBRARY_API DataFrame GetNextFrame();

//Returns the newest TC Frame
DATAHANDLINGLIBRARY_API DataFrame GetTC();

//Adds a new frame to the end of the SaveFile
DATAHANDLINGLIBRARY_API void AddSaveFrame(DataFrame data);

//Frees allocated Memory of the passed SaveFile's Frames, does not free SaveFile itself
DATAHANDLINGLIBRARY_API void CloseSave();

//Frees all allocated Memory, including "dataHandling" itself, and closes all open Files and Ports
DATAHANDLINGLIBRARY_API void CloseAll();

//Tries to send outgoing data via the configured output path, returns the amount of bytes send
DATAHANDLINGLIBRARY_API int Send(byte* start, int amount);

//Reads received data via the configured path into the buffer, returns the amount of bytes received
DATAHANDLINGLIBRARY_API int Receive(byte* buffer, int max);

//Tries to open the comm Port with the specified name
DATAHANDLINGLIBRARY_API int SetPort(const char name[]);

#endif // DATAHANDLINGLIBRARY_H