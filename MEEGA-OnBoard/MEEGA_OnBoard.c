#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <pthread.h>

#define DEBUG
#ifdef DEBUG

#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define INPUT 0

//DEBUG for GPIO control from RaspberryPi
static inline void pinMode(int pin, int mode) {
	char *pinStr = " ", *modeStr = " ";
	switch (pin) {
	case 54: pinStr = "LEDs"; break;
	case 29: pinStr = "Reservoir_Valve"; break;
	case 01: pinStr = "ValveSwitch"; break;
	case 34: pinStr = "Nozzle_Servo"; break;
	case 50: pinStr = "ServoSwitch_1"; break;
	case 48: pinStr = "ServoSwitch_2"; break;
	case 41: pinStr = "RPi_SOE"; break;
	case 47: pinStr = "RPi_LO";break;
	default: break;
	}
	switch (mode) {
	case 1: modeStr = "OUTPUT"; break;
	case 0: modeStr = "INPUT"; break;
	default: break;
	}
	printf("[DEBUG] Pin %d (%s) set to mode %d (%s)\n", pin, pinStr, mode, modeStr);
}
static inline void digitalWrite(int pin, int value) {
	char* pinStr = " ", * modeStr = " ";
	switch (pin) {
	case 54: pinStr = "LEDs"; break;
	case 29: pinStr = "Reservoir_Valve"; break;
	case 34: pinStr = "Nozzle_Servo"; break;
	default: break;
	}
	switch (value) {
	case 1: modeStr = "HIGH"; break;
	case 0: modeStr = "LOW"; break;
	default: break;
	}
	printf("[DEBUG] Pin %d (%s) set to value %d (%s)\n", pin, pinStr, value, modeStr);
}
static inline int digitalRead(int pin) {
	char* pinStr = " ";
	switch (pin) {
	case 01: pinStr = "ValveSwitch"; break;
	case 50: pinStr = "ServoSwitch_1"; break;
	case 48: pinStr = "ServoSwitch_2"; break;
	case 41: pinStr = "RPi_SOE"; break;
	case 47: pinStr = "RPi_LO";break;
	default: break;
	}
	printf("[DEBUG] Reading value from pin %d (%s)\n", pin, pinStr);
	return LOW;	//return LOW for debug testing
}

static inline void softPwmWrite(int pin,int Value) {
	char* pinStr = " ", * modeStr = " ";
	switch (pin) {
	case 34: pinStr = "Nozzle_Servo"; break;
	default: break;
	}
	printf("[DEBUG] Pin %d (%s) set to value %d degree (%s)\n", pin, pinStr, Value, modeStr);
}
static inline void softPwmCreate(int pin, int startValue, int endValue) {
	char* pinStr = " ";
	switch (pin) {
	case 34: pinStr = "Nozzle_Servo"; break;
	default: break;
	}
	printf("[DEBUG] Create PWM value from pin %d (%s), Range Value %d - %d\n", pin, pinStr, startValue, endValue);
}

//DEBUG for I2C and SPC Sersors Reading
static inline int analogRead(int pin) { 
	printf("[DEBUG] Reading analog value from pin %d\n", pin);
	return 0;	//return 0 for debug testing
}
#else
#include "DataHandlingLibrary.h"
#include <wiringPi.h>	//Include wiringPi library for GPIO control
#include <softPwm.h>	//Include softPwm library for PWM control
#endif

#define LEDs 54	//pin
#define Reservoir_Valve 29	//pin
#define ValveSwitch 01	//pin
#define Nozzle_Servo 34	//pin
#define ServoSwitch_1 50	// Deckel ganz zu Feedback
#define ServoSwitch_2 48	// Deckel ganz auf Feedback

#define RPi_SOE 41	//pin
#define RPi_LO 47	//pin


//#########################################################################################################################################################//
//################################################################## PROGRAM STARTS HERE ##################################################################//
//#########################################################################################################################################################//
int SoESignal() {
#ifdef DEBUG
	int SoE;
	printf("*SoE Signal? 1 for YES, 0 for NO: "); scanf_s("%d", &SoE);
	if (SoE == 1) return (digitalRead(RPi_SOE) == 0);
	else return (digitalRead(RPi_SOE) == 1);
#else
	return (digitalRead(RPi_SOE) == LOW);	//Check if SoE signal is HIGH, if so, start experiment. change to HIGH if connected to RaspberryPi
#endif
}

