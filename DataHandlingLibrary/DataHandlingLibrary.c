//Source File of DataHandlingLibrary
#include "DataHandlingLibrary.h"

//Core
static struct DataHandlingHub dataHandling = { 0 };

//INTERNAL
static int _SetPositions_();
static int _SetPortConfig_();
static int _CreateHandler_();
static int _CreateFrameLookUp_();
static void _SortCalibration_();

//PRIVATE (INTERNAL)
DataPacket GetInPacket();
DataPacket GetOutPacket();
int AddInPacket(DataPacket data);
int AddOutPacket(DataPacket data);
int VirtualSave();
int FormPackets(); //Converts all buffered DataFrames into buffered outgoing DataPackets, returns the amount converted
int FormFrames(); //Converts all buffered incoming DataPackets into buffered DataFrames (with {0} values if parts are missing), returns the amount converted
DataFrame GetOutFrame(); //Returns the latest buffered outgoing DataFrame and removes it from the buffer
int AddInFrame(DataFrame frame); //Adds an incoming DataFrame to the Buffer, returns the corresponding index
DataFrame GetInFrame(); //Returns the latest buffered incoming DataFrame and removes it from the buffer
int LoadPort(); //Configures and opens the communication port

//Implementations:

int CalculateChecksum(DataPacket data)
{
	//WIP
	return 1;
}
int CalculateCRC(DataPacket data)
{
	//WIP
	return 0;
}

int UpdateAll()
{
	int out = 0;
	out += UpdateFiles();
	out += UpdateBuffer();
	return out;
}

int UpdateBuffer()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitiated DataHandling");
		return 0;
	}
	int out = 1;
	if (FormPackets() > 0)
		if (Send(dataHandling.buffer->outgoingPos, dataHandling.buffer->outgoingBytes) < 0)
			out -= 1;
	if (Receive(dataHandling.buffer->incomingPos, dataHandling.buffer->incomingBytes) > 0)
	{
		if (dataHandling.buffer->incomingBytes < PACKET_LENGTH) dataHandling.buffer->incomingBytes += PACKET_LENGTH;
		if (FormFrames() > 0)
			for (DataFrame temp = GetOutFrame(); !FrameIsEmpty(temp); temp = GetOutFrame())
				AddSaveFrame(temp);
		else out -= 1;
	}
	return out;
}

