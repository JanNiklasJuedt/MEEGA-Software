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
#define WINDOWS_OS 0b00000001
#define LINUX_OS 0b00000010
#define MAC_OS 0b00000100
#define ANDROID_OS 0b00001000

#define NONE 0

#define TERMINAL 0b00000001
#define LOGFILE 0b00000010

#define LINEAR 0b00000001
#define QUADRATIC 0b00000010
#define CUBIC 0b00000100


//<-------------------------------------DataHandling Settings------------------------------------->//
#define DATAHANDLINGLIBRARY_OS (WINDOWS_OS)
#define CALIBRATION_METHOD (LINEAR)
#define DEBUG_OUTPUT (LOGFILE + TERMINAL)

#define USE_DEFAULT_VALUES 1
#define TRANSMISSION_DEBUG 0
//<----------------------------------------------------------------------------------------------->//


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
#define DEFAULTCOMPATH "COM4"
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

#else

#define DATAHANDLINGLIBRARY_CONSTANT
#define DATAHANDLINGLIBRARY_API
#define DEFAULTCOMPATH ""
#define BAUD_RATE 0
#define INVALID_HANDLE_VALUE 0

#endif // DATAHANDLINGLIBRARY_OS

//Unneccessary null define
#ifndef NULL
#define NULL (void*)0
#endif // NULL

//DataHandling Constants
#define FRAME_LENGTH sizeof(DataFrame)
#define PACKET_LENGTH sizeof(DataPacket)

#define PATH_LENGTH 100 //Chars
#define BUFFER_LENGTH 10 //DataFrames

#define DATA_LENGTH 48 //Bytes
#define PAYLOAD_LENGTH 16 //Bytes
#define PACKET_BUFFER_LENGTH (DATA_LENGTH / PAYLOAD_LENGTH * BUFFER_LENGTH + 1) //DataPackets

#define CHKSM_TYPE uint16_t
#define SYNC_TYPE uint16_t
typedef unsigned char byte;

#define START_BYTE 0b11111111
#define COMM_TIMEOUT 10 //Milliseconds

#define SENSOR_AMOUNT Nozzle_Temperature_3 + 1
#define TELEMETRY_AMOUNT Experiment_State + 1
#define TELECOMMAND_AMOUNT Test_Run + 1
#define CALIBRATION_POINTS 3

#define LOW_RES 16 //Bits
#define HIGH_RES 24 //Bits
#define DELAY_LEN 16 //Bits
#define BASE_LEN 1 //Bits
#define STM_LEN 2 //Bits
#define EXP_LEN 4 //Bits
#define MAIN_LEN 4 //Bits
#define MAIN_V_LEN 1 //Bits
#define MAIN_T_LEN 3 //Bits
#define TIME_LEN 32 //Bits
#define MSG_ID_LEN 3 //Bits

DATAHANDLINGLIBRARY_CONSTANT const int PathLength = PATH_LENGTH;
DATAHANDLINGLIBRARY_CONSTANT const int DataLength = DATA_LENGTH;

DATAHANDLINGLIBRARY_CONSTANT const float FAILSAFE_VERSION = 1.1f;
DATAHANDLINGLIBRARY_CONSTANT const char FAILSAFE_NAME[] = "MEEGA_FailSafe.txt";

DATAHANDLINGLIBRARY_CONSTANT const float CALIBRATION_VERSION = 1.1f;
DATAHANDLINGLIBRARY_CONSTANT const char CALIBRATION_NAME[] = "MEEGA_Calibration.txt";

DATAHANDLINGLIBRARY_CONSTANT const float SAVEFILE_VERSION = 1.0f;
DATAHANDLINGLIBRARY_CONSTANT const char SAVEFILE_NAME[] = "MEEGA_SaveFile.meega";

DATAHANDLINGLIBRARY_CONSTANT const float VERSION = 0.5f;
DATAHANDLINGLIBRARY_CONSTANT const char DEBUGLOG_NAME[] = "MEEGA_DataHandlingLog.txt";

//Enums and Structs

