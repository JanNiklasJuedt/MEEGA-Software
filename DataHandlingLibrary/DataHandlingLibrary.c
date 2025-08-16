//Source File of DataHandlingLibrary
#include "pch.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include "DataHandlingLibrary.h"

//INTERNAL, Looks up values to be used by the ReadFrame() and WriteFrame() operations
static void _GetPosition_(int id, int* index, unsigned char* bit, unsigned char* length);

//Implementations:

int CalculateChecksum(char data[])
{
	//WIP
	return 1;
}
int CalculateCRC(char data[])
{
	//WIP
	return 0;
}

int Update(StorageHub* storage)
{
	//WIP
	return 0;
}

StorageHub Initialize(const char path[])
{
	StorageHub new = {NULL, NULL, NULL};
	FailSafe* failsafe = ReadFailSafe();
	if (failsafe == NULL) failsafe = CreateFailSafe();
	new.failSafe = failsafe;
	SaveFile* savefile;
	int readExisting;
	if (failsafe == NULL) readExisting = 0;
	else readExisting = !(new.failSafe->nominalExit) && new.failSafe->saveFilePath[0] != '\0';
	if (readExisting) savefile = ReadSave(new.failSafe->saveFilePath);
	else savefile = CreateSave(path);
	if (savefile == NULL) {
		savefile = VirtualSave();
		if (failsafe != NULL) strcpy_s(new.failSafe->saveFilePath, PATHLENGTH, "");
	}
	else if (!readExisting & (failsafe != NULL)) strcpy_s(new.failSafe->saveFilePath, PATHLENGTH, path);
	new.saveFile = savefile;
	new.buffer = CreateBuffer();
	return new;
}

DataFrame CreateFrame(int16_t sync)
{
	DataFrame temp = { .sync = sync };
	return temp;
}

DataFrame CreateTC(int16_t sync)
{
	DataFrame temp = { .sync = sync, .flag = TeleCommand + Source};
	return temp;
}

static void _GetPosition_(int id, int* index, unsigned char* bit, unsigned char* length)
{
	//TBC
	switch (id) {
	case AmbientPressure: *index = 0, *length = 2;
	case HHAmbientPressure: *index = 32, *bit = 8, *length = 1;
	case CompareTemperature: *index = 2, *length = 3;
	case HHCompareTemperature: *index = 32, *bit = 7, *length = 1;
	}
	return;
}

int WriteFrame( DataFrame* frame, int id, int value)
{
	char former32[4] = { 0,0,0,0 };
	char value32[4] = { 0,0,0,0 };
	memcpy(value32, &value, 4);
	int index = 0;
	char bit = 0;
	char length = 0;
	_GetPosition_(id, &index, &bit, &length);
	if (bit == 0) {
		for (int i = 0; i < length; i++) {
			former32[i] = frame->data[index + i];
			frame->data[index + i] = value32[i];
		}
	}
	else {
		former32[0] = frame->data[index];
		former32[0] >>= bit - length;
		former32[0] %= 1 << length;
		frame->data[index] -= former32[0] << (bit - length);
		frame->data[index] += value << (bit - length);
	}
	int former = 0;
	memcpy(&former, former32, 4);
	return former;
}

int WriteTC(DataFrame* tc, int id, int value)
{
	//WIP
	return 0;
}

int ReadFrame( DataFrame* frame, int id)
{
	int value = 0;
	int index = 0;
	char bit = 0;
	char length = 0;
	_GetPosition_(id, &index, &bit, &length);
	if (bit == 0) {
		for (int i = 1; i <= length; i++) {
			value += (frame->data[index + length - i]) << (i * sizeof(char));
		}
	}
	else {
		value = frame->data[index];
		value >>= bit - length;
		value %= 1 << length;
	}
	return value;
}

int ReadTC(DataFrame* tc, int id)
{
	//WIP
	return 0;
}

int FrameIsEmpty(DataFrame* frame) 
{
	return frame->sync == 0;
}

int FrameIsTC(DataFrame* frame)
{
	//WIP
	return 0;
}

static DataPacket CreatePacket(int16_t sync)
{
	DataPacket out = { .sync = sync };
	return out;
}

unsigned char* WritePacket(DataPacket outgoingData)
{
	//WIP
	return NULL;
}

DataPacket ReadPacket(unsigned char* incomingData)
{
	//WIP
	return CreatePacket(0);
}

int FormPackets(DataBuffer* buffer)
{
	DataFrame currentFrame = GetBufferFrame(buffer);
	DataPacket currentPacket;
	unsigned char id;
	unsigned char number = 0;
	for (; !FrameIsEmpty(&currentFrame); currentFrame = GetBufferFrame(buffer), number++) {
		currentPacket = CreatePacket(currentFrame.sync);
		for (id = 0; id <= 100; id++) {

		}
	}
	return number;
}

int FormFrames(DataBuffer* buffer)
{
	//WIP
	return 0;
}

DataPacket GetOutPacket(DataBuffer* buffer)
{
	DataPacket temp = CreatePacket(0);
	for (int i = BUFFERLENGTH; i > 0; i--) {
		temp = buffer->outgoing[i - 1];
		if (temp.sync != 0) {
			buffer->outgoing[i - 1] = CreatePacket(0);
		}
	}
	return temp;
}

DataPacket GetInPacket(DataBuffer* buffer)
{
	DataPacket temp = CreatePacket(0);
	for (int i = BUFFERLENGTH; i > 0; i--) {
		temp = buffer->incoming[i - 1];
		if (temp.sync != 0) {
			buffer->incoming[i - 1] = CreatePacket(0);
		}
	}
	return temp;
}

