//Source File of DataHandlingLibrary
#include "DataHandlingLibrary.h"

//Core initialization:
static struct DataHandlingHub dataHandling = { NULL, NULL, NULL, NULL, NULL, NULL }; //Access to all reserved memory
static SaveFrame* currentFrame = NULL; //Used by GetNextFrame()

//INTERNAL Declarations:
static int _SetPositions_(); //Fills in the FrameLookUpTable
static int _CreateHandler_(); //Reserves memory for the PortHandler
static int _CreateFrameLookUp_(); //Reserves memory for the FrameLookUpTable
static void _SortCalibration_(); //Sorts the CalibrationPoint-Array
static SYNC_TYPE _GetSync_(); //Returns a new, usable sync value
static byte _ToMSG_(byte type, byte id); //Encodes the MSG-byte
static void _FromMSG_(byte msg, byte* type_out, byte* id_out); //Decodes the MSG-byte
static void _ShiftArray_(void* array, int elementSize, int arraySize, int offsetAmount); //Shifts values inside an array
static int _SetPortConfig_(); //Configures Port settings, needs an opened Port

//EX-EXPORT (INTERNAL) Declarations:
DataPacket GetInPacket(); //Returns the latest incoming Packet
int AddOutPacket(DataPacket data); //Adds a Packet to the outgoing buffer
int VirtualSave(); //Creates a SaveFile-struct in memory
DataPacket CreatePacket(SYNC_TYPE sync); //Creates a Packet with the designated sync-value
DataPacket EmptyPacket(); //Creates an empty Packet
int FormPackets(); //Converts all buffered DataFrames into buffered outgoing DataPackets, returns the amount converted
int FormFrames(); //Converts all buffered incoming DataPackets into buffered DataFrames (with {0} values if parts are missing), returns the amount converted
DataFrame GetOutFrame(); //Returns the latest buffered outgoing DataFrame and removes it from the buffer
int AddInFrame(DataFrame frame); //Adds an incoming DataFrame to the Buffer, returns the corresponding index
DataFrame GetInFrame(); //Returns the latest buffered incoming DataFrame and removes it from the buffer
int LoadPort(); //Configures and opens the communication port

//Internal Implementations:
int _SetPositions_()
{
	if (dataHandling.frameLookUp == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int pos = 0;
	int length = 0;
	int id = 0;
	for (; id < TELEMETRY_AMOUNT; id++) {
		if (id < SENSOR_AMOUNT) length = HIGH_RES;
		else length = BASE_LEN;
		switch (id) {
		case Camera: length = 0; break;
		case Tank_Pressure:
		case Ambient_Pressure: length = LOW_RES; break;
		case Experiment_State: length = EXP_LEN; break;
		case Sensorboard_P:
		case Sensorboard_T: length = STM_LEN; break;
		case Mainboard: length = MAIN_LEN; break;
		case System_Time: length = TIME_LEN; break;
		}
		dataHandling.frameLookUp->telemetry_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telemetry_Pos_Len[id][1] = length;
		pos += length;

	}
	if (pos > DATA_LENGTH * 8) {
		DebugLog("!Unsufficient (Data) Real Estate");
		return 0;
	}
	for (id = 0, pos = 0; id < TELECOMMAND_AMOUNT; id++) {
		length = BASE_LEN + 1;
		switch (id) {
		case Power_Off_Delay:
		case Nozzle_On_Delay: length = 0; break;
		case Valve_Delay:
		case Servo_Delay:
		case EoE_Delay:
		case Servo_Control: length = DELAY_LEN + 1; break;
		}
		dataHandling.frameLookUp->telecommand_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telecommand_Pos_Len[id][1] = length;
		pos += length;

	}
	if (pos > DATA_LENGTH * 8) {
		DebugLog("!Unsufficient (Data) Real Estate");
		return 0;
	}
	return 1;
}

int _CreateHandler_()
{
	if (dataHandling.handler != NULL) free(dataHandling.handler);
	dataHandling.handler = malloc(sizeof(PortHandler));
	if (dataHandling.handler == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*)dataHandling.handler;
	for (int i = 0; i < sizeof(PortHandler); i++) {
		bytePtr[i] = 0;
	}
	dataHandling.handler->comHandle = INVALID_HANDLE_VALUE;
	if (dataHandling.failSafe != NULL) {
		strcpy(dataHandling.handler->comPath, dataHandling.failSafe->comPath);
		dataHandling.failSafe->changed = 1;
	}
	else {
		DebugLog("!Could not find FailSafe");
	}
	if ((dataHandling.handler->comPath[0] == '\0') & USE_DEFAULT_VALUES)
		strcpy(dataHandling.handler->comPath, DEFAULTCOMPATH);
	return 1;
}

int _CreateFrameLookUp_()
{
	if (dataHandling.frameLookUp != NULL) free(dataHandling.frameLookUp);
	dataHandling.frameLookUp = malloc(sizeof(FrameLookUpTable));
	if (dataHandling.frameLookUp == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*)dataHandling.frameLookUp;
	for (int i = 0; i < sizeof(FrameLookUpTable); i++)
		bytePtr[i] = 0;
	return 1;
}

void _SortCalibration_()
{
	if (dataHandling.calibration == NULL) {
		DebugLog("!Could not find Calibration");
		return;
	}
	if (dataHandling.calibration->sorted) return;
	int i, j, k;
	CalibrationPoint cpy, * upper, * lower;
	//Iterate through all Sensors
	for (i = 0; i < SENSOR_AMOUNT; i++) {
		//Bubble-Sort for each Sensor
		for (j = CALIBRATION_POINTS - 1; j > 0; j--) {
			for (k = 1; k <= j; k++) {
				upper = dataHandling.calibration->points[i] + k, lower = dataHandling.calibration->points[i] + k - 1;
				//Sort by ascending digital value and validness (valid Points at lower indexes)
				if ((upper->digital < lower->digital) || (upper->valid & !(lower->valid))) {
					cpy = *upper;
					*upper = *lower;
					*lower = cpy;
				}
			}
		}
	}
	dataHandling.calibration->sorted = 1;
	dataHandling.calibration->changed = 1;
}

static SYNC_TYPE _GetSync_()
{
	static SYNC_TYPE current = 0;
	current++;
	if (current == -1) current = 1;
	return current;
}

static byte _ToMSG_(byte type, byte id)
{
	if ((id < (1 << MSG_ID_LEN)) & (type < (1 << (8 - MSG_ID_LEN)))) return (type << MSG_ID_LEN) + id;
	return 0;
}

void _FromMSG_(byte msg, byte* type_out, byte* id_out)
{
	*id_out = msg % (1 << MSG_ID_LEN);
	*type_out = msg >> MSG_ID_LEN;
	return;
}

void _ShiftArray_(void* array, int elementSize, int arraySize, int offsetAmount)
{
	if (elementSize < 0 || arraySize < 0 || array == NULL) return;
	int i;
	byte* byteArray = array;
	if (offsetAmount < 0) {
		for (i = 0; i < (arraySize * elementSize); i++) {
			if (i < ((arraySize + offsetAmount) * elementSize)) byteArray[i] = byteArray[i - offsetAmount * elementSize];
			else byteArray[i] = 0;
		}
	}
	else if (offsetAmount > 0) {
		for (i = (arraySize * elementSize) - 1; i >= 0; i--) {
			if (i >= (offsetAmount * elementSize)) byteArray[i] = byteArray[i - offsetAmount * elementSize];
			else byteArray[i] = 0;
		}
	}
	return;
}

//External functions:
int Initialize()
{
	DebugLog("Setting up DataHandling:");
	if (!ReadFailSafe()) {
		CreateFailSafe();
	}
	int readExisting = 1;
	if (dataHandling.failSafe == NULL) readExisting = 0;
	else readExisting = !(dataHandling.failSafe->nominalExit) && (dataHandling.failSafe->saveFilePath[0] != '\0');
	if (readExisting) {
		DebugLog("Existing SaveFile found at§", dataHandling.failSafe->saveFilePath);
		ReadSave(dataHandling.failSafe->saveFilePath);
	}
	if (USE_DEFAULT_VALUES & (dataHandling.saveFile == NULL)) {
		CreateSave(SAVEFILE_NAME);
	}
	if (CALIBRATION_METHOD != NONE) {
		if (dataHandling.failSafe != NULL) {
			if (dataHandling.failSafe->calPath[0] != '\0') {
				DebugLog("Reading Calibration?");
				if (ReadCalibration(dataHandling.failSafe->calPath)) DebugLog("Calibration read");
			}
		}
		if ((dataHandling.calibration == NULL) & USE_DEFAULT_VALUES) {
			DebugLog("Creating new Calibration:");
			if (CreateCalibration(CALIBRATION_NAME)) DebugLog("Calibration created_");
		}
	}
	else DebugLog("Skipping Calibration");

	DebugLog("Executing Misc tasks:");
	_CreateFrameLookUp_();
	_SetPositions_();
	_CreateHandler_();
	DebugLog("Creating Buffer?");
	if (CreateBuffer()) DebugLog("Buffer created");
	if (USE_DEFAULT_VALUES)	LoadPort();
	DebugLog("Misc tasks completed_");
	DebugLog("Setup done_");
	return 1;
}

int UpdateAll()
{
	DebugLog("Updating:");
	int out = 0;
	out += UpdateBuffer();
	out += UpdateFiles();
	DebugLog("Update done_");
	return out;
}

int UpdateBuffer()
{
	DebugLog("Updating Buffer");
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitiated DataHandling");
		return 0;
	}
	int out = 0, amount = 0;
	if (FormPackets() > 0) {
		amount = Send();
		if (amount < 0)	out--;
#if (!TRANSMISSION_DEBUG)
		else if (amount > 0) {
			_ShiftArray_(dataHandling.buffer->outPackets, PACKET_LENGTH, PACKET_BUFFER_LENGTH, -(amount / (int)PACKET_LENGTH));
		}
#endif
	}
	amount = Receive();
	if (amount > 0)
	{
#if (TRANSMISSION_DEBUG)
		_ShiftArray_(dataHandling.buffer->outPackets, PACKET_LENGTH, PACKET_BUFFER_LENGTH, -(amount / (int)PACKET_LENGTH));
#endif
		if (FormFrames() > 0) {
			for (DataFrame temp = GetInFrame(); !FrameIsEmpty(temp); temp = GetInFrame()) AddSaveFrame(temp);
		}
		else out--;
	}
	return out;
}

