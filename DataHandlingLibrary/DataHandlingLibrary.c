//Source File of DataHandlingLibrary
#include "pch.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "DataHandlingLibrary.h"
#include <windows.h>

//INTERNAL
static int _SetPositions_();
static int _SetDCB_();
static int _ConfigurePort_();
static int _CreateHandler_();
static int _CreateFrameLookUp_();

//Core
static struct DataHandlingHub dataHandling = { 0 };

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

int Update()
{
	if (dataHandling.buffer == NULL || dataHandling.saveFile == NULL) return 0;
	if (WriteSave() == -1)
		return -3;
	if (FormPackets() > 0) 
		if (Send() == -1)
			return -1;
	if (Receive() > 0)
	{
		FormFrames();
		for (DataFrame temp = GetOutFrame(dataHandling.buffer); !FrameIsEmpty(temp); temp = GetOutFrame(dataHandling.buffer))
			AddSaveFrame(temp);
	}
	else return -2;
	return 1;
}

float MapSensVal(int id, int value)
{
	return MapSensorValue(id, value);
}

float MapSensorValue(int id, int value)
{
	//WIP
	if ((dataHandling.calibration != NULL) & (id >= 0) & (id < SENSOR_AMOUNT)) {
		return 1.0f;
	}
	else return 0.0f;
}

void WritePoint(int id, int number, int digitalValue, float analogValue)
{
	CalibrationPoint point = { digitalValue, analogValue };
	AddCalibrationPoint(id, number, point);
}

void AddCalibrationPoint(int id, int number, CalibrationPoint point)
{
	if ((dataHandling.calibration != NULL) & (id >= 0) & (id < SENSOR_AMOUNT) & (number > 0) & (number <= CALIBRATION_POINTS))
	dataHandling.calibration->points[id][number - 1] = point;
}

CalibrationPoint ReadPoint(int id, int number)
{
	if (dataHandling.calibration == NULL || id < 0 || id >= SENSOR_AMOUNT || number < 0 || number >= CALIBRATION_POINTS)
	{
		CalibrationPoint point = { 0, 0.0f };
		return point;
	}
	return dataHandling.calibration->points[id][number];
}

int ReadCalibration(const char* path)
{
	return CreateCalibration(path);;
}

int WriteCalibration()
{
	//WIP
	return 0;
}

int CreateCalibration(const char* path)
{
	SensorCalibration* new = malloc(sizeof(SensorCalibration));
	if (new == NULL) return 0;
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(SensorCalibration); i++) bytePtr[i] = 0;
	strcpy_s(new->calibrationFilePath, PATH_LENGTH, path);
	CalibrationPoint temp = { 0, 0.0f };
	for (int i = 0, j = 0; i < SENSOR_AMOUNT; i++)
		for (j = 0; j < CALIBRATION_POINTS; j++)
			new->points[i][j] = temp;
	dataHandling.calibration = new;
	return 1;
}

int Initialize(const char path[])
{
	ReadFailSafe();
	if (dataHandling.failSafe == NULL) CreateFailSafe();
	int readExisting = 1;
	if (dataHandling.failSafe == NULL) readExisting = 0;
	else readExisting = !(dataHandling.failSafe->nominalExit) && dataHandling.failSafe->saveFilePath[0] != '\0';
	if (readExisting) ReadSave(dataHandling.failSafe->saveFilePath);
	else CreateSave(path);
	if (dataHandling.saveFile == NULL) {
		VirtualSave();
		if (dataHandling.failSafe != NULL) strcpy_s(dataHandling.failSafe->saveFilePath, PATH_LENGTH, "");
	}
	else if (!readExisting & (dataHandling.failSafe != NULL)) strcpy_s(dataHandling.failSafe->saveFilePath, PATH_LENGTH, path);
	CreateBuffer();
	CreateCalibration((dataHandling.failSafe == NULL)? "" : dataHandling.failSafe->calPath);
	_CreateFrameLookUp_();
	_SetPositions_();
	_CreateHandler_();
	_ConfigurePort_();
	return 1;
}