struct params {
	char Mode[10];
	int ValveDelay, ServoDelay, EoEDelay, PoweroffDelay, FDA20, FDA2, NozzleOnCDelay, NoseConeSeparation, AfterLO; //FDA here is frames = frequency x duration. With FullData 20Hz & BasicData 2Hz
};
struct params flightstandard = { .Mode = "Flight", .NoseConeSeparation = 10000, .AfterLO = 55000, .ValveDelay = 5000, .ServoDelay = 6000, .EoEDelay = 30000, .PoweroffDelay = 1000, .NozzleOnCDelay = 1000, .FDA20 = 500};
struct params teststandard = { .Mode = "Test", .ValveDelay = 5000, .ServoDelay = 6000, .EoEDelay = 30000, .PoweroffDelay = 1000, .FDA2 = 5000};
struct params DEBUGstandard = { .Mode = "Debug", .AfterLO = 5000, .EoEDelay = 3000 };

int testAbort = 0;

int delay(int millisecond) {	//1000x Second
	clock_t start_time = clock();
	clock_t wait_time = (millisecond * CLOCKS_PER_SEC) / 1000;
	while (clock() < start_time + wait_time) if(testAbort) return 1;
	return 0;
}

void ServoRotation(int degree) {
	if (degree < 0) degree = 0;
	if (degree > 360) degree = 360;
	int pwmValue = (degree * 100) / 360;	//Convert degree to PWM value (0-100)???????
	softPwmWrite(Nozzle_Servo, pwmValue);
}

//########################################################################################################################################################//
//################################################################## EXPERIMENT PROGRAM ##################################################################//
//########################################################################################################################################################//

int ValveOpen = 1, ValveClose = 0, ValveStuck = 3, valveStatus = 0, ValvePos = 0, ValveComplete = 0, ServoRun = 1, ServoStop = 0, ServoStuck = 3, servoStatus = 0, nozzleStatus = 0, NozzleStuck = 3, NozzlePos = 0, NozzleOpen = 1, EoE = 0, SoE = 0, LO = 0, ExperimentStatus;

int ExperimentRun(struct params parameter) {
	digitalWrite(LEDs, 1);	//LED on
	ExperimentStatus = 2;	//Experiment started
	digitalWrite(Reservoir_Valve,ValveOpen);	//command open valve
#ifdef DEBUG
	printf("Command opening Valve\n");
	ValvePos = digitalRead(ValveSwitch);		//Feedback signal
	printf("*Input Valve 1 for open, 0 for close (std: open): "); scanf_s("%d", &ValvePos); //scanf_s is just for safety and used only in debug mode in visual studio
#else
	ValvePos = ValveOpen;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveOpen) {
		//Valve is open			
#ifdef DEBUG
		printf("Valve Status: Valve is open\n");
#else
		valveStatus = ValveOpen;
#endif
		delay(parameter.ValveDelay);
	}
	else if (ValvePos == ValveClose) {//Valve error: in close position
#ifdef DEBUG
		printf("Valve Status: Valve is stuck in close position\n");
#else
		valveStatus = ValveStuck;
#endif
		if (strcmp(parameter.Mode, "Test") == 0) {
#ifdef DEBUG
			printf("Valve Error Code 1, Return ...\n");
#else
			ExperimentStatus = 4;
#endif
			return 1;//abort test
		}
	}
	digitalWrite(Reservoir_Valve, ValveClose);	//command close valve
#ifdef DEBUG
	printf("Command closing Valve\n");
	printf("*Input Valve 1 for open, 0 for close (std: close): "); scanf_s("%d", &ValvePos);