int UpdateFiles()
{
	int out = 1;
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile");
		out -= 1;
	}
	else if (WriteSave() == -1) {
		DebugLog("!Could not write SaveFile file");
		out -= 1;
	}
	if (dataHandling.failSafe == NULL) {
		DebugLog("!Could not find FailSafe");
		out -= 1;
	}
	else if (WriteFailSafe() == -1) {
		DebugLog("!Could not write FailSafe file");
		out -= 1;
	}
	if (dataHandling.calibration == NULL) {
		if (METHOD != NONE) {
			DebugLog("!Could not fin Calibration");
			out -= 1;
		}
	}
	else if (WriteCalibration() == -1) {
		DebugLog("!Could not write Calibration file");
		out -= 1;
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

float MapSensorValue(int id, int value)
{
	if (METHOD == NONE) return (float)value;
	if ((dataHandling.calibration != NULL) & (id >= 0) & (id < SENSOR_AMOUNT) || (CALIBRATION_POINTS < 2)) {
		if (!dataHandling.calibration->sorted) _SortCalibration_();
		CalibrationPoint points[CALIBRATION_POINTS];
		float out = 0.0f;
		int i, j;
		for (i = 0; i < CALIBRATION_POINTS; i++) {
			//reading points
			points[i] = ReadPoint(id, i);
			//trivial solutions
			if (!points[0].valid) return out;
			if (!points[1].valid) return out;
			if ((points[i].digital = value) & (points[i].valid)) return points[i].analog;
			
		}
		//linear interpolation
		if ((METHOD == LINEAR) & (CALIBRATION_POINTS > 1)) {
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
		else if ((METHOD == QUADRATIC) & (CALIBRATION_POINTS == 3)) { 
			if (!points[2].valid) return out;
			float a = 0.0f, b = 0.0f, c = 0.0f;
			out = a * (value * value) + b * value + c;
		}
		return out;
	}
	return 0.0f;
}

void WritePoint(int id, int number, int digitalValue, float analogValue)
{
	CalibrationPoint point = { digitalValue, analogValue , 1};
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

CalibrationPoint ReadPoint(int id, int number)
{
	static CalibrationPoint point = { 0, 0.0f, 0 };
	if (dataHandling.calibration == NULL)
	{
		DebugLog("!Calibration not found");		
		return point;
	}
	if ((id >= 0) & (id < SENSOR_AMOUNT) & (number >= 0) & (number < CALIBRATION_POINTS)) 
		return dataHandling.calibration->points[id][number];
	else { 
		DebugLog("!ID# or number# out of range", id, number);
		return point;
	}
}

int ReadCalibration(const char* path)
{
	//WIP
	return CreateCalibration(path);;
}

int WriteCalibration()
{
	if (dataHandling.calibration == NULL) {
		DebugLog("!Could not find Calibration");
		return 0;
	}
	return !dataHandling.calibration->changed;
}

void _SortCalibration_()
{
	if (dataHandling.calibration == NULL) {
		DebugLog("!Could not find Calibration");
		return;
	}
	if (dataHandling.calibration->sorted) return;
	int i, j, k;
	CalibrationPoint cpy = { 0, 0, 0 };
	for (i = 0; i < SENSOR_AMOUNT; i++) {
		for (j = CALIBRATION_POINTS - 1; j > 0; j--) {
			for (k = 1; k <= j; k++) {
				//WHY do you break everything?
				if (dataHandling.calibration->points[i][k].digital < dataHandling.calibration->points[i][k - 1].digital)
				cpy = dataHandling.calibration->points[i][k];
				dataHandling.calibration->points[i][k] = dataHandling.calibration->points[i][k - 1];
				dataHandling.calibration->points[i][k - 1] = cpy;
			}
		}
	}
	dataHandling.calibration->sorted = 1;
}

#define RECURSIVE_LOG  if (!recursive) {recursive = 1; DebugLog(message + 1, args); recursive = 0;} else DebugLog(message + 1, args);

void DebugLog(char* message, ...)
{
	static int counter = -1, depth = 0, i = 0, recursive = 0, tailIndex = 0;
	static FILE* output = NULL;
	static char *head, *text, argument[20], *tail[20];
	if (DEBUG_OUTPUT == NONE) return;
	va_list args;
	va_start(args, message);
	if (output == NULL) {
		if (DEBUG_OUTPUT == LOGFILE) {
			output = fopen(DEBUGLOG_NAME, "w");
			if (output == NULL) {
				output = stdout;
				DebugLog("!Could not open Debug logging file");
			}
		}
		else if (DEBUG_OUTPUT == TERMINAL) output = stdout;
		else return;
	}
	if (!recursive) {
		head = "";
		text = "";
		argument[0] = '\0';
		tail[0] = "";
		for (i = 0; i < depth; i++) fprintf(output, "    ");
	}
	if (counter == -1) {
		fprintf(output, "Start of Debug Log:\n\nLibrary Version: %f\nDate Time: %i\n\n", VERSION, (int)time(NULL));
		counter++;
	}
	switch (message[0]) {
		case '\0': {
			fprintf(output, "\n");
			break;
		}
		case '-': {
			fprintf(output, "\nEnd of Debug Log: %s", message + 1);
			fclose(output);
			output = NULL;
			counter = -1;
			depth = 0;
			va_end(args);
			return;
		}
		case '+': {
			char change[PATH_LENGTH];
			strcpy(change, message);
			change[0] = '-';
			DebugLog(change);
			change[0] = '?';
			DebugLog(change);
			va_end(args);
			return;
		}
		case ':': {
			if (recursive) {
				DebugLog("!Wrong Use of Headline [:], Additional modifier passed in front");
				break;
			}
			head = "-";
			tail[tailIndex] = ":";
			text = message + 1;
			depth++;
			break;
		}
		case '_': {
			if (depth == 0) { 
				DebugLog("!Wrong Use of End of Headline [_], No preceding Headline [:]");
				break;
			}
			RECURSIVE_LOG
			depth--;
			break;
		}
		case '!': {
			head = "Error: ";
			RECURSIVE_LOG
			break;
		}
		case '#': {
			if (tailIndex < 20) {
				tail[tailIndex] = ": ";
				argument[tailIndex] = 'i';
				tailIndex++;
			}
			RECURSIVE_LOG;
			break;
		}
		case '?': {
			if (tailIndex < 20) {
				tail[tailIndex] = " ...";
				argument[tailIndex] = '\0';
				tailIndex++;
			}
			RECURSIVE_LOG;
			break;
		}
		case '@': {
			if (tailIndex < 20) {
				tail[tailIndex] = " at ";
				argument[tailIndex] = 'p';
				tailIndex++;
			}
			RECURSIVE_LOG
			break;
		}
		case '$': {
			if (tailIndex < 20) {
				tail[tailIndex] = " ";
				argument[tailIndex] = 's';
				tailIndex++;
			}
			RECURSIVE_LOG
			break;
		}
		default: {
			text = message;
			counter++;
		}
	}
	if (!recursive) {
		if (head[0] == '-') fprintf(output, "[--] %s", text);
		else fprintf(output, "[%02i] %s%s", counter, head, text);
		for (i = 0; i <= tailIndex; i++) {
			if (argument[i] != '\0') {
				if (argument[i] == 'i') fprintf(output, "%s%i", tail[i], va_arg(args, int));
				else if (argument[i] == 'p') fprintf(output, "%s%p", tail[i], va_arg(args, void*));
				else if (argument[i] == 's') fprintf(output, "%s%s", tail[i], va_arg(args, char*));
			}
			else {
				fprintf(output, "%s\n", tail[i]);
				break;
			}
		}
	}
	va_end(args);
}

int CreateCalibration(const char* path)
{
	if (dataHandling.handler != NULL) {
		free(dataHandling.handler);
		dataHandling.handler = NULL;
	}
	SensorCalibration* new = malloc(sizeof(SensorCalibration));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(SensorCalibration); i++) bytePtr[i] = 0;
	new->version = CALIBRATION_VERSION;
	new->dateTime = time(NULL);
	strcpy(new->calibrationFilePath, path);
	dataHandling.calibration = new;
	return 1;
}

int Initialize()
{
	DebugLog(":Setting up DataHandling");
	if (!ReadFailSafe()) {
		CreateFailSafe();
	}
	int readExisting = 1;
	if (dataHandling.failSafe == NULL) readExisting = 0;
	else readExisting = !(dataHandling.failSafe->nominalExit) && dataHandling.failSafe->saveFilePath[0] != '\0';
	if (readExisting) {
		DebugLog("Existing SaveFile found");
		ReadSave(dataHandling.failSafe->saveFilePath);
	}
	if (dataHandling.saveFile == NULL) {
		CreateSave(SAVEFILE_NAME);
	}
	if (dataHandling.saveFile == NULL) {
		VirtualSave();
		if (dataHandling.failSafe != NULL) strcpy(dataHandling.failSafe->saveFilePath, "");
	}
	else if (!readExisting & (dataHandling.failSafe != NULL)) strcpy(dataHandling.failSafe->saveFilePath, SAVEFILE_NAME);
	
	DebugLog("?Reserving Memory for Input / Output Buffer");
	if (CreateBuffer()) DebugLog("Buffer created");

	if (METHOD != NONE) {
		if (dataHandling.failSafe != NULL) {
			if (dataHandling.failSafe->calPath[0] != '\0') {
				DebugLog("?Reading Calibration");
				if (ReadCalibration(dataHandling.failSafe->calPath)) DebugLog("Calibration read");
			}
		}
		if (dataHandling.calibration == NULL) {
			DebugLog("?Creating new Calibration");
			if (CreateCalibration(CALIBRATION_NAME)) DebugLog("Calibration created");
		}
	}
	else DebugLog("Skipping Calibration");

	DebugLog("?Executing Misc tasks");
	_CreateFrameLookUp_();
	_SetPositions_();
	_CreateHandler_();
	LoadPort();
	DebugLog("Misc tasks completed");
	DebugLog("_Setup done");
	return 1;
}

DataFrame CreateFrame(uint16_t sync)
{
	DataFrame temp = { 0 };
	char* bytePtr = (char*) & temp;
	for (int i = 0; i < sizeof(DataFrame); i++) bytePtr[i] = 0;
	temp.sync = sync;
	return temp;
}

DataFrame CreateTC(uint16_t sync)
{
	DataFrame temp = CreateFrame(sync);
	FrameAddFlag(&temp, TeleCommand);
	return temp;
}

DataFrame EmptyFrame()
{
	return CreateFrame(0);
}

DataFrame EmptyTC() 
{
	return CreateTC(0);
}

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
		if ((id >= 0) & (id < SENSOR_AMOUNT)) length = BASE_RES;
		if ((id >= SENSOR_AMOUNT) & (id < TELEMETRY_AMOUNT)) length = BASE_LEN;
		switch (id) {
			case Compare_Temperature:
			case Chamber_Pressure:
			case Nozzle_Pressure_1:
			case Nozzle_Pressure_2:
			case Nozzle_Pressure_3:
			case Nozzle_Temperature_1:
			case Nozzle_Temperature_2:
			case Nozzle_Temperature_3: length = HIGH_RES; break;
			case Experiment_State: length = EXP_LEN; break;
			case Nozzle_Servo:
			case Sensorboard_1:
			case Sensorboard_2: length = HIGH_LEN; break;
			case Mainboard: length = MAIN_LEN; break;
			case System_Time: length = TIME_LEN; break;
		}
		dataHandling.frameLookUp->telemetry_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telemetry_Pos_Len[id][1] = length;
		pos += length;
		if (pos >= DATA_LENGTH * 8) {
			DebugLog("!Unsufficient (Data) Real Estate");
			return 0;
		}
	}
	for (id = 0, pos = 0; id < TELECOMMAND_AMOUNT; id++) {
		if ((id >= 0) & (id < TELECOMMAND_AMOUNT)) length = BASE_LEN + 1;
		switch (id) {
			case Valve_Delay:
			case Servo_Delay:
			case EoE_Delay:
			case Power_Off_Delay:
			case Nozzle_On_Delay:
			case Servo_Control: length = DELAY_LEN + 1; break;
		}
		dataHandling.frameLookUp->telecommand_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telecommand_Pos_Len[id][1] = length;
		pos += length;
		if (pos >= DATA_LENGTH * 8) {
			DebugLog("!Unsufficient (Data) Real Estate");
			return 0;
		}
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
	char* bytePtr = (char*) dataHandling.handler;
	for (int i = 0; i < sizeof(PortHandler); i++) {
		bytePtr[i] = 0;
	}
	dataHandling.handler->comHandle = INVALID_HANDLE_VALUE;
	if (dataHandling.failSafe != NULL) 
		strcpy(dataHandling.handler->comPath, dataHandling.failSafe->comPath);
	else {
		DebugLog("!Could not find FailSafe");
		strcpy(dataHandling.handler->comPath, DEFAULTCOMPATH);
	}
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
	char* bytePtr = (char*)dataHandling.frameLookUp;
	for (int i = 0; i < sizeof(FrameLookUpTable); i++)
		bytePtr[i] = 0;
	return 1;
}

int WriteFrame(DataFrame* frame, int id, int value)
{
	if (frame == NULL || dataHandling.frameLookUp == NULL) {
		DebugLog("!Invalid Frame-pointer or uninitialized DataHandling");
		return 0;
	}
	int TC = FrameIsTC(*frame);
	if ((TC & (id >= TELECOMMAND_AMOUNT)) || id >= TELEMETRY_AMOUNT) {
		DebugLog("!ID out of range");
		return 0;
	}
	int index = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][0] : dataHandling.frameLookUp->telemetry_Pos_Len[id][0];
	int length = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][1] : dataHandling.frameLookUp->telemetry_Pos_Len[id][1];
	if (value < 0 || value >= 1 << length) {
		DebugLog("!#Value out of writable range at Index", id);
		return 0;
	}
	int old_value = 0;
	int old_bytes = 0;
	int new_bytes = 0;
	int new_value = value;
	char* newBytePtr = (char*) &new_bytes;
	char* bytePtr = (char*) &old_bytes;
	char* oldBytePtr = (char*) &old_value;
	for (int i = 0; i <= length / 8; i++) {
		oldBytePtr[i] = frame->data[index / 8 + i];
		bytePtr[i] = oldBytePtr[i];
	}
	old_value >>= 8 - ((index + length) % 8);
	old_value %= 1 << length;
	new_value <<= 8 - ((index + length) % 8);
	old_value <<= 8 - ((index + length) % 8);
	new_bytes = old_bytes - old_value + new_value;
	for (int i = 0; i <= length / 8; i++) {
		frame->data[index / 8 + i] = newBytePtr[i];
	}
	old_value >>= 8 - ((index + length) % 8);
	return old_value;
}