DataFrame CreateFrame(uint16_t sync)
{
	DataFrame temp = { 0 };
	char* bytePtr = (char*) & temp;
	for (int i = 0; i < sizeof(DataFrame); i++) bytePtr[i] = 0;
	if (sync != 0) temp.sync = sync;
	return temp;
}

DataFrame CreateTC(uint16_t sync)
{
	DataFrame temp = CreateFrame(sync);
	AddFlag(&temp, TeleCommand);
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

static int _SetPositions_()
{
	if (dataHandling.frameLookUp == NULL) return -1;
	int pos = 0;
	int length = 0;
	int id = 0;
	for (; id < TELEMETRY_AMOUNT; id++) {
		if ((id >= 0) & (id < SENSOR_AMOUNT)) length = BASE_RES;
		if ((id >= SENSOR_AMOUNT) & (id < TELEMETRY_AMOUNT)) length = 1;
		switch (id) {
			case Compare_Temperature:
			case Chamber_Pressure:
			case Nozzle_Pressure_1:
			case Nozzle_Pressure_2:
			case Nozzle_Pressure_3:
			case Nozzle_Temperature_1:
			case Nozzle_Temperature_2:
			case Nozzle_Temperature_3: length = HIGH_RES; break;
			case Nozzle_Servo:
			case Sensorboard_1:
			case Sensorboard_2: length = 2; break;
			case Mainboard: length = 4; break;
			case System_Time: length = 32; break;
		}
		dataHandling.frameLookUp->telemetry_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telemetry_Pos_Len[id][1] = length;
		pos += length;
		if (pos >= DATA_LENGTH * 8) return 0;
	}
	for (id = 0, pos = 0; id < TELECOMMAND_AMOUNT; id++) {
		if ((id >= 0) & (id < TELECOMMAND_AMOUNT)) length = 2;
		switch (id) {
			case Valve_Delay:
			case Servo_Delay:
			case EoE_Delay:
			case Power_Off_Delay:
			case Nozzle_On_Delay: 
			case Servo_Control: length = 32; break;
		}
		dataHandling.frameLookUp->telecommand_Pos_Len[id][0] = pos;
		dataHandling.frameLookUp->telecommand_Pos_Len[id][1] = length;
		pos += length;
		if (pos >= DATA_LENGTH * 8) return 0;
	}
	return 1;
}

static int _SetDCB_()
{
	if (dataHandling.handler == NULL) return 0;
	FillMemory(&(dataHandling.handler->dcb), sizeof(dataHandling.handler->dcb), 0);
	dataHandling.handler->dcb.DCBlength = sizeof(dataHandling.handler->dcb);
	if (!BuildCommDCB("9600,n,8,1", &(dataHandling.handler->dcb))) return 0;
	return 1;
}

static int _ConfigurePort_()
{
	if (!0) {
		if (dataHandling.handler == NULL) return 0;
		dataHandling.handler->comHandle = CreateFile(dataHandling.handler->comPath, GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, 0, NULL);
		if (dataHandling.handler->comHandle != INVALID_HANDLE_VALUE)
			if (!_SetDCB_(dataHandling.handler))
				if (!SetCommState(dataHandling.handler->comHandle, &(dataHandling.handler->dcb))) return 1;
	}
	return 0;
}

int _CreateHandler_()
{
	if (dataHandling.handler != NULL) free(dataHandling.handler);
	dataHandling.handler = malloc(sizeof(PortHandler));
	if (dataHandling.handler == NULL) return -1;
	char* bytePtr = (char*) dataHandling.handler;
	for (int i = 0; i < sizeof(PortHandler); i++) {
		bytePtr[i] = 0;
	}
	if (dataHandling.failSafe != NULL) 
		strcpy_s(dataHandling.handler->comPath, PATH_LENGTH, dataHandling.failSafe->comPath);
	else return 0;
	return 1;
}

int _CreateFrameLookUp_()
{
	if (dataHandling.frameLookUp != NULL) free(dataHandling.frameLookUp);
	dataHandling.frameLookUp = malloc(sizeof(FrameLookUpTable));
	if (dataHandling.frameLookUp == NULL) return 0;
	char* bytePtr = (char*)dataHandling.frameLookUp;
	for (int i = 0; i < sizeof(FrameLookUpTable); i++)
		bytePtr[i] = 0;
	return 1;
}

int WriteFrame(DataFrame* frame, int id, int value)
{
	if (frame == NULL || dataHandling.frameLookUp == NULL) return 0;
	int TC = FrameIsTC(*frame);
	if (TC & (id >= TELECOMMAND_AMOUNT) || id >= TELEMETRY_AMOUNT) return 0;
	int index = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][0] : dataHandling.frameLookUp->telemetry_Pos_Len[id][0];
	int length = (TC) ? dataHandling.frameLookUp->telecommand_Pos_Len[id][1] : dataHandling.frameLookUp->telemetry_Pos_Len[id][1];
	if (value < 0 || value >= 1 << length) return 0;
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
	if (dataHandling.frameLookUp == NULL) return 0;
	int TC = FrameIsTC(frame);
	if (TC & (id >= TELECOMMAND_AMOUNT) || id >= TELEMETRY_AMOUNT) return 0;
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
	return HasFlag(frame, TeleCommand);
}