int UpdateFiles()
{
	DebugLog("Updating Files");
	int out = 0;
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile");
		out--;
	}
	else if (WriteSave() == -1) {
		out--;
	}
	if (dataHandling.failSafe == NULL) {
		DebugLog("!Could not find FailSafe");
		out--;
	}
	else if (!WriteFailSafe()) {
		out--;
	}
	if (dataHandling.calibration == NULL) {
		if (CALIBRATION_METHOD != NONE) {
			DebugLog("!Could not find Calibration");
			out--;
		}
	}
	else if (!WriteCalibration()) {
		out--;
	}
	return out;
}

DataHandlingHub* GetDataHandling()
{
	return &dataHandling;
}

FailSafe* GetFailSafe()
{
	if (dataHandling.failSafe == NULL) CreateFailSafe();
	return dataHandling.failSafe;
}

float MapSensorValue(int id, long long value)
{
	if (CALIBRATION_METHOD == NONE) return (float)value;
	if ((dataHandling.calibration != NULL) & (id >= 0) & (id < SENSOR_AMOUNT) || (CALIBRATION_POINTS < 2)) {
		if (!dataHandling.calibration->sorted) _SortCalibration_();
		CalibrationPoint points[CALIBRATION_POINTS];
		float out = 0.0f;
		int i, j;
		for (i = 0; i < CALIBRATION_POINTS; i++) {
			//reading points
			points[i] = ReadPoint(id, i);
			//trivial solution
			if ((points[i].digital == value) & (points[i].valid)) return points[i].analog;
			
		}
		//test for insufficient calibration points
		if (!(points[0].valid & points[1].valid)) return out;
		//linear interpolation
		if ((CALIBRATION_METHOD == LINEAR) & (CALIBRATION_POINTS > 1)) {
			float a = 0.0f;
			for (i = 0, j = 1; j < CALIBRATION_POINTS - 1; i++, j++) {
				if (value < points[j].digital) {
					for (; i > 0; i--) {
						if (points[i].digital < value) break;
					}
					break;
				}
				if (!points[j + 1].valid) break;
			}
			if (points[i].digital == points[j].digital) return out;
			a = (float)(value - points[i].digital) / (float)(points[j].digital - points[i].digital);
			out = points[i].analog + (points[j].analog - points[i].analog) * a;
		}
		//not implemented, quadratic regression
		else if ((CALIBRATION_METHOD == QUADRATIC) & (CALIBRATION_POINTS == 3)) {
			//test for insufficient calibration points
			if (!points[2].valid) return out;
			float a = 0.0f, b = 0.0f, c = 0.0f;
			out = a * (value * value) + b * value + c;
		}
		return out;
	}
	return 0.0f;
}

CalibrationPoint ReadPoint(int id, int number)
{
	static CalibrationPoint invalidPoint = { 0, 0.0f, 0 };
	if (dataHandling.calibration == NULL)
	{
		DebugLog("!Calibration not found");		
		return invalidPoint;
	}
	if ((id >= 0) & (id < SENSOR_AMOUNT) & (number >= 0) & (number < CALIBRATION_POINTS)) 
		return dataHandling.calibration->points[id][number];
	else { 
		DebugLog("!ID# or number# out of range", id, number);
		return invalidPoint;
	}
}

void WritePoint(int id, int number, long long digitalValue, float analogValue)
{
	CalibrationPoint point = { digitalValue, analogValue , 1 };
	AddPoint(id, number, point);
}

void AddPoint(int id, int number, CalibrationPoint point)
{
	if (dataHandling.calibration != NULL) {
		if ((id >= 0) & (id < SENSOR_AMOUNT) & (number >= 0) & (number < CALIBRATION_POINTS)) {
			dataHandling.calibration->points[id][number] = point;
			dataHandling.calibration->sorted = 0;
			dataHandling.calibration->changed = 1;
		}
		else DebugLog("!ID# or number# out of range", id, number);
	}
	else DebugLog("!Calibration not found");
}

int CreateCalibration(const char* path)
{
	if (dataHandling.calibration != NULL) {
		free(dataHandling.calibration);
		dataHandling.calibration = NULL;
	}
	SensorCalibration* new = malloc(sizeof(SensorCalibration));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*) new;
	for (int i = 0; i < sizeof(SensorCalibration); i++) bytePtr[i] = 0;
	new->version = CALIBRATION_VERSION;
	new->dateTime = time(NULL);
	new->changed = 1;
	strcpy(new->calibrationFilePath, path);
	if (dataHandling.failSafe != NULL) {
		strcpy(dataHandling.failSafe->calPath, path);
		dataHandling.failSafe->changed = 1;
	}
	dataHandling.calibration = new;
	return 1;
}

#define CALIBRATION_HEADER_STRING "MEEGA Sensor-Calibration\n"
#define CALIBRATION_VERSION_STRING "Version: %f;\n"
#define CALIBRATION_TIME_STRING "Datetime: %lli;\n"
#define CALIBRATION_POINT_HEADER_STRING "CalibrationPoints:\n"
#define CALIBRATION_SENSOR_START_STRING "%02i: {"
#define CALIBRATION_SENSOR_END_STRING "}\n"
#define CALIBRATION_POINT_STRING "{%lli,%f,%c}"