int ReadFrame(DataFrame frame, int id)
{
	if (dataHandling.frameLookUp == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
	int TC = FrameIsTC(frame);
	if ((TC & (id >= TELECOMMAND_AMOUNT)) || id >= TELEMETRY_AMOUNT) {
		DebugLog("!#ID out of range", id);
		return 0;
	}
	int index = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][0] : dataHandling.frameLookUp->telemetry_Pos_Len[id][0];
	int length = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][1] : dataHandling.frameLookUp->telemetry_Pos_Len[id][1];
	int value = 0;
	char* bytePtr = (char*) &value;
	for (int i = 0; i <= length / 8; i++) bytePtr[i] = frame.data[index / 8 + i];
	value >>= 8 - ((index + length) % 8);
	value %= 1 << length;
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
	int group1 = frame.flag >> 6, group2 = (frame.flag % 1 << 6) >> 3, group3 = (frame.flag % 1 << 3);
	if (id >= 10) {
		if (id >= 100) {
			return group1 == id / 100;
		}
		else {
			return group2 == id / 10;
		}
	}
	else {
		return group3 == id;
	}
	return 0;
}

void FrameAddFlag(DataFrame* frame, int id)
{
	if (frame == NULL) return;
	int group1 = frame->flag >> 6, group2 = (frame->flag % 1 << 6) >> 3, group3 = (frame->flag % 1 << 3);
	if (id >= 10) {
		if (id >= 100) {
			if (id < (1 << 2) * 100) group1 = id / 100;
			else return;
		}
		else {
			if (id < (1 << 3) * 10) group2 = id / 10;
			else return;
		}
	}
	else {
		if (id <= 1 << 3) group3 = id;
		else return;
	}
	frame->flag = (group1 << 6) + (group2 << 3) + group1;
}