int HasFlag(DataFrame frame, int id)
{
	//WIP
	return 0;
}

void AddFlag(DataFrame* frame, int id)
{
	//WIP
}

int Send()
{
	if (dataHandling.handler == NULL || dataHandling.buffer == NULL) return -1;
	int number = 0;
	if (WriteFile(dataHandling.handler->comHandle, dataHandling.buffer->outgoingPos, dataHandling.buffer->outgoingBytes, &number, NULL))
	{
		dataHandling.buffer->outgoingBytes -= number;
		dataHandling.buffer->outgoingPos += number;
		return number;
	}
	return -1;
}

int Receive()
{
	if (dataHandling.handler == NULL || dataHandling.buffer == NULL) return -1;
	int number = 0;
	if (ReadFile(dataHandling.handler->comHandle, dataHandling.buffer->incomingPos, PACKET_LENGTH, &number, NULL))
	{
		dataHandling.buffer->incomingPos += number;
		dataHandling.buffer->incomingBytes += number;
		return number;
	}
	return -1;
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
	if (dataHandling.buffer == NULL) return 0;
	DataPacket currentPacket; 
	DataFrame currentFrame = GetOutFrame();
	int number = 0;
	int id, payloadIndex, dataIndex;
	for (; !FrameIsEmpty(currentFrame); currentFrame = GetOutFrame(), number++) {
		for (id = 0; id <= 255; id++) {
			currentPacket = CreatePacket(currentFrame.sync);
			currentPacket.mode = ONBOARD;
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
	if (dataHandling.buffer == NULL) return 0;
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
	if (dataHandling.buffer == NULL) return EmptyPacket();
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
	if (dataHandling.buffer == NULL) return EmptyPacket();
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
	if (dataHandling.buffer == NULL) return EmptyFrame();
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
	if (dataHandling.buffer == NULL) return EmptyFrame();
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
	if (dataHandling.buffer == NULL) return -1;
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
	if (dataHandling.buffer == NULL) return -1;
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
	if (dataHandling.buffer == NULL) return -1;
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
	if (dataHandling.buffer == NULL) return -1;
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
	DataBuffer* new = (DataBuffer*) malloc(sizeof(DataBuffer));
	if (new == NULL) return 0; 
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(DataBuffer); i++) bytePtr[i] = 0;
	dataHandling.buffer = new;
	return 1;
}

int CreateFailSafe() 
{
	FailSafe* new = (FailSafe*) malloc(sizeof(FailSafe));
	if (new == NULL) return 0;
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(FailSafe); i++) bytePtr[i] = 0;
	new->conn = 'a';
	new->lang = 'e';
	new->dateTime = time(NULL);
	new->version = VERSION;
	new->mode = 'f';
	strcpy_s(new->comPath, PATH_LENGTH, DEFAULTCOMPATH);
	FILE* file;
	fopen_s(&file, FAILSAFENAME, "w");
	if (file != NULL) {
		fprintf(file, "Version: %i;\n", VERSION);
		fprintf(file, "Datetime: %lli;\n\n", new->dateTime);
		fprintf(file, "Savefile: %s;\n", new->saveFilePath);
		fprintf(file, "Complete: %c;\n\n", (new->complete) ? 'y' : 'n');
		fprintf(file, "Regular Exit: No;\n\n");
		fprintf(file, "Mode: %c;\n", new->mode);
		fprintf(file, "Connection: %c;\n", new->conn);
		fprintf(file, "Language: %c;", new->lang);
		fclose(file);
	}
	dataHandling.failSafe = new;
	return 1;
}