int ReadCalibration(const char* path)
{
	DebugLog("Reading Calibration:");
	FILE* file;
	int i, j, sensor, defaultpath = 0, error = 0;
	if (path == NULL || path[0] == '\0')
		if (USE_DEFAULT_VALUES) {
			file = fopen(CALIBRATION_NAME, "rb");
			defaultpath = 1;
		}
		else {
			DebugLog("!Invalid path passed to ReadCalibration()");
			return 0;
		}
	else {
		file = fopen(path, "rb");
	}
	if (file == NULL) {
		DebugLog("!Calibration could not be opened_");
		return 0;
	}
	if (defaultpath) CreateCalibration(CALIBRATION_NAME);
	else CreateCalibration(path);
	if (dataHandling.calibration == NULL) {
		DebugLog("!Calibration could not be created_");
		return 0;
	}
	DebugLog("Calibration found@", dataHandling.calibration);
	SensorCalibration* calibration = dataHandling.calibration;
	if (fscanf(file, CALIBRATION_HEADER_STRING) != EOF) {
		if (fscanf(file, CALIBRATION_VERSION_STRING, &calibration->version) != EOF) {
			if (calibration->version == CALIBRATION_VERSION) {
				if (fscanf(file, CALIBRATION_TIME_STRING, &calibration->dateTime) != EOF) {
					if (fscanf(file, CALIBRATION_POINT_HEADER_STRING) != EOF) {
						for (i = 0; i < SENSOR_AMOUNT; i++) {
							if (fscanf(file, CALIBRATION_SENSOR_START_STRING, &sensor) != EOF) {
								if (sensor != i) {
									error = 1;
									break;
								}
								for (j = 0; j < CALIBRATION_POINTS; j++) {
									if (fscanf(file, CALIBRATION_POINT_STRING, &calibration->points[sensor][j].digital, &calibration->points[sensor][j].analog, &calibration->points[sensor][j].valid) == EOF) {
										error = 1;
										break;
									}
								}
								if (fscanf(file, CALIBRATION_SENSOR_END_STRING) == EOF) {
									error = 1;
									break;
								}
							}
							else {
								error = 1;
								break;
							}
						}
						if (!error) {
							DebugLog("Calibration read from§_", path);
							return 1;
						}
					}
				}
			}
		}
	}
	DebugLog("!Calibration File could not be parsed_");
	return 0;
}

int WriteCalibration()
{
	//DebugLog("Writing Calibration to file:");
	if (dataHandling.calibration == NULL) {
		DebugLog("!Could not find Calibration");
		return 0;
	}
	//DebugLog("Calibration found@", dataHandling.calibration);
	SensorCalibration calibration = *dataHandling.calibration;
	if (calibration.changed) {
		FILE* file = fopen(calibration.calibrationFilePath, "w");
		if (file != NULL) {
			fprintf(file, CALIBRATION_VERSION_STRING, calibration.version);
			fprintf(file, CALIBRATION_TIME_STRING, calibration.dateTime);
			fprintf(file, CALIBRATION_POINT_HEADER_STRING);
			for (int i = 0; i < SENSOR_AMOUNT; i++) {
				fprintf(file, CALIBRATION_SENSOR_START_STRING, i);
				for (int j = 0; j < CALIBRATION_POINTS; j++) {
					fprintf(file, CALIBRATION_POINT_STRING, calibration.points[i][j].digital, calibration.points[i][j].analog, calibration.points[i][j].valid);
				}
				fprintf(file, CALIBRATION_SENSOR_END_STRING);
			}
			fclose(file);
			//DebugLog("Calibration written at§_", calibration.calibrationFilePath);
			return 1;
		}
		else {
			DebugLog("!Could not open Calibration file");
			return 0;
		}
	else {
		file = fopen(path, "rb");
	}
	//DebugLog("Write unneccessary_");
	return 1;
}

DataFrame CreateFrame()
{
	DataFrame temp = EmptyFrame();
	temp.sync = _GetSync_();
	return temp;
}

DataFrame CreateTC()
{
	DataFrame temp = EmptyFrame();
	temp.sync = _GetSync_();
	FrameSetFlag(&temp, TeleCommand);
	return temp;
}

DataFrame EmptyFrame()
{
	DataFrame temp = { 0 };
	byte* bytePtr = (byte*)&temp;
	for (int i = 0; i < sizeof(DataFrame); i++) bytePtr[i] = 0;
	temp.start = -1;
	FrameSetFlag(&temp, Source);
	return temp;
}

DataFrame EmptyTC() 
{
	DataFrame temp = EmptyFrame();
	FrameSetFlag(&temp, TeleCommand);
	return temp;
}

long long WriteFrame(DataFrame* frame, int id, long long value)
{
	if (frame == NULL) {
		DebugLog("!Invalid Frame-pointer");
		return 0;
	}
	if (dataHandling.frameLookUp == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
	int TC = FrameIsTC(*frame);
	int index;
	int length;
	int valid = 0;
	if (id >= 0) {
		if (TC) {
			if (id < TELECOMMAND_AMOUNT) {
				index = dataHandling.frameLookUp->telecommand_Pos_Len[id][0];
				length = dataHandling.frameLookUp->telecommand_Pos_Len[id][1];
				valid = 1;
			}
		}
		else {
			if (id < TELEMETRY_AMOUNT) {
				index = dataHandling.frameLookUp->telemetry_Pos_Len[id][0];
				length = dataHandling.frameLookUp->telemetry_Pos_Len[id][1];
				valid = 1;
			}
		}
	}
	if (!valid) {
		DebugLog("!ID# out of range", id);
		return 0;
	}
	long long maxValue = 1ll << length;
	if (value < 0 || value >= maxValue) {
		DebugLog("!Value# out of writable range at ID#", value, id);
		return 0;
	}
	int offset = index % 8;
	long long old_value = 0;
	long long workspace = 0;
	long long return_value = 0;
	long long new_value = value;
	byte* bytePtr = (byte*) &old_value;
	for (int i = 0; i < ((length / 8) + (offset != 0 ) + ((length % 8) != 0)); i++) {
		if (index / 8 + i == DATA_LENGTH) break;
		bytePtr[i] = frame->data[index / 8 + i];
	}
	workspace = old_value;
	old_value >>= offset;
	old_value %= 1ll << length;
	return_value = old_value;
	new_value <<= offset;
	old_value <<= offset;
	new_value = workspace - old_value + new_value;
	bytePtr = (byte*) &new_value;
	for (int i = 0; i < ((length / 8) + (offset != 0) + ((length % 8) != 0)); i++) {
		if (index / 8 + i == DATA_LENGTH) break;
		frame->data[index / 8 + i] = bytePtr[i];
	}
	frame->chksm = CalculateChecksum(*frame);
	return return_value;
}

long long ReadFrame(DataFrame frame, int id)
{
	if (dataHandling.frameLookUp == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
	int TC = FrameIsTC(frame);
	if ((TC & (id >= TELECOMMAND_AMOUNT)) || id >= TELEMETRY_AMOUNT) {
		
	}
	int index;
	long long length;
	int valid = 0;
	if (id >= 0) {
		if (TC) {
			if (id < TELECOMMAND_AMOUNT) {
				index = dataHandling.frameLookUp->telecommand_Pos_Len[id][0];
				length = dataHandling.frameLookUp->telecommand_Pos_Len[id][1];
				valid = 1;
			}
		}
		else {
			if (id < TELEMETRY_AMOUNT) {
				index = dataHandling.frameLookUp->telemetry_Pos_Len[id][0];
				length = dataHandling.frameLookUp->telemetry_Pos_Len[id][1];
				valid = 1;
			}
		}
	}
	if (!valid) {
		DebugLog("!ID# out of range", id);
		return 0;
	}
	int offset = index % 8;
	long long value = 0;
	byte* bytePtr = (byte*) &value;
	for (int i = 0; i < ((length / 8) + (offset != 0) + ((length % 8) != 0)); i++) {
		if (index / 8 + i == DATA_LENGTH) break;
		bytePtr[i] = frame.data[index / 8 + i];
	}
	value >>= offset;
	value %= 1ll << length;
	return value;
}

int FrameIsEmpty(DataFrame frame) 
{
	return frame.sync == 0;
}

int FrameIsTC(DataFrame frame)
{
	return FrameHasFlag(frame, TeleCommand);
}

int FrameHasFlag(DataFrame frame, int id)
{
	if (id >= 8 || id < 0) return 0;
	return (frame.flag >> id) % (1 << (id + 1));
}

void FrameSetFlag(DataFrame* frame, int id)
{
	if (frame == NULL || id >= 8 || id < 0) return;
	if ((frame->flag >> id) % (1 << (id + 1)));
	else frame->flag += 1 << id;
	if (id == Partial || id == Biterror) {
		FrameRemoveFlag(frame, OK);
		FrameRemoveFlag(frame, Source);
	}
	else if (id == OK) FrameRemoveFlag(frame, Source);
	return;
}

void FrameRemoveFlag(DataFrame* frame, int id)
{
	if (frame == NULL || id >= 8 || id < 0) return;
	if ((frame->flag >> id) % (1 << (id + 1))) frame->flag -= 1 << id;
	return;
}

DataPacket CreatePacket(SYNC_TYPE sync)
{
	DataPacket out = { 0 };
	byte* bytePtr = (byte*) &out;
	for (int i = 0; i < sizeof(out); i++)
		bytePtr[i] = 0;
	out.sync = sync;
	out.start = -1;
	return out;
}

DataPacket EmptyPacket()
{
	return CreatePacket(0);
}

int PacketIsEmpty(DataPacket packet)
{
	return packet.sync == 0;
}

int CreateBuffer()
{
	if (dataHandling.buffer != NULL) {
		free(dataHandling.buffer);
		dataHandling.buffer = NULL;
	}
	DataBuffer* new = malloc(sizeof(DataBuffer));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*) new;
	for (int i = 0; i < sizeof(DataBuffer); i++) bytePtr[i] = 0;
	dataHandling.buffer = new;
	return 1;
}

int EncodePackets()
{
	//Deprecated
	return 1;
}

int DecodePackets()
{
	//Deprecated
	return 0;
}

int FormPackets()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
	DataPacket currentPacket; 
	DataFrame currentFrame = GetOutFrame();
	int number = 0;
	int payloadIndex, dataIndex;
	byte id, tc;
	for (; !FrameIsEmpty(currentFrame); currentFrame = GetOutFrame()) {
		dataIndex = 0;
		tc = FrameIsTC(currentFrame);
		for (id = 0; id < (1 << MSG_ID_LEN); id++, number++) {
			currentPacket = CreatePacket(currentFrame.sync);
			currentPacket.msg = _ToMSG_(tc, id);
			for (payloadIndex = 0; payloadIndex < PAYLOAD_LENGTH; payloadIndex++, dataIndex++) {
				if (dataIndex < DATA_LENGTH) currentPacket.payload[payloadIndex] = currentFrame.data[dataIndex];
				else currentPacket.payload[payloadIndex] = 0;
			}
			currentPacket.chksm = currentFrame.chksm;
			CalculateCRC(&currentPacket);
			AddOutPacket(currentPacket);
			if (dataIndex >= DATA_LENGTH) break;
		}
	}
	return number;
}

int FormFrames()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
	DataPacket currentPacket = GetInPacket();
	DataFrame* framePtr = dataHandling.buffer->inFrames;
	int number = 0;
	int payloadIndex = 0, dataIndex = 0;
	byte id, type, foundMatch, faulty;
	for (; !PacketIsEmpty(currentPacket); currentPacket = GetInPacket(), number++) {
		faulty = 0, foundMatch = 0;
		if (CalculateCRC(&currentPacket)) faulty = 1;
		_FromMSG_(currentPacket.msg, &type, &id);
		if (framePtr->sync != currentPacket.sync) {
			for (framePtr = dataHandling.buffer->inFrames; framePtr != dataHandling.buffer->outFrames; framePtr++) {
				if ((framePtr->sync == currentPacket.sync) & (framePtr->chksm == currentPacket.chksm)) {
					foundMatch = 1;
					break;
				}
			}
			if (!foundMatch) {
				framePtr = dataHandling.buffer->inFrames + AddInFrame(CreateFrame());
				framePtr->sync = currentPacket.sync;
				if (type) FrameSetFlag(framePtr, TeleCommand);
				FrameSetFlag(framePtr, OK);
				framePtr->chksm = currentPacket.chksm;
			}
		}
		dataIndex = id * PAYLOAD_LENGTH;
		for (payloadIndex = 0; payloadIndex < PAYLOAD_LENGTH; payloadIndex++, dataIndex++) {
			if (dataIndex < DATA_LENGTH) {
				if (framePtr->data[dataIndex] != 0) break;
				framePtr->data[dataIndex] = currentPacket.payload[payloadIndex];
			}
		}
		if (faulty) FrameSetFlag(framePtr, Biterror);
	}
	return number;
}