#else
	ValvePos = ValveClose;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveClose) {
		//Valve is close
#ifdef DEBUG
		printf("Valve Status: Valve is close\n");
#else
		valveStatus = ValveClose;
		ValveComplete = 1; //Valve operation complete
#endif
		delay(parameter.ServoDelay);
	}
	else if (ValvePos = ValveOpen) {
		//Valve error: in open position / cont. error
#ifdef DEBUG
		printf("Valve Status: Valve is stuck in open position\n");
#else
		valveStatus = ValveStuck;
#endif
		if (strcmp(parameter.Mode, "Test") == 0) {
#ifdef DEBUG
			printf("Valve Error Code 2, Return ...\n");
#else
			ExperimentStatus = 4;
#endif
			return 2;//abort test
		}
	}
	if (strcmp(parameter.Mode, "Flight") == 0) {
		ServoRotation(90); //command rotate the serve 90°
#ifdef DEBUG
		printf("Command to run Servo\n");
		printf("Servo run for 90 Degree\n");
#endif
		delay(parameter.NozzleOnCDelay);
#ifdef DEBUG
		printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
		if (NozzlePos == 1) {
#else
		if (NozzlePos == digitalRead(ServoSwitch_2)) {
#endif
			//Feedback signal
			//Nozzle Cover Problem: in close position
#ifdef DEBUG
			printf("Nozzle Cover is open\n");
#else
			nozzleStatus = NozzleOpen;
#endif
#ifdef DEBUG
			delay(DEBUGstandard.EoEDelay);
#else
			delay(parameter.EoEDelay);
#endif
			digitalWrite(LEDs, 0);			//LED off
			EoE = 1; //Successful End of Experiment
		}
#ifdef DEBUG
		else if (NozzlePos == 0) {
#else
		else if (NozzlePos == digitalRead(ServoSwitch_1)) {
#endif
			//Nozzle Cover Problem: in close position
			ServoRotation(180);
#ifdef DEBUG
			printf("Second attempt\n");
			printf("Servo run for 180 Degree\n");
			printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
#endif
			delay(parameter.NozzleOnCDelay);
#ifdef DEBUG
			if (NozzlePos == 1) {
#else
			if (NozzlePos == digitalRead(ServoSwitch_2)) {
#endif
#ifdef DEBUG
				printf("Nozzle Cover is open\n");
#else
				nozzleStatus = NozzleOpen;
#endif
#ifdef DEBUG
				delay(DEBUGstandard.EoEDelay);
#else
				delay(parameter.EoEDelay);
#endif
				digitalWrite(LEDs, 0);			//LED off
				EoE = 1; //Successful End of Experiment
			}
			else {
#ifdef DEBUG
				printf("Nozzle Cover is stuck in close position\n");
#else
				nozzleStatus = NozzleStuck;
				ExperimentStatus = 4;
#endif
				if (strcmp(parameter.Mode, "Test") == 0) {
#ifdef DEBUG
					printf("Nozzle Error Code 3, Return ...\n");
#else
					ExperimentStatus = 4;
#endif
					return 3;//abort test
				}
			}
		}
	}
	else if (strcmp(parameter.Mode, "Test") == 0) {
#ifdef DEBUG
		printf("Simulating nozzle cover open\n");
#else
		nozzleStatus = NozzleOpen;				//simulate nozzle cover open
#endif
#ifdef DEBUG
		delay(DEBUGstandard.EoEDelay);
#else
		delay(parameter.EoEDelay);
#endif
		digitalWrite(LEDs, 0);
		nozzleStatus = 0;						//Reset simulation of nozzle cover open
#ifndef DEBUG
		ExperimentStatus = 3;
#endif
		delay(parameter.PoweroffDelay);
	}
	if (EoE == 1) {
#ifdef DEBUG
		printf("Experiment: Successful\n");
#else
		ExperimentStatus = 3;
#endif
		delay(parameter.PoweroffDelay);
#ifdef DEBUG
		printf("End of Experiment: Successful\n");
#else
		ExperimentStatus = 5;
#endif
		return 43;	//End of Experiment
	}
	else {
#ifdef DEBUG
		printf("End of Experiment: Error\n");
#else
		ExperimentStatus = 4;
#endif
		delay(parameter.PoweroffDelay);
		return 404;	//Error in Experiment
	}
	return 0;
}


//###########################################################################################################################################################################//
//################################################################## START OF DATA ACQUISITION AND LOGGING ##################################################################//
//###########################################################################################################################################################################//

//Householding Data Acquisition
#define id_Ambient_Pressure 000
#define id_Compare_Temperature 001
#define id_Tank_Pressure 002
#define id_Tank_Temperature 003
#define id_Chamber_Pressure 004
#define id_Chamber_Temperature 005
#define id_Nozzle_Pressure_1 006
#define id_Nozzle_Pressure_2 026
#define id_Nozzle_Pressure_3 036
#define id_Nozzle_Temperature_1 007
#define id_Nozzle_Temperature_2 017
#define id_Nozzle_Temperature_3 027
#define id_Nozzle_Cover 48	//ServoSwitch_2
#define id_Nozzle_Servo 34	//Nozzle_Servo
#define id_Reservoir_Valve 010
#define id_LEDs 012
#define id_Sensorboard_1 013
#define id_Sensorboard_2 113
#define id_Mainboard 014 //RSPI
#define id_System_Time 015
#define id_Experiment_Status 016

void DataAcquisition(struct DataFrame* frame) {
#ifndef DEBUG
	int SystemTime = clock();	//System Time
	int AmbientPressure = analogRead(0);																//alle sensor daten etc lesen und in Data Handling int speichern. 2mode full & basic data acquisition. Hausholdong data speichern. 
	int CompareTemperature = analogRead(1);
	int TankPressure = analogRead(2);
	int TankTemperature = analogRead(3);
	int ChamberPressure = analogRead(4);
	int ChamberTemperature = analogRead(5);
	int NozzlePressure_1 = analogRead(6);
	int NozzlePressure_2 = analogRead(16);
	int NozzlePressure_3 = analogRead(26);
	int NozzleTemperature_1 = analogRead(7);
	int NozzleTemperature_2 = analogRead(17);
	int NozzleTemperature_3 = analogRead(27);
	int NozzleCover = digitalRead(ServoSwitch_2);	//Nozzle Cover Feedback: fully open
	int NozzleServo = digitalRead(Nozzle_Servo);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Reservoir_Valve);	//Reservoir Valve
	int LEDsStat = digitalRead(LEDs);
	int Sensorboard_1 = 0;		//Sensorboard is not implemented yet ?
	int Sensorboard_2 = 0;
	int Mainboard = 0;			//Mainboard is not implemented yet ?
	//Experiment Status CHECK!

	WriteFrame(frame, id_System_Time, SystemTime);
	WriteFrame(frame, id_Ambient_Pressure, AmbientPressure);
	WriteFrame(frame, id_Compare_Temperature, CompareTemperature);
	WriteFrame(frame, id_Tank_Pressure, TankPressure);
	WriteFrame(frame, id_Tank_Temperature, TankTemperature);
	WriteFrame(frame, id_Chamber_Pressure, ChamberPressure);
	WriteFrame(frame, id_Chamber_Temperature, ChamberTemperature);
	WriteFrame(frame, id_Nozzle_Pressure_1, NozzlePressure_1);
	WriteFrame(frame, id_Nozzle_Pressure_2, NozzlePressure_2);
	WriteFrame(frame, id_Nozzle_Pressure_3, NozzlePressure_3);
	WriteFrame(frame, id_Nozzle_Temperature_1, NozzleTemperature_1);
	WriteFrame(frame, id_Nozzle_Temperature_2, NozzleTemperature_2);
	WriteFrame(frame, id_Nozzle_Temperature_3, NozzleTemperature_3);
	WriteFrame(frame, id_Nozzle_Cover, NozzleCover);
	WriteFrame(frame, id_Nozzle_Servo, NozzleServo);
	WriteFrame(frame, id_Reservoir_Valve, ReservoirValve);
	WriteFrame(frame, id_LEDs, LEDsStat);
	WriteFrame(frame, id_Sensorboard_1, Sensorboard_1);
	WriteFrame(frame, id_Sensorboard_2, Sensorboard_2);
	WriteFrame(frame, id_Mainboard, Mainboard);
	WriteFrame(frame, id_Experiment_Status, ExperimentStatus);
}

void Log(struct StorageHub* storage) {
	struct params freq;
	int sync = 0;				//Sync value for the DataFrame
	int syncLimit = 0;			//Sync limit for the DataFrame, every 10 Frames a new Sync value is set

	while (1) {
		struct DataFrame frame = CreateFrame(sync++);
		DataAcquisition(&frame);	//DataAcquisition function to fill the frame with data
		AddSaveFrame(storage->saveFile, frame);	//Add the frame to the save file
		AddBufferFrame(storage->buffer, frame);	//Add the frame to the buffer
		syncLimit++;
		if (syncLimit >= 10) {
			FormPackets(storage->buffer);				//Form the packets from the buffer
			syncLimit = 0;								//Reset the sync limit
		}
		Update(storage);	//Update the storage hub, this will write the packets to the harddrive if necessary
		clock_t start = clock();
		if (SoESignal()) {
			clock_t end = clock();
			long duration = ((end - start)*1000)/CLOCKS_PER_SEC;
			int wait = freq.FDA20 - (int)duration;
			if (wait > 0) delay(wait); //Full Data Acquisition 20Hz
		}
		else {
			delay(freq.FDA2);		//Basic Data Acquisition 2Hz
		}
	}
}
void* LogThread(void* arg) {
	struct StorageHub* storage = (struct StorageHub*)arg;
	Log(storage);	//Start the logging function
	return NULL;	//Return NULL to end the thread
#endif
}


//BETA Control Panel Functions not yet implemented from DataHandling
int ExperimentControl() {
#ifndef DEBUG
	ExperimentStatus = 6;
	struct StorageHub* storage;
	while (1) {
		DataPacket cmdpacket = GetInPacket(storage->buffer);
		//Valve Control
		if (cmdpacket.sync != 0) {
			//DataFrame* TCFrame = (DataFrame*)&cmdpacket;	//Convert DataPacket to DataFrame

			//Valve Control
			if (ReadTC(id_Reservoir_Valve) == 1) digitalWrite(Reservoir_Valve, ValveOpen);	//command open valve
			else if (ReadTC(id_Reservoir_Valve) == 0) digitalWrite(Reservoir_Valve, ValveClose);	//command close valve

			//LEDs Control
			if (ReadTC(id_LEDs) == 1) digitalWrite(LEDs, ValveOpen);	//command open valve
			else if (ReadTC(id_LEDs) == 0) digitalWrite(LEDs, ValveClose);	//command close valve

			//Servo Control
			if (ReadTC(id_Nozzle_Servo) >= 0 && ReadTC(id_Nozzle_Servo) >= 180) ServoRotation(ReadTC(id_Nozzle_Servo));	//command rotate the servo to the specified degree
		}
	}
#endif
return 0;
}


//######################################################################################################################################################//
//################################################################## FAILSAFE PROGRAM ##################################################################//
//######################################################################################################################################################//

typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, VALVE_OPENED, EXPERIMENT_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;
int ValveOpened = 0;
int NozzleOpened = 0;
int experimentRunning = 0;

#ifndef DEBUG
void FailSafeRecovery(StorageHub* storage) {
	DataFrame lastFrame;
	if (ReadFrame(storage->saveFile, System_Time)) {
		currentState = lastFrame.currentState;
		ValveOpened = lastFrame.ValveOpened;
		NozzleOpened = lastFrame.NozzleOpened;
		experimentRunning = lastFrame.experimentRunning;
	}
	else {
		currentState = WAIT_LO;
		ValveOpened = 0;
		NozzleOpened = 0;
		experimentRunning = 0;
	}
}
#endif


//###########################################################################################################################################################//
//################################################################## START OF MAIN PROGRAM ##################################################################//
//###########################################################################################################################################################//
//START OF MAIN PROGRAM
int main() {
#ifdef DEBUG
	pinMode(Reservoir_Valve, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Nozzle_Servo, OUTPUT);
	pinMode(LEDs, OUTPUT);

	pinMode(ServoSwitch_1, INPUT);
	pinMode(ServoSwitch_2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);

	softPwmCreate(Nozzle_Servo, 0, 360); 	//Create a soft PWM on the Nozzle Servo pin with a range of 0-360 degrees

#else
	wiringPiSetupGpio();
	pinMode(Reservoir_Valve, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Nozzle_Servo, OUTPUT);
	pinMode(LEDs, OUTPUT);

	pinMode(ServoSwitch_1, INPUT);
	pinMode(ServoSwitch_2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);

	softPwmCreate(Nozzle_Servo, 0, 360); 	//Create a soft PWM on the Nozzle Servo pin with a range of 0-360 degrees

	pullUpDonControl(RPi_LO, PUD_DOWN);
	pullUpDonControl(RPi_SOE, PUD_DOWN);

	struct StorageHub storage = Initialize(NULL);
	FailSafeRecovery(&storage);
#endif
	//Idle: 0; LO: 1; Running SoE: 2; Success: 3; Failure: 4; EoE: 5; Experiment Contol Panel: 6 
	ExperimentStatus = 0;
	struct params config;

#ifndef DEBUG
	pthread_t logThread;
	//create a thread that runs LogThread function: success->parallel programm; failure->no threads logging and return to NULL
	//using if to let know if there is/are problem(s)
	if (pthread_create(&logThread, NULL, LogThread, (void*)&storage)) {	//Create a thread for logging
		digitalWrite(LEDs, 1);
		delay(5000);	//LED on for 5s then off: logging thread failed to start
		digitalWrite(LEDs, 0);
		return 1;
	}
#endif
	int EoECompleted = 0;

	while (!EoECompleted) {	
		//int flightmode = 1;
		//int testmode = 0;
		int LOSignal = digitalRead(RPi_LO);

#ifdef DEBUG
		int modeBit;
		printf("*Mode selection 1 for Flight, 0 for Test: "); scanf_s("%d", &modeBit);
#else
		struct DataPacket mode = GetInPacket(storage.buffer);	//get packet from buffer
		int modeBit = mode.mode;	//get mode bit from packet
#endif
		// Test Mode = 0, Flight Mode = 1

		if (modeBit == 1) {		//Flight Mode
			config = flightstandard;
#ifdef DEBUG
			printf("*LO Signal? 1 for YES, 0 for NO: "); scanf_s("%d", &LOSignal);
#endif
			if (LOSignal == 0) continue;

			currentState = WAIT_LO;
			ValveOpened = 0;
			NozzleOpened = 0;
			experimentRunning = 0;
			while(currentState != END_OF_EXPERIMENT) {
				switch (currentState) {
				case WAIT_LO:
					if (LOSignal == 1) {	//change to HIGH if connected to RaspberryPi
						currentState = AFTER_LO;
					}
					break;

				case AFTER_LO:
#ifdef DEBUG
					delay(DEBUGstandard.AfterLO);
#else
					ExperimentStatus = 1; //LO Signal received
					delay(config.AfterLO);	//Wait for 55s after liftoff
#endif
					currentState = NOSECONE_SEPARATION;
					break;

				case NOSECONE_SEPARATION:
					digitalWrite(LEDs, 1);	//LED on
#ifdef DEBUG
					printf("Nose Cone Separation\n");
#endif
					delay(config.NoseConeSeparation);			//Wait for Nozzle Cone Separation
					digitalWrite(LEDs, 0);	//LED off
					currentState = WAIT_SOE;
					break;

				case WAIT_SOE:
					while (!SoESignal()) {
						delay(100);
					}
					currentState = VALVE_OPENED;
					break;

				case VALVE_OPENED:
					currentState = EXPERIMENT_RUNNING;
					break;

				case EXPERIMENT_RUNNING:
					if (!NozzleOpened) {
						int ExperimentRunStatus = ExperimentRun(config);
						experimentRunning = 1;

						if (ExperimentRunStatus == 43 || ExperimentRunStatus == 404) {
							NozzleOpened = 1;
							currentState = END_OF_EXPERIMENT; //End of Experiment
						}
					}
					break;

				case NOZZLE_OPENED:
				case END_OF_EXPERIMENT:
					break;
				}
#ifndef DEBUG
				WriteSave(storage.saveFile);
#endif
			}
			EoECompleted = 1;
		}
		else if (modeBit == 0) {	//Test Mode							//Manuel abbrechen
			config = teststandard;
			//Test Mode
			digitalWrite(LEDs, 1);
			while (!SoESignal()) {
				delay(100);
			}
			int ExperimentRunStatus = ExperimentRun(config);

#ifndef DEBUG
			DataPacket cmdparam = GetInPacket(storage.buffer);
			if (cmdparam.sync != 0) {
				config.ValveDelay = cmdparam.payload[0] * 1000;	//Valve Delay in ms
				config.ServoDelay = cmdparam.payload[1] * 1000;	//Servo Delay in ms
				config.EoEDelay = cmdparam.payload[2] * 1000;	//End of Experiment Delay in ms
				config.PoweroffDelay = cmdparam.payload[3] * 1000;	//Power off Delay in ms
			}

			WriteSave(storage.saveFile);

			ExperimentStatus = 0;
#endif
			ExperimentControl();
			continue;
		}
	}
	return 0;
}