/// <summary>
/// Telemetry data identifier
/// </summary>
enum DATAHANDLINGLIBRARY_API TMID{
	//Sensors:
	Ambient_Pressure, Compare_Temperature, Tank_Pressure, Tank_Temperature, Chamber_Pressure, Chamber_Temperature_1, Chamber_Temperature_2,
	Nozzle_Pressure_1, Nozzle_Temperature_1, Nozzle_Pressure_2, Nozzle_Temperature_2, Nozzle_Pressure_3, Nozzle_Temperature_3,
	//Householding Sensors:
	Ambient_Pressure_Health, Compare_Temperature_Health, Tank_Pressure_Health, Tank_Temperature_Health, Chamber_Pressure_Health, Chamber_Temperature_1_Health, Chamber_Temperature_2_Health,
	Nozzle_Pressure_1_Health, Nozzle_Temperature_1_Health, Nozzle_Pressure_2_Health, Nozzle_Temperature_2_Health, Nozzle_Pressure_3_Health, Nozzle_Temperature_3_Health,
	//Householding Misc:
	Nozzle_Open, Nozzle_Closed, Nozzle_Servo, Reservoir_Valve, Camera, LEDs, Sensorboard_P, Sensorboard_T, Mainboard, Mainboard_T, Mainboard_V, System_Time, Lift_Off, Start_Experiment, End_Experiment, Mode, Experiment_State
};

/// <summary>
/// Telecommand data identifier
/// </summary>
enum DATAHANDLINGLIBRARY_API TCID {
	Mode_Change, Valve_Delay, Servo_Delay, EoE_Delay, Power_Off_Delay, Nozzle_On_Delay, Dry_Run, LED_Control, Servo_Control, Valve_Control, Camera_Control, Test_Abort, Test_Run
};

/// <summary>
/// DataFrame annotation flags
/// </summary>
enum DATAHANDLINGLIBRARY_API Flag {
	Source, OK, Biterror, Partial, TeleMetry, TeleCommand
};

/// <summary>
/// Stores all data pertaining one timestep, exactly as it will be saved on the harddrive
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API DataFrame {
	//Signals the beginning of a new Frame (= -1)
	byte start;
	//Used to mark DataFrames for faulty or missing data and TeleCommand
	byte flag;
	//Used to form DataPackets (0 denotes an empty DataFrame)
	SYNC_TYPE sync;
	//Byte Array for saving data
	byte data[DATA_LENGTH];
	//Checksum to check for complete Frames
	CHKSM_TYPE chksm;
} DataFrame;

/// <summary>
/// Stores the data contained in one packet of the transmission protocol
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API DataPacket {
	//Signals the beginning of a new Packet (= -1)
	byte start;
	//Used to identify payload data
	byte msg;
	//Used to stitch together DataFrames (= DataFrame.sync)
	SYNC_TYPE sync;
	//Byte Array containing a part of the Frame.data
	byte payload[PAYLOAD_LENGTH];
	CHKSM_TYPE chksm;
	//Cyclic Redundancy Check Output
	CHKSM_TYPE crc;
} DataPacket;

/// <summary>
/// Input/output buffer for transmissions
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API DataBuffer {
	struct DataPacket inPackets[PACKET_BUFFER_LENGTH];
	struct DataPacket outPackets[PACKET_BUFFER_LENGTH];
	struct DataFrame inFrames[BUFFER_LENGTH];
	struct DataFrame outFrames[BUFFER_LENGTH];
} DataBuffer;

/// <summary>
/// Stores all persistent data needed for a (spontanious) program reboot
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API FailSafe {
	float version;
	time_t dateTime;
	//path used to look up the newest savefile
	char saveFilePath[PATH_LENGTH];
	//if the experiment run of the newest savefile has been completed (Bool)
	byte complete;
	//if the program has exited nominally (Bool)
	byte nominalExit;
	//identifier of the used input/output path
	char comPath[PATH_LENGTH];
	//path used to look up calibration data
	char calPath[PATH_LENGTH];
	byte changed;
} FailSafe;

/// <summary>
/// Stores one DataFrame of a savefile, as well as pointers to the neighbours
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API SaveFrame {
	struct DataFrame data;
	struct SaveFrame* nextFrame;
	struct SaveFrame* previousFrame;
} SaveFrame;