DataPacket GetInPacket()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return EmptyPacket();
	}
	DataPacket temp = EmptyPacket();
	for (int i = PACKET_BUFFER_LENGTH; i > 0; i--) {
		temp = dataHandling.buffer->inPackets[i - 1];
		if (!PacketIsEmpty(temp)) {
			dataHandling.buffer->inPackets[i - 1] = EmptyPacket();
			break;
		}
	}
	return temp;
}

DataFrame GetOutFrame()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return EmptyFrame();
	}
	DataFrame temp = EmptyFrame();
	for (int i = BUFFER_LENGTH; i > 0; i--) {
		temp = dataHandling.buffer->outFrames[i - 1];
		if (!FrameIsEmpty(temp)) {
			dataHandling.buffer->outFrames[i - 1] = EmptyFrame();
			break;
		}
	}
	return temp;
}

DataFrame GetInFrame()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return EmptyFrame();
	}
	DataFrame temp = EmptyFrame();
	for (int i = BUFFER_LENGTH; i > 0; i--) {
		temp = dataHandling.buffer->inFrames[i - 1];
		if (!FrameIsEmpty(temp)) {
			dataHandling.buffer->inFrames[i - 1] = EmptyFrame();
			break;
		}
	}
	if (temp.chksm != CalculateChecksum(temp)) FrameSetFlag(&temp, Partial);
	else FrameSetFlag(&temp, OK);
	return temp;
}

int AddOutPacket(DataPacket data)
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int i = 0;
	for (; i <= PACKET_BUFFER_LENGTH; i++) {
		if (PacketIsEmpty(dataHandling.buffer->outPackets[i])) {
			dataHandling.buffer->outPackets[i] = data;
			break;
		}
	}
	return i;
}

int AddOutFrame(DataFrame frame)
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int i = 0;
	for (; i <= BUFFER_LENGTH; i++) {
		if (FrameIsEmpty(dataHandling.buffer->outFrames[i])) {
			dataHandling.buffer->outFrames[i] = frame;
			break;
		}
	}
	return i;
}

int AddInFrame(DataFrame frame)
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int i = 0;
	for (; i <= BUFFER_LENGTH; i++) {
		if (FrameIsEmpty(dataHandling.buffer->inFrames[i])) {
			dataHandling.buffer->inFrames[i] = frame;
			break;
		}
	}
	return i;
}

#define FAILSAFE_TITLE_STRING "MEEGA FailSafe\n\n"
#define FAILSAFE_VERSION_STRING "Version: %f;\n"
#define FAILSAFE_DATE_STRING "Datetime: %lli;\n"
#define FAILSAFE_SAVEFILE_STRING "Savefile: %s;\n"
#define FAILSAFE_CALIBRATION_STRING "Calibrationfile: %s;\n"
#define FAILSAFE_COMPLETE_STRING "Complete: %c;\n"
#define FAILSAFE_NOMINAL_STRING "Nominal Exit: %c;\n"

int CreateFailSafe() 
{
	if (dataHandling.failSafe != NULL) {
		free(dataHandling.failSafe);
		dataHandling.failSafe = NULL;
	}
	FailSafe* new = malloc(sizeof(FailSafe));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*) new;
	for (int i = 0; i < sizeof(FailSafe); i++) bytePtr[i] = 0;
	new->nominalExit = 0;
	new->dateTime = time(NULL);
	new->version = FAILSAFE_VERSION;
	if (USE_DEFAULT_VALUES) {
		strcpy(new->saveFilePath, SAVEFILE_NAME);
		strcpy(new->comPath, DEFAULTCOMPATH);
		strcpy(new->calPath, CALIBRATION_NAME);
	}
	FILE* file;
	file = fopen(FAILSAFE_NAME, "w");
	if (file != NULL) {
		fprintf(file, FAILSAFE_TITLE_STRING);
		fprintf(file, FAILSAFE_VERSION_STRING, new->version);
		fprintf(file, FAILSAFE_DATE_STRING, new->dateTime);
		if (USE_DEFAULT_VALUES) fprintf(file, FAILSAFE_SAVEFILE_STRING, new->saveFilePath);
		else fprintf(file, FAILSAFE_SAVEFILE_STRING, " ");
		if ((CALIBRATION_METHOD != NONE) & USE_DEFAULT_VALUES) fprintf(file, FAILSAFE_CALIBRATION_STRING, new->calPath);
		else fprintf(file, FAILSAFE_CALIBRATION_STRING, " ");
		fprintf(file, FAILSAFE_COMPLETE_STRING, (new->complete) ? 'y' : 'n');
		fprintf(file, FAILSAFE_NOMINAL_STRING, (new->nominalExit)? 'y' : 'n');
		fclose(file);
	}
	else DebugLog("!Could not create FailSafe file");
	dataHandling.failSafe = new;
	return 1;
}