DataPacket CreatePacket(int16_t sync)
{
	DataPacket out = { 0 };
	char* bytePtr = (char*) & out;
	for (int i = 0; i < sizeof(out); i++)
		bytePtr[i] = 0;
	if (sync != 0) out.sync = sync;
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

int EncodePackets()
{
	//WIP
	return 1;
}

int DecodePackets()
{
	//WIP
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
	int id, payloadIndex, dataIndex;
	for (; !FrameIsEmpty(currentFrame); currentFrame = GetOutFrame(), number++) {
		for (id = 0; id <= 255; id++) {
			currentPacket = CreatePacket(currentFrame.sync);
			currentPacket.mode = (OS == LINUX_OS) ? 0 : 1;
			currentPacket.id = id;
			for (payloadIndex = 0; payloadIndex < PAYLOAD_LENGTH; payloadIndex++) {
				dataIndex = payloadIndex + PAYLOAD_LENGTH * id;
				if (dataIndex < DATA_LENGTH) currentPacket.payload[payloadIndex] = currentFrame.data[dataIndex];
				else currentPacket.payload[payloadIndex] = 0;
			}
			AddOutPacket(currentPacket);
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
	int sync = framePtr->sync, number = 0;
	int bufferIndex, payloadIndex, dataIndex;
	for (; !PacketIsEmpty(currentPacket); currentPacket = GetInPacket(), number++) {
		if (sync != currentPacket.sync) {
			for (bufferIndex = 0, framePtr = dataHandling.buffer->outFrames; bufferIndex < BUFFER_LENGTH || framePtr->sync == currentPacket.sync; bufferIndex++, framePtr = dataHandling.buffer->outFrames + bufferIndex);
			if (framePtr->sync != currentPacket.sync) framePtr = dataHandling.buffer->inFrames + AddInFrame(CreateFrame(currentPacket.sync));
			sync = framePtr->sync;
		}
		for (payloadIndex = 0; payloadIndex < PAYLOAD_LENGTH; payloadIndex++) {
			dataIndex = payloadIndex + PAYLOAD_LENGTH * currentPacket.id;
			if (dataIndex < DATA_LENGTH) framePtr->data[dataIndex] = currentPacket.payload[payloadIndex];
		}
	}
	return number;
}

DataPacket GetOutPacket()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return EmptyPacket();
	}
	DataPacket temp = EmptyPacket();
	for (int i = BUFFER_LENGTH; i > 0; i--) {
		temp = dataHandling.buffer->outPackets[i - 1];
		if (!PacketIsEmpty(temp)) {
			dataHandling.buffer->outPackets[i - 1] = EmptyPacket();
		}
	}
	return temp;
}

DataPacket GetInPacket()
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return EmptyPacket();
	}
	DataPacket temp = EmptyPacket();
	for (int i = BUFFER_LENGTH; i > 0; i--) {
		temp = dataHandling.buffer->inPackets[i - 1];
		if (!PacketIsEmpty(temp)) {
			dataHandling.buffer->inPackets[i - 1] = EmptyPacket();
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
	return temp;
}

int AddOutPacket(DataPacket data)
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int i = 0;
	for (; i <= BUFFER_LENGTH; i++) {
		if (PacketIsEmpty(dataHandling.buffer->outPackets[i])) {
			dataHandling.buffer->outPackets[i] = data;
			break;
		}
	}
	return i;
}