/// <summary>
/// Stores all data collected/received during the mission
/// </summary>
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

/// <summary>
/// Stores all data neccessary for Communication devices
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API PortHandler {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	DCB options;
	HANDLE comHandle;
	COMMTIMEOUTS timeout;
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	struct termios options;
	int comHandle;
	int timeout;
#else
	int options;
	int comHandle;
	int timeout;
#endif
	int valid;
	char comPath[PATH_LENGTH];
} PortHandler;

/// <summary>
/// Stores one calibration point consisting of the digital ADC output and the corresponding analog calibration measurement
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API CalibrationPoint {
	long long digital;
	float analog;
	char valid;
} CalibrationPoint;

/// <summary>
/// Stores all data neccessary for sensor value mapping
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API SensorCalibration {
	float version;
	time_t dateTime;
	byte sorted;
	byte changed;
	struct CalibrationPoint points[SENSOR_AMOUNT][CALIBRATION_POINTS];
	char calibrationFilePath[PATH_LENGTH];
} SensorCalibration;

/// <summary>
/// Stores data neccessary for reading/writing Frame-data
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API FrameLookUpTable {
	int telemetry_Pos_Len[TELEMETRY_AMOUNT][2];
	int telecommand_Pos_Len[TELECOMMAND_AMOUNT][2];
} FrameLookUpTable;

/// <summary>
/// Stores pointers to all top-level Data dataHandling components of the program
/// </summary>
typedef struct DATAHANDLINGLIBRARY_API DataHandlingHub {
	struct SaveFile* saveFile;
	struct FailSafe* failSafe;
	struct DataBuffer* buffer;
	struct PortHandler* handler;
	struct SensorCalibration* calibration; //May be NULL
	struct FrameLookUpTable* frameLookUp;
} DataHandlingHub;

//Function Delcarations

/// <summary>
/// Logs the message into the Debug Output with following format characters:
/// {:} New Section
/// {_} End Section
/// {-} End DebugLog
/// {?} Fill in " ..." 
/// {!} Error message
/// {#} Integer argument 
/// {§} String argument
/// {@} Pointer argument
/// {~} Integer Array argument (expects: int length, int* array)
/// </summary>
/// <param name="message">String containing format characters</param>
/// <param name="...">Variadic arguments for format characters</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void DebugLog(const char* message, ...);

/// <summary>
/// Prints the active SaveFile to the Debug Output
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void DebugSaveFile();

/// <summary>
/// Prints the content of a given DataFrame to the Debug Output
/// </summary>
/// <param name="frame"></param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void DebugSaveFrame(DataFrame frame);

/// <summary>
/// Prints the content of the last DataFrame in the active SaveFile to the Debug Output
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void DebugLastFrame();

/// <summary>
/// Calculates checksum of DataFrames
/// </summary>
/// <param name="data">DataFrame to check</param>
/// <returns>Calculated checksum</returns>
DATAHANDLINGLIBRARY_API CHKSM_TYPE CalculateChecksum(DataFrame data);

/// <summary>
/// Calculates cyclic redundancy check of DataPackets
/// </summary>
/// <param name="data">DataPacket to check</param>
/// <returns>{0} for no Errors {1} for unsolved Errors {-1} for solved Errors</returns>
DATAHANDLINGLIBRARY_API int CalculateCRC(DataPacket* data);

/// <summary>
/// Calls neccessary functions for saving and transmitting data
/// </summary>
/// <returns>The amount of Errors</returns>
DATAHANDLINGLIBRARY_API int UpdateAll();

/// <summary>
/// Updates the buffer, handles packet and transmission operations
/// </summary>
/// <returns>The amount of Errors</returns>
DATAHANDLINGLIBRARY_API int UpdateBuffer();

/// <summary>
/// Writes all changes to the corresponding files
/// </summary>
/// <returns>The amount of Errors</returns>
DATAHANDLINGLIBRARY_API int UpdateFiles();

/// <summary>
/// </summary>
/// <returns>A pointer to access all DataHandling structures</returns>
DATAHANDLINGLIBRARY_API DataHandlingHub* GetDataHandling();

/// <summary>
/// </summary>
/// <returns>A pointer to the FailSafe structure</returns>
DATAHANDLINGLIBRARY_API FailSafe* GetFailSafe();