DataFrame GetBufferFrame(DataBuffer* buffer)
{
	DataFrame temp = CreateFrame(0);
	for (int i = BUFFERLENGTH; i > 0; i--) {
		temp = buffer->frameStack[i - 1];
		if (temp.sync != 0) {
			buffer->frameStack[i - 1] = CreateFrame(0);
		}
	}
	return temp;
}

int AddBufferFrame(DataBuffer* buffer, DataFrame frame)
{
	int number = 0;
	for (; number <= BUFFERLENGTH; number++) {
		if (buffer->frameStack[number].sync == 0) {
			buffer->frameStack[number] = frame;
			break;
		}
	}
	return number + 1;
}

DataFrame GetBufferTC(DataBuffer* buffer)
{
	//WIP
	return CreateTC(0);
}

int AddBufferTC(DataBuffer* buffer, DataFrame frame)
{
	//WIP
	return 0;
}

DataBuffer* CreateBuffer()
{
	DataBuffer* temp = (DataBuffer*) malloc(sizeof(DataBuffer));
	if (temp == NULL) return NULL;
	for (int i = 0; i < 10; i++) {
		temp->frameStack[i] = CreateFrame(0);
		temp->incoming[i] = CreatePacket(0);
		temp->outgoing[i] = CreatePacket(0);
		temp->TCStack[i] = CreateTC(0);
	}
	return temp;
}

int AddInPacket(DataBuffer* buffer, DataPacket data)
{
	int number = 0;
	for (; number <= BUFFERLENGTH; number++) {
		if (buffer->incoming[number].sync == 0) {
			buffer->incoming[number] = data;
			break;
		}
	}
	return number + 1;
}

int AddOutPacket(DataBuffer* buffer, DataPacket data)
{
	int number = 0;
	for (; number <= BUFFERLENGTH; number++) {
		if (buffer->outgoing[number].sync == 0) {
			buffer->outgoing[number] = data;
			break;
		}
	}
	return number + 1;
}

FailSafe* CreateFailSafe() 
{
	FailSafe* new = (FailSafe*) malloc(sizeof(FailSafe));
	if (new == NULL) return NULL;
	new->complete = 0;
	new->conn = 'a';
	new->lang = 'e';
	new->dateTime = time(NULL);
	new->nominalExit = 0;
	new->saveFilePath[0] = '\0';
	new->version = VERSION;
	new->mode = 'f';
	new->conn = '\0';
	new->lang = '\0';
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
	return new;
}

FailSafe* ReadFailSafe()
{
	//WIP
	return NULL;
}

int UpdateFailSafe(FailSafe* failsafe)
{
	//WIP
	return 0;
}

SaveFile* VirtualSave()
{
	SaveFile* new = (SaveFile*) malloc(sizeof(SaveFile));
	if (new == NULL) return NULL;
	new->dateTime = time(NULL);
	new->firstFrame = NULL;
	new->lastFrame = NULL;
	new->frameAmount = 0;
	new->savedAmount = -1;
	new->saveFilePath[0] = '\0';
	new->version = VERSION;
	DataFrame* tc = (DataFrame*)malloc(sizeof(DataFrame));
	if (tc == NULL) return NULL;
	new->currentTC = tc;
	*tc = CreateTC(0);
	return new;
}

int CheckSave(SaveFile* savefile)
{
	//WIP
	return 0;
}

SaveFile* ReadSave(const char path[])
{
	//WIP
	return NULL;
}

SaveFileFrame* GetSaveFrame(SaveFile* savefile, int index)
{
	if (index >= savefile->frameAmount)	return NULL;
	if (index < 0) return savefile->lastFrame;
	SaveFileFrame* frame = savefile->firstFrame;
	for (int i = 0; i < index; i++) {
		if (frame == NULL) return NULL;
		if (frame->nextFrame == NULL) return frame;
		frame = frame->nextFrame;
	}
	return frame;
}

DataFrame* UpdateTC(SaveFile* savefile)
{
	//WIP
	return NULL;
}

SaveFileFrame* AddSaveFrame(SaveFile* savefile, DataFrame data)
{
	SaveFileFrame* newframe = (SaveFileFrame*) malloc(sizeof(SaveFileFrame));
	if (newframe == NULL) return NULL;
	newframe->data = data;
	newframe->nextFrame = NULL;
	if (savefile->firstFrame == NULL) {
		savefile->firstFrame = newframe;
		savefile->lastFrame = newframe;
		savefile->frameAmount = 1;
	}
	else {
		savefile->lastFrame->nextFrame = newframe;
		savefile->lastFrame = newframe;
		savefile->frameAmount++;
	}
	return savefile->lastFrame;
}

SaveFileFrame* CreateSaveFrame(SaveFile* savefile, int16_t sync)
{
	DataFrame data = CreateFrame(sync);
	return AddSaveFrame(savefile, data);
}

int WriteSave(SaveFile* savefile)
{
	//WIP
	return 0;
}

SaveFile* CreateSave(const char path[])
{
	SaveFile* new = VirtualSave();
	new->savedAmount = 0;
	FILE* file;
	if (path != NULL) {
		fopen_s(&file, path, "wb");
		strcpy_s(new->saveFilePath, PATHLENGTH, path);
	}
	else {
		file = NULL;
	}
	if (file != NULL) {
		fprintf(file, "%c", VERSION);
		fwrite(&(new->dateTime), sizeof(time_t), 1, file);
		fprintf(file, "%c", EOL);
		fclose(file);
	}
	else {
		free(new);
		return NULL;
	}
	return new;
}