int AddInPacket(DataPacket data)
{
	if (dataHandling.buffer == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	int i = 0;
	for (; i <= BUFFER_LENGTH; i++) {
		if (PacketIsEmpty(dataHandling.buffer->inPackets[i])) {
			dataHandling.buffer->inPackets[i] = data;
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

void AddFrame(DataFrame frame)
{
	AddSaveFrame(frame);
	AddOutFrame(frame);
	return;
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

int CreateBuffer()
{
	if (dataHandling.buffer != NULL) {
		free(dataHandling.buffer);
		dataHandling.buffer = NULL;
	}
	DataBuffer* new = (DataBuffer*) malloc(sizeof(DataBuffer));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(DataBuffer); i++) bytePtr[i] = 0;
	dataHandling.buffer = new;
	return 1;
}

int CreateFailSafe() 
{
	if (dataHandling.failSafe != NULL) {
		free(dataHandling.failSafe);
		dataHandling.failSafe = NULL;
	}
	FailSafe* new = (FailSafe*)malloc(sizeof(FailSafe));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(FailSafe); i++) bytePtr[i] = 0;
	new->nominalExit = 1;
	new->conn = 'a';
	new->lang = 'e';
	new->dateTime = time(NULL);
	new->version = FAILSAFE_VERSION;
	new->mode = 'f';
	strcpy(new->saveFilePath, SAVEFILE_NAME);
	strcpy(new->comPath, DEFAULTCOMPATH);
	FILE* file;
	file = fopen(FAILSAFE_NAME, "w");
	if (file != NULL) {
		fprintf(file, "Version: %f;\n", new->version);
		fprintf(file, "Datetime: %lli;\n", new->dateTime);
		fprintf(file, "Savefile: %s;\n", new->saveFilePath);
		fprintf(file, "Complete: %c;\n", (new->complete) ? 'y' : 'n');
		fprintf(file, "Nominal Exit: %c;\n", (new->nominalExit)? 'y': 'n');
		fprintf(file, "Mode: %c;\n", new->mode);
		fprintf(file, "Connection: %c;\n", new->conn);
		fprintf(file, "Language: %c;", new->lang);
		fclose(file);
	}
	else DebugLog("!Could not create FailSafe file");
	dataHandling.failSafe = new;
	return 1;
}

int ReadFailSafe()
{
	return 0;
	DebugLog(":Reading FailSafe");
	if (dataHandling.failSafe != NULL) {
		DebugLog("?Freeing FailSafe");
		free(dataHandling.failSafe);
		dataHandling.failSafe = NULL;
		DebugLog("FailSafe freed");
	}
	FILE* file = NULL;
	FailSafe* this = (FailSafe*)malloc(sizeof(FailSafe));
	if (this == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	dataHandling.failSafe = this;
	char* bytePtr = (char*) this;
	for (int i = 0; i < sizeof(FailSafe); i++) bytePtr[i] = 0;
	float ReadVersion = 0.0f;
	this->version = FAILSAFE_VERSION;
	DebugLog("Memory initialized");
	file = fopen(FAILSAFE_NAME, "r");
	if (file != NULL) {
		DebugLog("File opened");
		if (ReadVersion = fscanf(file, "Version: %f;") != EOF) {
			if (ReadVersion == this->version) {
				if (ReadVersion != this->version) return 0;
				//Newest FileReader here:
				char boolreader;
				int length = PATH_LENGTH;
				if (fscanf(file, "Datetime: %lli;\n", &this->dateTime) != EOF)
					if (fscanf(file, "Savefile: %s;\n", &this->saveFilePath, length) != EOF) {
						length = 1;
						if (fscanf(file, "Complete: %c;\n", &boolreader, length) != EOF) {
							this->complete = (boolreader == 'y') ? 1 : 0;
							if (fscanf(file, "Nominal Exit: %c;\n", &boolreader, length) != EOF) {
								this->nominalExit = (boolreader == 'y') ? 1 : 0;
								if (fscanf(file, "Mode: %c;\n", &this->mode, length) != EOF)
									if (fscanf(file, "Connection: %c;\n", &this->conn, length) != EOF)
										if (fscanf(file, "Language: %c;", &this->lang, length) != EOF) {
											DebugLog("_@Failsafe read", this);
											fclose(file);
											return 1;
										}
							}
						}
					}
				DebugLog("!Could not parse FailSafe file");
				fclose(file);
			}
			else if (0) {
					//Older FileReader here:
			}
		}
	}
	else DebugLog("!Could not open FailSafe file");
	DebugLog("_Failsafe reading failed");
	return 0;
}

int WriteFailSafe()
{
	//WIP
	if (dataHandling.failSafe == NULL) {
		DebugLog("!Could not find FailSafe");
		return 0;
	}
	return !dataHandling.failSafe->changed;
}

int VirtualSave()
{
	if (dataHandling.saveFile != NULL) {
		CloseSave();
		free(dataHandling.saveFile);
		dataHandling.saveFile = NULL;
	}
	SaveFile* new = (SaveFile*) malloc(sizeof(SaveFile));
	if (new == NULL) {
		DebugLog("!Memory allocation failed");
		return 0;
	}
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(SaveFile); i++) bytePtr[i] = 0;
	new->dateTime = time(NULL);
	new->savedAmount = -1;
	new->version = SAVEFILE_VERSION;
	new->currentTC = CreateTC(0);
	dataHandling.saveFile = new;
	return 1;
}

int CheckSave()
{
	//WIP
	return 0;
}

int ReadSave(const char path[])
{
	//WIP
	return 0;
}

SaveFileFrame* GetSaveFrame(int index)
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return NULL;
	}
	if (index >= dataHandling.saveFile->frameAmount || index < 0) return dataHandling.saveFile->lastFrame;
	if (index == 0) return dataHandling.saveFile->firstFrame;
	SaveFileFrame* frame = dataHandling.saveFile->firstFrame;
	for (int i = 0; i < index; i++) {
		if (frame == NULL) return NULL;
		if (frame->nextFrame == NULL) return frame;
		frame = frame->nextFrame;
	}
	return frame;
}

DataFrame UpdateTC()
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
	SaveFileFrame* currentFrame = dataHandling.saveFile->lastFrame;
	for (; currentFrame->previousFrame != NULL; currentFrame = currentFrame->previousFrame) {
		if (FrameIsTC(currentFrame->data)) {
			if (FrameIsEmpty(newestTC)) newestTC = currentFrame->data;
			else if (currentFrame->data.sync < newestTC.sync) break;
			else if (currentFrame->data.sync > newestTC.sync) newestTC = currentFrame->data;
		}
	}
	if (!FrameIsEmpty(newestTC)) dataHandling.saveFile->currentTC = newestTC;
	return dataHandling.saveFile->currentTC;
}