/// <summary>
/// Maps digital sensor values to calibrated measurement values
/// </summary>
/// <param name="id">TMID of the sensor</param>
/// <param name="value">Digital sensor value</param>
/// <returns>Analog measurement value</returns>
DATAHANDLINGLIBRARY_API float MapSensorValue(int id, long long value);

/// <summary>
/// Writes a calibration point into the SensorCalibration structure
/// </summary>
/// <param name="id">TMID of the sensor</param>
/// <param name="number">Index of the point</param>
/// <param name="digitalValue"></param>
/// <param name="analogValue"></param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void WritePoint(int id, int number, long long digitalValue, float analogValue);

/// <summary>
/// Writes a calibration point into the SensorCalibration structure
/// </summary>
/// <param name="id">TMID of the sensor</param>
/// <param name="number">Index of the point</param>
/// <param name="point"></param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void AddPoint(int id, int number, CalibrationPoint point);

/// <summary>
/// Reads a CalibrationPoint from the SensorCalibration structure
/// </summary>
/// <param name="id">TMID of the sensor</param>
/// <param name="number">Index of the point</param>
/// <returns>Read CalibrationPoint</returns>
DATAHANDLINGLIBRARY_API CalibrationPoint ReadPoint(int id, int number);

/// <summary>
/// Reads the SensorCalibration structure from a file
/// </summary>
/// <param name="path">String with system path and name</param>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int ReadCalibration(const char* path);

/// <summary>
/// Writes the SensorCalibration structure to a file
/// </summary>
/// <returns>{1} if successful, {0} if file could not be read, {-1} if file was not found</returns>
DATAHANDLINGLIBRARY_API int WriteCalibration();

/// <summary>
/// Creates a new SensorCalibration structure
/// </summary>
/// <param name="path">String with system path and name</param>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int CreateCalibration(const char* path);

/// <summary>
/// Initializes Memory and loads Data from files if possible
/// </summary>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int Initialize();

/// <summary>
/// </summary>
/// <returns>A new DataFrame</returns>
DATAHANDLINGLIBRARY_API DataFrame CreateFrame();

/// <summary>
/// </summary>
/// <returns>A new TeleCommand-DataFrame</returns>
DATAHANDLINGLIBRARY_API DataFrame CreateTC();

/// <summary>
/// </summary>
/// <returns>An empty DataFrame</returns>
DATAHANDLINGLIBRARY_API DataFrame EmptyFrame();

/// <summary>
/// </summary>
/// <returns>An empty TeleCommand-DataFrame</returns>
DATAHANDLINGLIBRARY_API DataFrame EmptyTC();

/// <summary>
/// Writes data onto a DataFrame
/// </summary>
/// <param name="frame">Pointer to the frame</param>
/// <param name="id">TMID or TCID, according to the frame</param>
/// <param name="value"></param>
/// <returns>The old value ({0} if empty)</returns>
DATAHANDLINGLIBRARY_API long long WriteFrame(DataFrame* frame, int id, long long value);

/// <summary>
/// Reads data from a DataFrame
/// </summary>
/// <param name="frame">DataFrame to read from</param>
/// <param name="id">TMID or TCID, according to the frame</param>
/// <returns>Data read</returns>
DATAHANDLINGLIBRARY_API long long ReadFrame(DataFrame frame, int id);

/// <summary>
/// </summary>
/// <param name="frame">DataFrame to check</param>
/// <returns>Whether the DataFrame contains useful data</returns>
DATAHANDLINGLIBRARY_API int FrameIsEmpty(DataFrame frame);

/// <summary>
/// </summary>
/// <param name="frame">DataFrame to check</param>
/// <returns>Whether the DataFrame is a TeleCommand-DataFrame</returns>
DATAHANDLINGLIBRARY_API int FrameIsTC(DataFrame frame);

/// <summary>
/// Checks if the DataFrame has the specified Flag
/// </summary>
/// <param name="frame">DataFrame to check</param>
/// <param name="id">From enum Flags</param>
/// <returns>Whether the DataFrame has the flag set</returns>
DATAHANDLINGLIBRARY_API int FrameHasFlag(DataFrame frame, int id);