int ReadFailSafe()
{
	DebugLog("Reading FailSafe:");
	if (dataHandling.failSafe != NULL) {
		DebugLog("Freeing FailSafe?");
		free(dataHandling.failSafe);
		dataHandling.failSafe = NULL;
		DebugLog("FailSafe freed");
	}
	FILE* file = NULL;
	FailSafe* this = malloc(sizeof(FailSafe));
	if (this == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	dataHandling.failSafe = this;
	byte* bytePtr = (byte*) this;
	for (int i = 0; i < sizeof(FailSafe); i++) bytePtr[i] = 0;
	float ReadVersion = 0.0f;
	this->version = FAILSAFE_VERSION;
	file = fopen(FAILSAFE_NAME, "r");
	if (file != NULL) {
		if (fscanf(file, FAILSAFE_TITLE_STRING) != EOF) {
			if (fscanf(file, FAILSAFE_VERSION_STRING, &ReadVersion) != EOF) {
				if (ReadVersion == this->version) {
					//Newest FileReader here:
					char ReadChar;
					int length = PATH_LENGTH;
					if (fscanf(file, FAILSAFE_DATE_STRING, &this->dateTime) != EOF) {
						if (fscanf(file, FAILSAFE_SAVEFILE_STRING, &this->saveFilePath) != EOF) {
							if (fscanf(file, FAILSAFE_CALIBRATION_STRING, &this->calPath) != EOF) {
								length = 1;
								if (fscanf(file, FAILSAFE_COMPLETE_STRING, &ReadChar) != EOF) {
									this->complete = (ReadChar == 'y') ? 1 : 0;
									if (fscanf(file, FAILSAFE_NOMINAL_STRING, &ReadChar) != EOF) {
										this->nominalExit = (ReadChar == 'y') ? 1 : 0;
										DebugLog("Failsafe read@_", this);
										fclose(file);
										return 1;
									}
								}
							}
						}
					}
					DebugLog("!Could not parse FailSafe file");
					fclose(file);
				}
				else if (ReadVersion == 1.0f) {
					//Older FileReader:
					char ReadChar;
					int length = PATH_LENGTH;
					if (fscanf(file, FAILSAFE_DATE_STRING, &this->dateTime) != EOF) {
						if (fscanf(file, FAILSAFE_SAVEFILE_STRING, &this->saveFilePath) != EOF) {
							length = 1;
							if (fscanf(file, FAILSAFE_COMPLETE_STRING, &ReadChar) != EOF) {
								this->complete = (ReadChar == 'y') ? 1 : 0;
								if (fscanf(file, FAILSAFE_NOMINAL_STRING, &ReadChar) != EOF) {
									this->nominalExit = (ReadChar == 'y') ? 1 : 0;
									if (fscanf(file, "Mode: %c;\n", &ReadChar) != EOF) {
										if (fscanf(file, "Connection: %c;\n", &ReadChar) != EOF) {
											if (fscanf(file, "Language: %c;", &ReadChar) != EOF) {
												DebugLog("Failsafe read@_", this);
												fclose(file);
												return 1;
											}
										}
									}
								}
							}
						}
					}
					DebugLog("!Could not parse FailSafe file");
					fclose(file);
				}
				else if (ReadVersion = 0.0f) {
					//Older FileReader:
				}
			}
		}
	}
	else DebugLog("!Could not open FailSafe file");
	DebugLog("Failsafe reading failed_");
	return 0;
}

int WriteFailSafe()
{
	//DebugLog("Writing FailSafe to file:");
	if (dataHandling.failSafe == NULL) {
		DebugLog("!Could not find FailSafe_");
		return 0;
	}
	//DebugLog("FailSafe found@", dataHandling.failSafe);
	FailSafe* failsafe = dataHandling.failSafe;
	if (!failsafe->changed) {
		//DebugLog("FailSafe write unneccessary_");
		return 1;
	}
	FILE* file;
	file = fopen(FAILSAFE_NAME, "w");
	if (file != NULL) {
		fprintf(file, FAILSAFE_TITLE_STRING);
		fprintf(file, FAILSAFE_VERSION_STRING, failsafe->version);
		fprintf(file, FAILSAFE_DATE_STRING, failsafe->dateTime);
		fprintf(file, FAILSAFE_SAVEFILE_STRING, failsafe->saveFilePath);
		if (CALIBRATION_METHOD != NONE) fprintf(file, FAILSAFE_CALIBRATION_STRING, failsafe->calPath);
		else fprintf(file, FAILSAFE_CALIBRATION_STRING, " ");
		fprintf(file, FAILSAFE_COMPLETE_STRING, (failsafe->complete) ? 'y' : 'n');
		fprintf(file, FAILSAFE_NOMINAL_STRING, (failsafe->nominalExit) ? 'y' : 'n');
		fclose(file);
		failsafe->changed = 0;
		//DebugLog("FailSafe written at§_", FAILSAFE_NAME);
		return 1;
	}
	else DebugLog("!Could not open FailSafe file");
	return 0;
}

int VirtualSave()
{
	if (dataHandling.saveFile != NULL) {
		//DebugLog("Found existing SaveFile");
		CloseSave();
		free(dataHandling.saveFile);
		dataHandling.saveFile = NULL;
	}
	SaveFile* new = malloc(sizeof(SaveFile));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	byte* bytePtr = (byte*) new;
	for (int i = 0; i < sizeof(SaveFile); i++) bytePtr[i] = 0;
	new->dateTime = time(NULL);
	new->savedAmount = -1;
	new->version = SAVEFILE_VERSION;
	new->currentTC = EmptyTC();
	dataHandling.saveFile = new;
	return 1;
}

int CreateSave(const char path[])
{
	DebugLog("Creating SaveFile:");
	VirtualSave();
	if (dataHandling.saveFile == NULL) {
		DebugLog("SaveFile creation failed_");
		return 0;
	}
	dataHandling.saveFile->savedAmount = 0;
	FILE* file = NULL;
	if (path != NULL) {
		file = fopen(path, "wb");
		strcpy(dataHandling.saveFile->saveFilePath, path);
	}
	if (file != NULL) {
		fprintf(file, "%f", SAVEFILE_VERSION);
		fwrite(&(dataHandling.saveFile->dateTime), sizeof(dataHandling.saveFile->dateTime), 1, file);
		fclose(file);
	}
	else {
		DebugLog("!Could not create SaveFile file");
		DebugLog("SaveFile creation failed_");
		free(dataHandling.saveFile);
		dataHandling.saveFile = NULL;
		return 0;
	}
	if (dataHandling.failSafe != NULL) {
		strcpy(dataHandling.failSafe->saveFilePath, path);
		dataHandling.failSafe->complete = 0;
		dataHandling.failSafe->changed = 1;
	}
	else DebugLog("!Could not find FailSafe");
	DebugLog("SaveFile created@_", dataHandling.saveFile);
	return 1;
}

int CheckSave()
{
	/* -----------------------------------------------------REWRITE DUE
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile");
		return 0;
	}
	SaveFrame* overhead = GetSaveFrame(dataHandling.saveFile->savedAmount);
	if (overhead != NULL) {
		if (overhead->previousFrame != NULL) overhead->previousFrame->nextFrame = NULL;
		dataHandling.saveFile->lastFrame = overhead->previousFrame;
	}
	ReadSave(dataHandling.saveFile->saveFilePath);
	if (overhead != NULL) {
		if (dataHandling.saveFile->frameAmount != 0) {
			if (GetSaveFrame(-1)->data.sync == overhead->data.sync) return 1;
			dataHandling.saveFile->lastFrame->nextFrame = overhead;
			overhead->previousFrame = dataHandling.saveFile->lastFrame;
		}
		else {
			dataHandling.saveFile->firstFrame = overhead;
			overhead->previousFrame = NULL;
		}
	}
	overhead = dataHandling.saveFile->firstFrame;
	dataHandling.saveFile->frameAmount = 0;
	if (overhead != NULL) {
		dataHandling.saveFile->frameAmount++;
		while (overhead->nextFrame != NULL) overhead = overhead->nextFrame, dataHandling.saveFile->frameAmount++;
		dataHandling.saveFile->lastFrame = overhead;
	}
	*/
	return 1;
}

int ReadSave(const char path[])
{
	DebugLog("Reading SaveFile:");
	FILE* file;
	if (path == NULL || path[0] == '\0')
		if (USE_DEFAULT_VALUES) file = fopen(SAVEFILE_NAME, "rb");
		else {
			DebugLog("!Invalid path passed to ReadSave()");
			return 0;
		}
	else file = fopen(path, "rb");
	if (file == NULL) {
		DebugLog("!SaveFile could not be opened_");
		return 0;
	}
	DebugLog("Opened SaveFile");
	if (!VirtualSave()) return 0;
	byte* writePtr = (byte*) &dataHandling.saveFile->dateTime;
	int i = 0;
	if (fscanf(file, "%f", &dataHandling.saveFile->version) == EOF) {
		DebugLog("!Unexpected End of File");
		return 0;
	}
	for (; i < sizeof(dataHandling.saveFile->dateTime); i++, writePtr++) {
		if (fscanf(file, "%c", writePtr) == EOF) {
			DebugLog("!Unexpected End of File");
			return 0;
		}
	}
	for (i = 0; 1; i++){
		if (i % sizeof(DataFrame) == 0) {				
			AddSaveFrame(CreateFrame(0));
			writePtr = (byte*)&dataHandling.saveFile->lastFrame->data;
		}
		if (fscanf(file, "%c", writePtr) == EOF) break;
		writePtr++;
	}
	if (i++ % sizeof(DataFrame) != 0) DebugLog("!Read incomplete Frame");
	for (SaveFrame* current = dataHandling.saveFile->firstFrame; current != NULL; current = current->nextFrame) {
		if (CalculateChecksum(current->data) != current->data.chksm) FrameSetFlag(&current->data, Partial);
	}
	DebugLog("Amount of Frames read#_", dataHandling.saveFile->frameAmount);
	dataHandling.saveFile->savedAmount = dataHandling.saveFile->frameAmount;
	return 1;
}

int WriteSave()
{
	//DebugLog("Writing SaveFile:");
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile");
		return 0;
	}
	//DebugLog("SaveFile found@", dataHandling.saveFile);
	if (dataHandling.saveFile->savedAmount == -1 || dataHandling.saveFile->savedAmount >= dataHandling.saveFile->frameAmount) {
		//DebugLog("SaveFile write unneccessary_");
		return 0;
	}
	FILE* file = NULL;
	if (dataHandling.saveFile->saveFilePath[0] != '\0') {
		file = fopen(dataHandling.saveFile->saveFilePath, "ab");
		if (file != NULL) {
			GetSaveFrame(dataHandling.saveFile->savedAmount - dataHandling.saveFile->unloadedAmount);
			SaveFrame* current = currentFrame;
			byte* bytePtr = NULL;
			int number = 0;
			while (current != NULL) {
				bytePtr = (byte*)&(current->data);
				number += (int)fwrite(bytePtr, sizeof(DataFrame), 1, file);
				current = current->nextFrame;
				dataHandling.saveFile->savedAmount++;
			}
			fclose(file);
			if (dataHandling.saveFile->savedAmount < dataHandling.saveFile->frameAmount) DebugLog("!Could not write all frames");
			//DebugLog("SaveFile written at§_", dataHandling.saveFile->saveFilePath);
			return number;
		}
		else DebugLog("!Could not open SaveFile file");
	}
	//DebugLog("Could not write SaveFile at§_", dataHandling.saveFile->saveFilePath);
	return 0;
}