SaveFileFrame* AddSaveFrame(DataFrame data)
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return NULL;
	}
	SaveFileFrame* newFrame = (SaveFileFrame*) malloc(sizeof(SaveFileFrame));
	if (newFrame == NULL) {
		DebugLog("!Memory allocation failed");
		return NULL;
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
	return dataHandling.saveFile->lastFrame;
}

SaveFileFrame* CreateSaveFrame(uint16_t sync)
{
	if (dataHandling.saveFile == NULL) {
		DebugLog("!SaveFile could not be found");
		return NULL;
	}
	DataFrame data = CreateFrame(sync);
	return AddSaveFrame(data);
}

void CloseSave()
{
	DebugLog(":Closing SaveFile");
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile to close");
		return;
	}
	DebugLog("@Savefile found", dataHandling.saveFile);
	DebugLog("?Emptying SaveFileFrames");
	SaveFileFrame *current = dataHandling.saveFile->lastFrame, *last = dataHandling.saveFile->firstFrame, *next;
	if (current != NULL) {
		next = current->previousFrame;
		if (next != NULL) {
			while ((next != dataHandling.saveFile->firstFrame) & (next != NULL)) {
				free(current);
				current = next;
				next = next->previousFrame;
			}
		}
		if (current != last) DebugLog("!Could not parse SaveFileFrames"); //TBC
		free(current);
	}
	DebugLog("SaveFileFrames emptied");
	dataHandling.saveFile->lastFrame = NULL;
	dataHandling.saveFile->firstFrame = NULL;
	dataHandling.saveFile->frameAmount = dataHandling.saveFile->savedAmount;
	dataHandling.saveFile->loadedAmount = 0;
	dataHandling.saveFile->currentTC = EmptyTC();
	DebugLog("_SaveFile closed");
}