int ReadFailSafe()
{
	//WIP
	return 0;
}

int UpdateFailSafe()
{
	//WIP
	return 0;
}

int VirtualSave()
{
	SaveFile* new = (SaveFile*) malloc(sizeof(SaveFile));
	if (new == NULL) return 0;
	char* bytePtr = (char*) new;
	for (int i = 0; i < sizeof(SaveFile); i++) bytePtr[i] = 0;
	new->dateTime = time(NULL);
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = -1;
	new->saveFilePath[0] = '\0';
	new->version = VERSION;
	DataFrame* tc = (DataFrame*)malloc(sizeof(DataFrame));
	if (tc == NULL) return 0;
	new->currentTC = tc;
	*tc = CreateTC(0);
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
	if (dataHandling.saveFile == NULL || index >= dataHandling.saveFile->frameAmount) return NULL;
	if (index < 0) return dataHandling.saveFile->lastFrame;
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
	//WIP
	return EmptyFrame();
}

SaveFileFrame* AddSaveFrame(DataFrame data)
{
	if (dataHandling.saveFile == NULL) return NULL;
	SaveFileFrame* newFrame = (SaveFileFrame*) malloc(sizeof(SaveFileFrame));
	if (newFrame == NULL) return NULL;
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
	if (dataHandling.saveFile == NULL) return NULL;
	DataFrame data = CreateFrame(sync);
	return AddSaveFrame(data);
}

void CloseSave()
{
	SaveFileFrame* current = dataHandling.saveFile->lastFrame;
	SaveFileFrame* next = current->previousFrame;
	if (next != NULL) {
		for (; next != dataHandling.saveFile->firstFrame; next = current->previousFrame) {
			free(current);
			current = next;
		}
	}
	dataHandling.saveFile->lastFrame = NULL;
	free(dataHandling.saveFile->firstFrame);
	dataHandling.saveFile->firstFrame = NULL;
	free(dataHandling.saveFile->currentTC);
	dataHandling.saveFile->currentTC = NULL;
	dataHandling.saveFile->frameAmount = 0;
}

void CloseAll()
{
	free(dataHandling.buffer);
	free(dataHandling.calibration);
	free(dataHandling.failSafe);
	free(dataHandling.frameLookUp);
	CloseHandle(dataHandling.handler->comHandle);
	free(dataHandling.handler);
	CloseSave(dataHandling.saveFile);
	free(dataHandling.saveFile);
	dataHandling.buffer = NULL;
	dataHandling.calibration = NULL;
	dataHandling.failSafe = NULL;
	dataHandling.frameLookUp = NULL;
	dataHandling.handler = NULL;
	dataHandling.saveFile = NULL;
}

int WriteSave()
{
	//WIP
	return 0;
}

int CreateSave(const char path[])
{
	VirtualSave();
	if (dataHandling.saveFile == NULL) return 0;
	dataHandling.saveFile->savedAmount = 0;
	FILE* file;
	if (path != NULL) {
		fopen_s(&file, path, "wb");
		strcpy_s(dataHandling.saveFile->saveFilePath, PATH_LENGTH, path);
	}
	else {
		file = NULL;
	}
	if (file != NULL) {
		fprintf(file, "%c", VERSION);
		fwrite(&(dataHandling.saveFile->dateTime), sizeof(time_t), 1, file);
		fprintf(file, "%c", 255);
		fclose(file);
	}
	else {
		free(dataHandling.saveFile);
		dataHandling.saveFile = NULL;
		return 0;
	}
	return 1;
}