DataFrame GetSaveFrame(int index)
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return EmptyFrame();
	}
	if (dataHandling.saveFile->lastFrame == NULL) {
		DebugLog("!SaveFile is empty");
		return EmptyFrame();
	}
	SaveFrame* frame = NULL;
	if (index >= dataHandling.saveFile->frameAmount || index < 0) frame = dataHandling.saveFile->lastFrame;
	else frame = dataHandling.saveFile->firstFrame;
	for (int i = 0; i < index;) {
		if (frame == NULL) return EmptyFrame();
		if (frame->nextFrame == NULL) break;
		frame = frame->nextFrame;
		if (!FrameIsTC(frame->data)) i++;
	}
	while (FrameIsTC(frame->data)) {
		if (frame->previousFrame != NULL) frame = frame->previousFrame;
		else return EmptyFrame();
	}
	currentFrame = frame;
	return frame->data;
}

DataFrame GetNextFrame()
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return EmptyFrame();
	}
	if (currentFrame == NULL) {
		if (dataHandling.saveFile->firstFrame != NULL) {
			currentFrame = dataHandling.saveFile->firstFrame;
		}
		else return EmptyFrame();
	}
	else if (currentFrame->nextFrame != NULL) {
		currentFrame = currentFrame->nextFrame;
	}
	else return EmptyFrame();
	while (FrameIsTC(currentFrame->data)) {
		if (currentFrame->nextFrame == NULL) break;
		else currentFrame = currentFrame->nextFrame;
	}
	if (!FrameIsTC(currentFrame->data))	return currentFrame->data;
	return EmptyFrame();
}

DataFrame GetTC()
{
	DataFrame newestTC = EmptyTC();
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return newestTC;
	}
	if (dataHandling.saveFile->lastFrame == NULL) {
		DebugLog("!SaveFile is empty");
		dataHandling.saveFile->currentTC = newestTC;
		return newestTC;
	}
	SaveFrame* currentFrame = dataHandling.saveFile->lastFrame;
	for (; currentFrame->previousFrame != NULL; currentFrame = currentFrame->previousFrame) {
		if (FrameIsTC(currentFrame->data)) {
			if (!FrameIsEmpty(currentFrame->data) && FrameHasFlag(currentFrame->data, OK)) {
				newestTC = currentFrame->data;
				break;
			}
		}
	}
	if (!FrameIsEmpty(newestTC)) dataHandling.saveFile->currentTC = newestTC;
	return dataHandling.saveFile->currentTC;
}

void AddSaveFrame(DataFrame data)
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return;
	}
	SaveFrame* newFrame = malloc(sizeof(SaveFrame));
	if (newFrame == NULL) {
		DebugLog("!Memory allocation failed");
		return;
	}
	newFrame->data = data;
	newFrame->nextFrame = NULL;
	newFrame->previousFrame = NULL;
	if (dataHandling.saveFile->lastFrame == NULL) {
		dataHandling.saveFile->firstFrame = newFrame;
		dataHandling.saveFile->lastFrame = newFrame;
		dataHandling.saveFile->frameAmount = 1;
	}
	else {
		dataHandling.saveFile->lastFrame->nextFrame = newFrame;
		newFrame->previousFrame = dataHandling.saveFile->lastFrame;
		dataHandling.saveFile->lastFrame = newFrame;
		dataHandling.saveFile->frameAmount++;
	}
	return;
}

void AddFrame(DataFrame frame)
{
	AddSaveFrame(frame);
	AddOutFrame(frame);
	return;
}