void CloseAll()
{
	DebugLog(":Closing DataHandling");
	DebugLog("?Setting nominal exit");
	if (dataHandling.failSafe != NULL) {
		dataHandling.failSafe->nominalExit = 1;
		if (WriteFailSafe() != -1) DebugLog("Nominal exit set");
	}
	else DebugLog("!Could not find FailSafe");
	DebugLog("?Freeing Memory");
	if (dataHandling.buffer != NULL) free(dataHandling.buffer);
	if (dataHandling.calibration != NULL) free(dataHandling.calibration);
	if (dataHandling.failSafe != NULL) free(dataHandling.failSafe);
	if (dataHandling.frameLookUp != NULL) free(dataHandling.frameLookUp);
	if (dataHandling.handler != NULL) {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
		if (!CloseHandle(dataHandling.handler->comHandle)) {
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
		if (!close(dataHandling.handler->comHandle)) {
#else
		if (0) {
#endif
			DebugLog("!Could not close serial Port");
		}
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
	DebugLog("_DataHandling closed");
}

int WriteSave()
{
	DebugLog(":Writing SaveFile");
	if (dataHandling.saveFile == NULL) {
		DebugLog("!Could not find SaveFile");
		DebugLog("");
		return 0;
	}
	DebugLog("@SaveFile found", dataHandling.saveFile);
	if (dataHandling.saveFile->savedAmount == -1 || dataHandling.saveFile->savedAmount >= dataHandling.saveFile->frameAmount) {
		DebugLog("_SaveFile write unneccessary");
		return 0;
	}
	FILE* file = NULL;
	if (dataHandling.saveFile->saveFilePath[0] != '\0') {
		file = fopen(dataHandling.saveFile->saveFilePath, "ab");
		if (file != NULL) {
			SaveFileFrame* current = GetSaveFrame(dataHandling.saveFile->savedAmount - dataHandling.saveFile->unloadedAmount - 1);
			char* bytePtr = NULL;
			int number = 0;
			while (current != NULL) {
				bytePtr = (char*)&(current->data);
				number += (int)fwrite(bytePtr, sizeof(DataFrame), 1, file);
				current = current->nextFrame;
				dataHandling.saveFile->savedAmount++;
			}
			fclose(file);
			if (dataHandling.saveFile->savedAmount < dataHandling.saveFile->frameAmount) DebugLog("!Could not write all frames");
			DebugLog("_$SaveFile written at", dataHandling.saveFile->saveFilePath);
			return number;
		}
		else DebugLog("!Could not open SaveFile file");
	}
	DebugLog("_$Could not write SaveFile at", dataHandling.saveFile->saveFilePath);
	return 0;
}

int CreateSave(const char path[])
{
	DebugLog(":Creating SaveFile");
	VirtualSave();
	if (dataHandling.saveFile == NULL) {
		DebugLog("_SaveFile creation failed");
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
		fwrite(&(dataHandling.saveFile->dateTime), sizeof(time_t), 1, file);
		fclose(file);
	}
	else {
		DebugLog("!Could not create SaveFile file");
		DebugLog("_SaveFile creation failed");
		free(dataHandling.saveFile);
		dataHandling.saveFile = NULL;
		return 0;
	}
	DebugLog("_@SaveFile created", dataHandling.saveFile);
	return 1;
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
	if (GetCommState(dataHandling.handler->comHandle, &(dataHandling.handler->options))) {
		dataHandling.handler->options.Parity = NOPARITY;
		dataHandling.handler->options.ByteSize = 8;
		dataHandling.handler->options.StopBits = ONESTOPBIT;
		dataHandling.handler->options.BaudRate = BAUD_RATE;
	}
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	if (tcgetattr(dataHandling.handler->comHandle, &(dataHandling.handler->options)) == 0) {
		dataHandling.handler->options.c_iflag = IGNPAR;
		dataHandling.handler->options.c_cflag = BAUD_RATE | CS8 | CLOCAL | CREAD;
		dataHandling.handler->options.c_oflag = 0;
		dataHandling.handler->options.c_lflag = 0;
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
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return 0;
	}
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	dataHandling.handler->comHandle = CreateFileA(dataHandling.handler->comPath, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	dataHandling.handler->comHandle = open(dataHandling.handler->comPath, O_RDWR | O_NOCTTY | O_NDELAY);
#endif
	if (dataHandling.handler->comHandle != INVALID_HANDLE_VALUE) {
		if (_SetPortConfig_()) {
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
			if (SetCommState(dataHandling.handler->comHandle, &(dataHandling.handler->options))) return 1;
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
			tcflush(dataHandling.handler->comHandle, TCIOFLUSH);
			if (tcsetattr(dataHandling.handler->comHandle, TCSANOW, &(dataHandling.handler->options)) == 0) return 1;
#else
			if (0);
#endif
			else DebugLog("!#Could not set CommState of serial Port", errno);
		}
	}
	else DebugLog("!#Could not open serial Port", errno);
	return 0;
}

int Send(char* start, int amount)
{
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	if (start == NULL) {
		DebugLog("!NULL Pointer passed");
		return -1;
	}
	int number = 0;
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	if (WriteFile(dataHandling.handler->comHandle, start, amount, &number, NULL))
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	number = write(dataHandling.handler->comHandle, start, amount);
	if (number >= 0)
#else 
	if (0)
#endif
	{
		dataHandling.buffer->outgoingBytes -= number;
		dataHandling.buffer->outgoingPos += number;
		return number;
	}
	DebugLog("!Unable to write to serial Port");
	return -1;
}

int Receive(char* buffer, int max)
{
	if (dataHandling.handler == NULL) {
		DebugLog("!Uninitialized DataHandling");
		return -1;
	}
	if (buffer == NULL) {
		DebugLog("!NULL Pointer passed");
		return -1;
	}
	int number = 0;
#if (DATAHANDLINGLIBRARY_OS == WINDOWS_OS)
	if (ReadFile(dataHandling.handler->comHandle, buffer, max, &number, NULL))
#elif (DATAHANDLINGLIBRARY_OS == LINUX_OS)
	number = read(dataHandling.handler->comHandle, buffer, max);
	if (number >= 0)
#else
	if (0)
#endif
	{
		dataHandling.buffer->incomingPos += number;
		dataHandling.buffer->incomingBytes -= number;
		return number;
	}
	DebugLog("!Unable to listen to serial Port");
	return -1;
}