/// <summary>
/// Sets the specified Flag for the DataFrame
/// </summary>
/// <param name="frame">Pointer to the DataFrame</param>
/// <param name="id">From enum Flags</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void FrameSetFlag(DataFrame* frame, int id); 

/// <summary>
/// Removes the specified Flag from the DataFrame
/// </summary>
/// <param name="frame">Pointer to the DataFrame</param>
/// <param name="id">From enum Flags</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void FrameRemoveFlag(DataFrame* frame, int id);

/// <summary>
/// Adds an outgoing DataFrame to the Buffer
/// </summary>
/// <param name="frame">DataFrame to add</param>
/// <returns>The corresponding index</returns>
DATAHANDLINGLIBRARY_API int AddOutFrame(DataFrame frame);

/// <summary>
/// Shorthand for AddOutFrame() and AddSaveFrame()
/// </summary>
/// <param name="frame">DataFrame to add</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void AddFrame(DataFrame frame);

/// <summary>
/// Initializes new Buffer-Arrays
/// </summary>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int CreateBuffer();

/// <summary>
/// Creates a new Failsafe structure from default values
/// </summary>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int CreateFailSafe();

/// <summary>
/// Reads a Failsafe-file into a structure
/// </summary>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int ReadFailSafe();

/// <summary>
/// Writes the Failsafe-structure into a file
/// </summary>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int WriteFailSafe();

/// <summary>
/// Writes the frames added since the last save onto the harddrive
/// </summary>
/// <returns>The number of bytes written or {-1} if unsuccessful</returns>
DATAHANDLINGLIBRARY_API int WriteSave();

/// <summary>
/// Creates a new SaveFile structure and file
/// </summary>
/// <param name="path">System path and name file</param>
/// <returns>Whether successful</returns>
DATAHANDLINGLIBRARY_API int CreateSave(const char path[]);

//Rewrite Due
DATAHANDLINGLIBRARY_API int CheckSave();

/// <summary>
/// Reads a SaveFile-file into the Savefile-structure, discarding current memory
/// </summary>
/// <param name="path">System path and name of file</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API int ReadSave(const char path[]);

/// <summary>
/// Returns the Frame of the SaveFile at the corresponding index, defaults to the last one and ignores TC Frames
/// </summary>
/// <param name="index"></param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API DataFrame GetSaveFrame(int index);

/// <summary>
/// Returns the next Frame, counting from the last successful call to GetSaveFrame()
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API DataFrame GetNextFrame();

/// <summary>
/// </summary>
/// <returns>The newest TC Frame</returns>
DATAHANDLINGLIBRARY_API DataFrame GetTC();

/// <summary>
/// Adds a new frame to the end of the SaveFile
/// </summary>
/// <param name="data">DataFrame to add</param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void AddSaveFrame(DataFrame data);

/// <summary>
/// Frees allocated Memory of the loaded SaveFile's Frames, does not free SaveFile itself
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void CloseSave();

/// <summary>
/// Frees all allocated Memory and closes all open Files and Ports
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void CloseAll();

/// <summary>
/// Tries to send outgoing data via the CommPort
/// </summary>
/// <returns>The Amount of bytes send</returns>
DATAHANDLINGLIBRARY_API int Send();

/// <summary>
/// Reads received data via the CommPort into the buffer
/// </summary>
/// <returns>The amount of bytes written to buffer</returns>
DATAHANDLINGLIBRARY_API int Receive();

/// <summary>
/// Tries to open the Communication Port with the specified name
/// </summary>
/// <param name="name"></param>
/// <returns></returns>
DATAHANDLINGLIBRARY_API int SetPort(const char name[]);

/// <summary>
/// </summary>
/// <returns>Whether a Communication Port is opened and ready to use</returns>
DATAHANDLINGLIBRARY_API int PortIsOpen();

/// <summary>
/// Closes an open Communication Port
/// </summary>
/// <returns></returns>
DATAHANDLINGLIBRARY_API void ClosePort();

//Tries to open the comm Port with the specified name
DATAHANDLINGLIBRARY_API int SetPort(const char name[]);

#endif // DATAHANDLINGLIBRARY_H