void CloseSave()
{
	DebugLog("Closing SaveFile:");
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile to close");
		return;
	}
	DebugLog("Savefile found@", dataHandling.saveFile);
	DebugLog("Writing SaveFile");
	WriteSave();
	DebugLog("Emptying SaveFileFrames?");
	SaveFrame *current = dataHandling.saveFile->lastFrame, *last = dataHandling.saveFile->firstFrame, *next;
	if (current != NULL) {
		next = current->previousFrame;
		while (next != NULL) {
			free(current);
			current = next;
			next = next->previousFrame;
		}
		if (current != last) DebugLog("!Could not parse SaveFileFrames"); //Maybe try backwards?
		free(current);
	}
	DebugLog("SaveFileFrames emptied");
	dataHandling.saveFile->lastFrame = NULL;
	dataHandling.saveFile->firstFrame = NULL;
	currentFrame = NULL;
	dataHandling.saveFile->frameAmount = dataHandling.saveFile->savedAmount;
	dataHandling.saveFile->loadedAmount = 0;
	dataHandling.saveFile->currentTC = EmptyTC();
	if (dataHandling.failSafe != NULL) {
		dataHandling.failSafe->complete = 1;
		dataHandling.failSafe->changed = 1;
	}
	DebugLog("SaveFile closed_");
}

void CloseAll()
{
	DebugLog("Closing DataHandling:");
	DebugLog("Setting nominal exit?");
	if (dataHandling.failSafe != NULL) {
		dataHandling.failSafe->nominalExit = 1;
		dataHandling.failSafe->changed = 1;
		if (WriteFailSafe() != -1) DebugLog("Nominal exit set");
	}
	else DebugLog("!Could not find FailSafe");
	DebugLog("Freeing Memory?");
	if (dataHandling.buffer != NULL) free(dataHandling.buffer);
	if (dataHandling.calibration != NULL) free(dataHandling.calibration);
	if (dataHandling.failSafe != NULL) free(dataHandling.failSafe);
	if (dataHandling.frameLookUp != NULL) free(dataHandling.frameLookUp);
	if (dataHandling.handler != NULL) {
		ClosePort();
		free(dataHandling.handler);
	}
	if (dataHandling.saveFile != NULL) {
		CloseSave(dataHandling.saveFile);
		free(dataHandling.saveFile);
	}
	dataHandling.buffer = NULL;
	dataHandling.calibration = NULL;
	dataHandling.failSafe = NULL;
	dataHandling.frameLookUp = NULL;
	dataHandling.handler = NULL;
	dataHandling.saveFile = NULL;
	DebugLog("Memory freed");
	DebugLog("DataHandling closed_");
}

//Communication Functions:
int _SetPortConfig_()
{
	if ((dataHandling.handler == NULL) || (dataHandling.handler->comHandle == INVALID_HANDLE_VALUE)) {
		DebugLog("!Unitialized DataHandling or invalid serial port");
		return 0;
	}
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	dataHandling.handler->options.DCBlength = sizeof(DCB);
	COMMTIMEOUTS timeout = { MAXDWORD , MAXDWORD, COMM_TIMEOUT * CLOCKS_PER_SEC / 1000, 0, COMM_TIMEOUT * CLOCKS_PER_SEC / 1000 };
	dataHandling.handler->timeout = timeout;
	if (GetCommState(dataHandling.handler->comHandle, &(dataHandling.handler->options))) {
		dataHandling.handler->options.Parity = NOPARITY;
		dataHandling.handler->options.ByteSize = 8;
		dataHandling.handler->options.StopBits = ONESTOPBIT;
		dataHandling.handler->options.BaudRate = BAUD_RATE;
	}
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	if (tcgetattr(dataHandling.handler->comHandle, &(dataHandling.handler->options)) == 0) {
		dataHandling.handler->options.c_iflag = 0;
		dataHandling.handler->options.c_cflag = CS8 | CLOCAL | CREAD;
		dataHandling.handler->options.c_oflag = 0;
		dataHandling.handler->options.c_lflag = 0;
		cfsetispeed(&dataHandling.handler->options, BAUD_RATE);
		cfsetospeed(&dataHandling.handler->options, BAUD_RATE);
		dataHandling.handler->timeout = COMM_TIMEOUT * CLOCKS_PER_SEC / 1000;
	}
#else
	if (0);
#endif
	else {
		DebugLog("!Could not retrieve CommState of serial Port");
		return 0;
	}
	return 1;
}

int LoadPort()
{
	DebugLog("Opening CommPort:");
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling_");
		return 0;
	}
#if (TRANSMISSION_DEBUG)
	DebugLog("Opened CommPort_");
	return 1;
#elif (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	dataHandling.handler->comHandle = CreateFileA(dataHandling.handler->comPath, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	dataHandling.handler->comHandle = open(dataHandling.handler->comPath, O_RDWR | O_NOCTTY | O_NDELAY);
#endif
	if (dataHandling.handler->comHandle != INVALID_HANDLE_VALUE) {
		if (_SetPortConfig_()) {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
			if (SetCommState(dataHandling.handler->comHandle, &(dataHandling.handler->options)) && SetCommTimeouts(dataHandling.handler->comHandle, &dataHandling.handler->timeout)) {
				DebugLog("Opened CommPort_");
				dataHandling.handler->valid = 1;
				return 1;
			}
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
			tcflush(dataHandling.handler->comHandle, TCIOFLUSH);
			if (tcsetattr(dataHandling.handler->comHandle, TCSANOW, &(dataHandling.handler->options)) == 0) {
				DebugLog("Opened CommPort_");
				dataHandling.handler->valid = 1;
				return 1;
			}
#else
			if (0);
#endif
			else DebugLog("!Could not set CommState of serial Port, Error#_", errno);
		}
	}
	else DebugLog("!Could not open CommPort, Error#_", errno);
	return 0;
}

void ClosePort() {
	DebugLog("Closing CommPort:");
	if (!PortIsOpen()) {
		DebugLog("No opened CommPort found_");
		return;
	}
#if (TRANSMISSION_DEBUG)
	if (0) {
#elif (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	if (!CloseHandle(dataHandling.handler->comHandle)) {
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	if (!close(dataHandling.handler->comHandle)) {
#else
	if (0) {
#endif
		DebugLog("!Could not close CommPort_");
	}
	else DebugLog("CommPort closed_");
}

int PortIsOpen() {
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
#if (TRANSMISSION_DEBUG)
	return 1;
#endif
	return dataHandling.handler->comHandle != INVALID_HANDLE_VALUE && dataHandling.handler->valid;
}

int Send()
{
	if (dataHandling.handler == NULL || dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	if (!PortIsOpen()) {
		DebugLog("!CommPort not ready");
		return -1;
	}
	int number = 0, amount = 0;
	for (; amount < PACKET_BUFFER_LENGTH; amount++) if (PacketIsEmpty(dataHandling.buffer->outPackets[amount])) break;
	amount *= PACKET_LENGTH;
	
#if (TRANSMISSION_DEBUG)
	if (1) {
		number = amount;
#elif (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	if (amount > 0 && WriteFile(dataHandling.handler->comHandle, dataHandling.buffer->outPackets, amount, &number, NULL)) {
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	number = write(dataHandling.handler->comHandle, dataHandling.buffer->outPackets, amount);
	if (number >= 0) {
#else 
	if (0) {
#endif
		DebugLog("Sent# Bytes", number);
		return number;
	}
	DebugLog("!Unable to write to CommPort");
	return -1;
}

int Receive()
{
	if (dataHandling.handler == NULL || dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	if (!PortIsOpen()) {
		DebugLog("!CommPort not ready");
		return -1;
	}
	int writeAmount = 0, foundStart = 0, didntTimeout = 0;
#if (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	clock_t start_time = 0;
#endif
	DataPacket* current = dataHandling.buffer->inPackets;
	byte readByte = 0, *writePtr = (byte*)current;
#if (TRANSMISSION_DEBUG)
	int readIndex = 0;
	for (int i = 0; i <= PACKET_LENGTH; i++, readIndex++) {
		readByte = ((byte*)dataHandling.buffer->outPackets)[readIndex];
#else
	for (int i = 0; i <= PACKET_LENGTH; i++) {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
		if (!ReadFile(dataHandling.handler->comHandle, &readByte, 1, &didntTimeout, NULL)) break;
		if (!didntTimeout) break;
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
		start_time = clock();
		while (read(dataHandling.handler->comHandle, &readByte, 1) != 1 && dataHandling.handler->timeout >= clock() - start_time);
		if (dataHandling.handler->timeout < clock() - start_time) break;
#endif
#endif
		if (readByte == START_BYTE) {
			if (foundStart) {
				current++;
				writePtr = (byte*)current;
			}
			else {
				foundStart = 1;
				writeAmount++;
			}
			i = 0;
		}
#if (TRANSMISSION_DEBUG)
		if (current == dataHandling.buffer->outPackets || readIndex == PACKET_BUFFER_LENGTH * PACKET_LENGTH) break;
#else
		if (current == dataHandling.buffer->outPackets) break;
#endif
		if (foundStart && i != PACKET_LENGTH) {
			writePtr[i] = readByte;
			writeAmount++;
		}
		else if (!foundStart && i == PACKET_LENGTH) i = 0;
	}
	if (writeAmount >= 0) DebugLog("Received# Bytes", writeAmount);
	else DebugLog("!Unable to read from CommPort");
	return writeAmount;
}

int SetPort(const char name[])
{
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	strcpy(dataHandling.handler->comPath, name);
	if (dataHandling.failSafe != NULL) {
		strcpy(dataHandling.failSafe->calPath, name);
		dataHandling.failSafe->changed = 1;
	}
	else DebugLog("!Could not find FailSafe");
	return LoadPort();
}

//Error Detection / Correction functions:
CHKSM_TYPE CalculateChecksum(DataFrame data)
{
	//WIP
	CHKSM_TYPE chksm = 0;
	//start 1 byte
	chksm += data.start;
	//sync 2 bytes
	chksm += (data.sync >> 8) & 0xFF;
	chksm += data.sync & 0xFF;
	//flags 1 byte
	chksm += data.flag;
	//data 42bytes
	for (int i = 0; i < DATA_LENGTH; i++) {
		chksm += data.data[i];
	}
	/* if use uint32_t chksm
	while (chksm > 0xFFFF) {
		chksm = (chksm & 0xFFFF) + (chksm >> 16);
	}
	*/
	return chksm;
}
int CalculateCRC(DataPacket* data)
{
	CHKSM_TYPE crc = 0xFFFF;
	const CHKSM_TYPE polynomial = 0x1021;
	byte*  crc_bytes = (byte*) data;	
	for (int i = 0; i < PACKET_LENGTH - sizeof(CHKSM_TYPE); i++) {
		crc ^= (crc_bytes[i] << 8); //XOR first 8bits
		for(int j= 0; j < 8; j++) {
			if (crc & 0x8000) crc = (crc << 1) ^ polynomial;
			else crc <<= 1;
		}
	}

	if (data->crc == 0) { //no crc -> fill crc
		data->crc = crc;
		return 0; //success
	}
	else {
		if (crc == data->crc) return 0; //0: success, 1: fail. crc presented -> check crc
		else {
			//...WIP
			return 1;
		}
	}
}

//Debug function:
void DebugLog(const char* message, ...)
{
	static int lineCounter[] = {-1, 0, 0, 0, 0, 0}, depth = 0;
	static FILE* output = NULL;
	static int bothOutputs = 0;
	const char* error = "Error: ", * numeric = " {%i}", * pointer = " at 0x%p", * string = " %s", * test = " ...", * counter = "[%02i] ";
	if (DEBUG_OUTPUT == NONE) return;
	va_list args, args_cpy;
	va_start(args, message);
	va_copy(args_cpy, args);
	if (output == NULL) {
		if (DEBUG_OUTPUT == (TERMINAL | LOGFILE)) bothOutputs = 1;
		if ((DEBUG_OUTPUT & LOGFILE) == LOGFILE) {
			output = fopen(DEBUGLOG_NAME, "w");
		}
		if (output == NULL) {
			output = stdout;
			bothOutputs = 0;
			if ((DEBUG_OUTPUT & LOGFILE) == LOGFILE) DebugLog("!Could not open Debug logging file");
		}
	}
	if (lineCounter[0] == -1) {
		fprintf(output, "Start of Debug Log:\n\nLibrary Version: %f\nDatetime: %i\n\n", VERSION, (int)time(NULL));
		if (bothOutputs) fprintf(stdout, "Start of Debug Log:\n\nLibrary Version: %f\nDatetime: %i\n\n", VERSION, (int)time(NULL));
		lineCounter[0]++;
	}
	int inputIndex = 0, makroIndex = 0, outputIndex = 0;
	char* makro, outputString[PATH_LENGTH];
	for (; outputIndex < PATH_LENGTH; outputIndex++) {
		outputString[outputIndex] = '\0';
	}
	for (; makroIndex < depth; makroIndex++) {
		fprintf(output, "    ");
		if (bothOutputs) fprintf(stdout, "    ");
	}
	fprintf(output, counter, lineCounter[depth]);
	if (bothOutputs) fprintf(stdout, counter, lineCounter[depth]);
	for (inputIndex = 0, outputIndex = 0; message[inputIndex] != '\0'; inputIndex++) {
		makro = NULL;
		switch (message[inputIndex]) {
		case '-': {
			fprintf(output, "\nEnd of Debug Log: %s", message + inputIndex);
			if (bothOutputs) fprintf(stdout, "\nEnd of Debug Log: %s", message + inputIndex);
			fclose(output);
			output = NULL;
			lineCounter[0] = -1;
			depth = 0;
			va_end(args);
			return;
		}
		case ':': {
			outputString[outputIndex] = ':';
			outputIndex++;
			if (depth < 5) depth++;
			lineCounter[depth] = 0;
			break;
		}
		case '_': {
			if (depth > 0) depth--;
			break;
		}
		case '!': {
			makro = error;
			break;
		}
		case '#': {
			makro = numeric;
			va_arg(args_cpy, int);
			break;
		}
		case '?': {
			makro = test;
			break;
		}
		case '@': {
			makro = pointer;
			va_arg(args_cpy, void*);
			break;
		}
		case '§': {
			makro = string;
			va_arg(args_cpy, char*);
			break;
		}
		case '~': {
			vfprintf(output, outputString, args);
			if (bothOutputs) vfprintf(stdout, outputString, args);
			for (outputIndex = 0; outputIndex < PATH_LENGTH; outputIndex++) {
				outputString[outputIndex] = '\0';
			}
			outputIndex = 0;
			int max = va_arg(args_cpy, int);
			int* array = va_arg(args_cpy, int*);
			if (array == NULL) break;
			for (makroIndex = 0; makroIndex < max; makroIndex++) {
				fprintf(output, numeric, array[makroIndex]);
				if (bothOutputs) fprintf(stdout, numeric, array[makroIndex]);
			}
			va_copy(args, args_cpy);
			break;
		}
		default: {
			outputString[outputIndex] = message[inputIndex];
			outputIndex++;
		}
		}
		if (outputIndex >= PATH_LENGTH - 10) break;
		if (makro != NULL)
			for (makroIndex = 0; makro[makroIndex] != '\0'; makroIndex++, outputIndex++) outputString[outputIndex] = makro[makroIndex];
	}
	outputString[outputIndex] = '\n';
	vfprintf(output, outputString, args);
	if (bothOutputs) vfprintf(stdout, outputString, args);
	lineCounter[depth]++;
	va_end(args);
	va_end(args_cpy);
}

void DebugSaveFile() {
	DebugLog("Printing SaveFile:");
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile not found_");
		return;
	}
	int i;
	int content[TELEMETRY_AMOUNT];
	DebugLog("Version#", (int)(dataHandling.saveFile->version * 10));
	DebugLog("Time of Creation#", dataHandling.saveFile->dateTime);
	DebugLog("Filename§", dataHandling.saveFile->saveFilePath);
	for (SaveFrame* current = dataHandling.saveFile->firstFrame; current != NULL; current = current->nextFrame) {
		if (FrameIsTC(current->data)) {
			for (i = 0; i < TELEMETRY_AMOUNT; i++) {
				if (i < TELECOMMAND_AMOUNT) content[i] = (int) ReadFrame(current->data, i);
				else content[i] = 0;
			}
		}
		else {
			for (i = 0; i < TELEMETRY_AMOUNT; i++) content[i] = (int) ReadFrame(current->data, i);
		}
		DebugLog("Flag# Sync# Data~ Chksm#", current->data.flag, current->data.sync, TELEMETRY_AMOUNT, content, current->data.chksm);
	}
	DebugLog("End of SaveFile_");
}
//End of DataHandlingLibrary