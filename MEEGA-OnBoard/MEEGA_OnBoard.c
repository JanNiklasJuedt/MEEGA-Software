#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include "DataHandlingLibrary.h"

#define DEBUG
//Mode; SoE; LO; Valve; Nozzle Feedback: For DEBUG Test value must be 1, else 0
#define SERVO_WO_PWM
#ifdef DEBUG

#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define INPUT 0

//DEBUG for GPIO control from RaspberryPi
static inline void pinMode(int pin, int mode) {
	char *pinStr = " ", *modeStr = " ";
	switch (pin) {
	case 54: pinStr = "LEDs_Pin"; break;
	case 29: pinStr = "Valve_Pin"; break;
	case 01: pinStr = "ValveSwitch"; break;
	case 34: pinStr = "Servo_Pin"; break;
	case 50: pinStr = "Nozzle_Cover_1"; break;
	case 48: pinStr = "Nozzle_Cover_2"; break;
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
	case 54: pinStr = "LEDs_Pin"; break;
	case 29: pinStr = "Valve_Pin"; break;
	case 34: pinStr = "Servo_Pin"; break;
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
	case 50: pinStr = "Nozzle_Cover_1"; break;
	case 48: pinStr = "Nozzle_Cover_2"; break;
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
	case 34: pinStr = "Servo_Pin"; break;
	default: break;
	}
	printf("[DEBUG] Pin %d (%s) set to value %d (%s)\n", pin, pinStr, Value, modeStr);
}
static inline void softPwmCreate(int pin, int startValue, int endValue) {
	char* pinStr = " ";
	switch (pin) {
	case 34: pinStr = "Servo_Pin"; break;
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
#include <wiringPi.h>	//Include wiringPi library for GPIO control
#include <sys/time.h>
#endif

#ifndef DEBUG
#ifdef SERVO_WO_PWM
#include <softPwm.h>	//Include softPwm library for PWM control without PWM-Board
#else
#include <pigpio.h>		//Include pigpio library for PWM control with PWM-Board
#endif
#endif

#define LEDs_Pin 54	//pin
#define Valve_Pin 29	//pin
#define ValveSwitch 01	//pin
#define Servo_Pin 34	//pin
#define Nozzle_Cover_1 50	//Nozzle Cover fully closed Feedback
#define Nozzle_Cover_2 48	//Nozzle Cover fully opened Feedback

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

struct parameter {
	int Mode, ValveDelay, ServoDelay, ManualServoDelay, EoEDelay, PoweroffDelay, FDA20, BDA2, NozzleOnCDelay, NoseConeSeparation, AfterLO, ServoAngle, ServoAngleReset;
};
struct parameter flightstandard = { .Mode = 1, .NoseConeSeparation = 10000, .AfterLO = 55000, .ValveDelay = 5000, .ServoDelay = 6000, .ManualServoDelay = 20000, .EoEDelay = 30000, .PoweroffDelay = 1000, .NozzleOnCDelay = 1000, .ServoAngle = 90 };
struct parameter dryrunstandard = { .Mode = 2, .ValveDelay = 5000, .ServoDelay = 6000, .EoEDelay = 30000, .PoweroffDelay = 1000, .NozzleOnCDelay = 3000, .ServoAngle = 30, .ServoAngleReset = 0 };
struct parameter testrun = { .Mode = 2, .ServoAngle = 30, .ServoAngleReset = 0 };
struct parameter DEBUGstandard = { .Mode = 3, .AfterLO = 5000, .EoEDelay = 3000 };
#ifdef DEBUG 
struct parameter datalogging = { .FDA20 = 50, .BDA2 = 500 }; //FDA here is frames = frequency x duration. With FullData 20Hz & BasicData 2Hz
#else 
struct parameter datalogging = { .FDA20 = 50000, .BDA2 = 500000 }; 
#endif


int Abort = 0;

#ifdef DEBUG
int delay(int millisecond) {	//1000x Second
	clock_t start_time = clock();
	clock_t wait_time = (millisecond * CLOCKS_PER_SEC) / 1000;
	while (clock() < start_time + wait_time) if (Abort) return 1;
	return 0;
}
#endif

#ifdef SERVO_WO_PWM		//Assume the servo 90° rotation is 1ms=0° to 2ms=90°
void ServoRotation(int degree) {
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	int pwmWidth = 10 + (degree * 10) / 90;	//pwm Width value from 10 = 0° to 20 = 90° in x10 of millisecond
	softPwmCreate(Servo_Pin, 0, 100); //100%
	softPwmWrite(Servo_Pin, pwmWidth);
}
#else
void ServoRotation(int degree) {
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	int pwmWidth = 1000 + (degree * 1000) / 90;	//pwm Width value from 1000 = 0° to 2000 = 90° in microsecond
	gpioServo(Servo_Pin, pwmWidth);
}
#endif



//########################################################################################################################################################//
//################################################################## EXPERIMENT PROGRAM ##################################################################//
//########################################################################################################################################################//
#ifdef DEBUG
int NozzlePos = 0;
#endif
int ValveOpen = 1, ValveClose = 0, ValveStuck = 3, valveStatus = 0, ValvePos = 0, ValveCompleted = 0, ServoRun = 1, ServoStop = 0, ServoStuck = 3, servoStatus = 0, nozzleStatus = 0, NozzleStuck = 3, NozzleOpen = 1, NozzleOpened = 0, EoE = 0, SoE = 0, LO = 0, ExperimentStatus;

int ValveRun(struct parameter parameter) {
#ifndef DEBUG
	DataFrame FrameTC = UpdateTC();
#endif
	digitalWrite(LEDs_Pin, 1);			//LED on
	digitalWrite(Valve_Pin, ValveOpen);	//command open valve
#ifdef DEBUG
	printf("Command opening Valve\n");
	ValvePos = digitalRead(ValveSwitch);		//Feedback signal
	ValvePos = ValveOpen; //For debug testing
	printf("*Input Valve 1 for open, 0 for close (std: open): "); scanf_s("%d", &ValvePos); //scanf_s is just for safety and used only in debug mode in visual studio
#else
	ValvePos = ValveOpen;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveOpen) {
		//Valve is open			
#ifdef DEBUG
		printf("Valve Status: Valve is opened\n");
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
		if (parameter.Mode == 2) {
#ifdef DEBUG
			printf("Valve Error Code 1, Return ...\n");
			return -1;
#else
			FrameTC = UpdateTC();
			if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
#endif
		}
	}
	digitalWrite(Valve_Pin, ValveClose);	//command close valve
#ifdef DEBUG
	printf("Command closing Valve\n");
	printf("*Input Valve 1 for open, 0 for close (std: close): "); scanf_s("%d", &ValvePos);
#else
	ValvePos = ValveClose;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveClose) {
		//Valve is close
#ifdef DEBUG
		printf("Valve Status: Valve is closed\n");
#else
		valveStatus = ValveClose;
#endif
		delay(parameter.ServoDelay);
	}
	else if (ValvePos == ValveOpen) {
		//Valve error: in open position / cont. error
#ifdef DEBUG
		printf("Valve Status: Valve is stuck in open position\n");
#else
		valveStatus = ValveStuck;
#endif
		if (parameter.Mode == 2) {
#ifdef DEBUG
			printf("Valve Error Code 2, Return ...\n");
			return -1;
#else
			FrameTC = UpdateTC();
			if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
#endif
		}
	}
	return 0;
}


int ExperimentRun(struct parameter parameter) {
#ifndef DEBUG
	DataFrame FrameTC = UpdateTC();
#endif
	if (parameter.Mode == 1) {
		ServoRotation(parameter.ServoAngle); //command rotate the serve 90° first attempt*
#ifdef DEBUG
		printf("Command to run Servo\n");
		printf("Servo run for 90 Degree\n");
#endif
		delay(parameter.NozzleOnCDelay);
#ifdef DEBUG
		printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
		if (NozzlePos == 1) {
#else
		if (digitalRead(Nozzle_Cover_2)) {
#endif
			//Feedback signal
#ifdef DEBUG
			printf("Nozzle Cover is opened\n");
#else
			nozzleStatus = NozzleOpen;
#endif
#ifdef DEBUG
			delay(DEBUGstandard.EoEDelay);
#else
			delay(parameter.EoEDelay);
#endif
			EoE = 1; //Successful End of Experiment
		}
#ifdef DEBUG
		else if (NozzlePos == 0) {
#else
		else if (digitalRead(Nozzle_Cover_1)) {
#endif
			//Nozzle Cover Problem: in close position
			ServoRotation(parameter.ServoAngle); //command rotate the serve 90° second attempt*
#ifdef DEBUG
			printf("Second attempt\n");
			printf("Servo run for 90 Degree\n");
			printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
#endif
			delay(parameter.NozzleOnCDelay);
#ifdef DEBUG
			if (NozzlePos == 1) {
#else
			if (digitalRead(Nozzle_Cover_2)) {
#endif
#ifdef DEBUG
				printf("Nozzle Cover is opened\n");
#else
				nozzleStatus = NozzleOpen;
#endif
#ifdef DEBUG
				delay(DEBUGstandard.EoEDelay);
#else
				delay(parameter.EoEDelay);
#endif
				EoE = 1; //Successful End of Experiment
			}
			else {
				//Manual override to open the nozzle cover
				for (int attempt = 0; attempt < 3; attempt++) {
#ifdef DEBUG
					printf("Manual Servo Run: "); scanf_s("%d", &NozzlePos);
					if (NozzlePos == 1) break;
#else
					ServoRotation(ReadFrame(FrameTC, Servo_Control));
					if (digitalRead(Nozzle_Cover_2)) break;
#endif
				}
#ifdef DEBUG
				if (NozzlePos == 1) {
#else
				if (digitalRead(Nozzle_Cover_2)) {
					nozzleStatus = NozzleOpen;
#endif
					delay(parameter.EoEDelay);
					EoE = 1; //Successful End of Experiment
				}
#ifdef DEBUG
				else if (NozzlePos == 0) printf("Nozzle Cover is stuck in close position\n");
#else
				else if (digitalRead(Nozzle_Cover_1)) nozzleStatus = NozzleStuck;
#endif
			}
		}
	}
	else if (parameter.Mode == 2) {
#ifdef DEBUG
		printf("Simulating nozzle cover open 30° (Success = 1; Fail = 0): "); scanf_s("%d", &NozzlePos);
		if (NozzlePos == 0) {
			return -1; //abort test
		}
#else
		ServoRotation(parameter.ServoAngle); //command rotate the serve 30° for testing
		if (parameter.ServoAngle <= 10) {
			FrameTC = UpdateTC();
			return -1; //abort test
		}
		else if (parameter.ServoAngle == 30) {
			delay(parameter.NozzleOnCDelay);
			ServoRotation(parameter.ServoAngleReset);
		}
		FrameTC = UpdateTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
		//nozzleStatus = NozzleOpen;				//simulate nozzle cover open
#endif
#ifdef DEBUG
		delay(DEBUGstandard.EoEDelay);
#else
		FrameTC = UpdateTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
		delay(parameter.EoEDelay);
#endif
		digitalWrite(LEDs_Pin, 0);
		nozzleStatus = 0;						//Reset simulation of nozzle cover open
		delay(parameter.PoweroffDelay);
	}

	if (EoE == 1) {
#ifdef DEBUG
		printf("Experiment: Successful\n");
#endif
		digitalWrite(LEDs_Pin, 0);			//LED off
		delay(parameter.PoweroffDelay);
#ifdef DEBUG
		printf("End of Experiment: Successful\n");
#endif
		return 43;	//End of Experiment
	}
	else if (parameter.Mode == 2) {
#ifdef DEBUG
		printf("End of Experiment: Test Mode\n");
		ExperimentStatus = 3;
#else
		ExperimentStatus = End_Experiment;
#endif
	}
	else if (parameter.Mode == 2 && -1) {
#ifdef DEBUG
		printf("End of Experiment: Test Mode Error\n");
#else
		digitalWrite(LEDs_Pin, 0);			//LED off
#endif
	}
	else {
#ifdef DEBUG
		printf("End of Experiment: Error\n");
#endif
		digitalWrite(LEDs_Pin, 0);			//LED off
		delay(parameter.PoweroffDelay);
		return 404;	//Error in Experiment
	}
	return 0;
}

#ifndef DEBUG
//BETA Control Panel Functions not yet implemented from DataHandling
int ExperimentControl() {
	ExperimentStatus = Start_Experiment;
	while (1) {
		DataFrame FrameTC = UpdateTC();
		//Valve Control
		if (!FrameIsEmpty(FrameTC)) {

			//Valve Control
			if (ReadFrame(FrameTC, Valve_Control) == 1) digitalWrite(Valve_Pin, ValveOpen);	//command open valve
			else if (ReadFrame(FrameTC, Valve_Control) == 0) digitalWrite(Valve_Pin, ValveClose);	//command close valve

			//LEDs Control
			if (ReadFrame(FrameTC, LED_Control) == 1) digitalWrite(LEDs_Pin, ValveOpen);	//command open valve
			else if (ReadFrame(FrameTC, LED_Control) == 0) digitalWrite(LEDs_Pin, ValveClose);	//command close valve

			//Servo Control
			if (ReadFrame(FrameTC, Servo_Control) >= 0 && ReadFrame(FrameTC, Servo_Control) <= 90) ServoRotation(ReadFrame(FrameTC, Servo_Control));	//command rotate the servo to the specified degree
		}
		delay(500);
	}
	ExperimentStatus = End_Experiment;
	return 0;
}
#endif



//###########################################################################################################################################################################//
//################################################################## START OF DATA ACQUISITION AND LOGGING ##################################################################//
//###########################################################################################################################################################################//
int SoEReceived = 0;
void DataAcquisition(DataFrame* frame) {
#ifdef DEBUG
	int SystemTime = clock();	//System Time
	int AmbientPressure = 1013;
	int CompareTemperature = 20;
	int TankPressure = 2;
	int TankTemperature = 70;
	int ChamberPressure = 4;
	int ChamberTemperature = 80;
	int NozzlePressure_1 = 5;
	int NozzlePressure_2 = 6;
	int NozzlePressure_3 = 4;
	int NozzleTemperature_1 = 78;
	int NozzleTemperature_2 = 83;
	int NozzleTemperature_3 = 79;
	int NozzleCover = 1;	//Nozzle Cover Feedback: fully open
	int NozzleServo = 1;	//Nozzle Servo Switch
	int ReservoirValve = 1;	//Reservoir Valve
	int LEDsStat = 1;
	int sensorboard_1 = 0;		//Sensorboard is not implemented yet ?
	int sensorboard_2 = 0;
	int mainboard = 0;			//Mainboard is not implemented yet ?
	int ExperimentStatus = 1;
#else
	int SystemTime = clock();	//System Time
	int AmbientPressure = analogRead(0);
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
	int NozzleCover = digitalRead(Nozzle_Cover_2);	//Nozzle Cover Feedback: fully open
	int NozzleServo = digitalRead(Servo_Pin);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Valve_Pin);	//Reservoir Valve
	int LEDsStat = digitalRead(LEDs_Pin);
	int sensorboard_1 = 0;		//Sensorboard is not implemented yet ?
	int sensorboard_2 = 0;
	int mainboard = 0;			//Mainboard is not implemented yet ?
	//Experiment Status CHECK!
#endif

	WriteFrame(frame, System_Time, SystemTime);
	WriteFrame(frame, Ambient_Pressure, AmbientPressure);
	WriteFrame(frame, Compare_Temperature, CompareTemperature);
	WriteFrame(frame, Tank_Pressure, TankPressure);
	WriteFrame(frame, Tank_Temperature, TankTemperature);
	WriteFrame(frame, Chamber_Pressure, ChamberPressure);
	WriteFrame(frame, Chamber_Temperature, ChamberTemperature);
	WriteFrame(frame, Nozzle_Pressure_1, NozzlePressure_1);
	WriteFrame(frame, Nozzle_Pressure_2, NozzlePressure_2);
	WriteFrame(frame, Nozzle_Pressure_3, NozzlePressure_3);
	WriteFrame(frame, Nozzle_Temperature_1, NozzleTemperature_1);
	WriteFrame(frame, Nozzle_Temperature_2, NozzleTemperature_2);
	WriteFrame(frame, Nozzle_Temperature_3, NozzleTemperature_3);
	WriteFrame(frame, Nozzle_Cover, NozzleCover);
	WriteFrame(frame, Nozzle_Servo, NozzleServo);
	WriteFrame(frame, Reservoir_Valve, ReservoirValve);
	WriteFrame(frame, LEDs, LEDsStat);
	WriteFrame(frame, Sensorboard_1, sensorboard_1);
	WriteFrame(frame, Sensorboard_2, sensorboard_2);
	WriteFrame(frame, Mainboard, mainboard);
	WriteFrame(frame, Mode, ExperimentStatus);
	WriteFrame(frame, Lift_Off, ExperimentStatus);
	WriteFrame(frame, Start_Experiment, ExperimentStatus);
	WriteFrame(frame, End_Experiment, ExperimentStatus);
}

void Log() {
	struct parameter freq = datalogging; //Logging frequency parameters
	int sync = 0;				//Sync value for the DataFrame
	int syncLimit = 0;			//Sync limit for the DataFrame, every 10 Frames a new Sync value is set

	while (1) {
#ifdef DEBUG
		clock_t start = clock();
#else
		struct timeval start, end;
		gettimeofday(&start,NULL);
#endif
		DataFrame frame = CreateFrame(sync++);
		DataAcquisition(&frame);	//DataAcquisition function to fill the frame with data
		AddFrame(frame);	//func from UPDATED DataHandlingLib
#ifndef DEBUG
		WritePoint(Ambient_Pressure, 0, 10, 1);
		WritePoint(Ambient_Pressure, 1, 20, 2);
		WritePoint(Ambient_Pressure, 2, 30, 3);
		UpdateAll();
		int p = ReadFrame(frame, Ambient_Pressure);
		float analysis = MapSensorValue(Ambient_Pressure, p);
#endif
		syncLimit++;
		if (syncLimit >= 10) {
			UpdateAll();	//Update the storage hub, this will write the packets to the harddrive if necessary
			syncLimit = 0;								//Reset the sync limit
		}
		if (SoEReceived) {
//---------------------------------------------------------------------------------------FIX--------------------------------------------------------------------------------
#ifdef DEBUG
			printf("Full Data Acquisition\n");
			clock_t end = clock();
			long duration = ((end - start) * 1000) / CLOCKS_PER_SEC;
			long wait = freq.FDA20 - duration;
			if (wait > 0) delay(wait);
#else
			gettimeofday(&end,NULL);
			suseconds_t duration = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
			suseconds_t wait = freq.FDA20 - duration;
			if (wait > 0) usleep(wait); //Full Data Acquisition 20Hz
#endif
		}
		else {
#ifdef DEBUG
			printf("Basic Data Acquisition\n");
			delay(freq.BDA2);		//Basic Data Acquisition 2Hz
#else
			gettimeofday(&end, NULL);
			suseconds_t duration = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
			suseconds_t wait = freq.BDA2 - duration;
			if (wait > 0) usleep(wait); //Basic Data Acquisition 2Hz
#endif
		}
		if (testrun.Mode == 2 || dryrunstandard.Mode == 2) {
#ifdef DEBUG
			if (Abort == 1) SoEReceived = 0;
#else
			if (ReadFrame(UpdateTC(), Test_Abort)) SoEReceived = 0;
#endif
		}
#ifdef DEBUG
		else if (ExperimentStatus == 3) SoEReceived = 0;
#else
		else if (ExperimentStatus == End_Experiment) SoEReceived = 0;
#endif
	}
}
void* LogThread(void* arg) {
	Log();	//Start the logging function
	return NULL;	//Return NULL to end the thread
}



//######################################################################################################################################################//
//################################################################## FAILSAFE PROGRAM ##################################################################//
//######################################################################################################################################################//

typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, VALVE_OPENED, EXPERIMENT_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;
int experimentRunning = 0;

void FailSafeRecovery() {
	SaveFileFrame* lastFrame = GetSaveFrame(-1); //Get the last SaveFileFrame
	if (lastFrame != NULL) {
		currentState = WAIT_LO;
		ValveCompleted = 0;
		NozzleOpened = 0;
		experimentRunning = 0;
	}
	else {
		CreateFailSafe();
		currentState = WAIT_LO;
		ValveCompleted = 0;
		NozzleOpened = 0;
		experimentRunning = 0;
	}
}



//###########################################################################################################################################################//
//################################################################## START OF MAIN PROGRAM ##################################################################//
//###########################################################################################################################################################//
//START OF MAIN PROGRAM
int main() {
#ifdef DEBUG
	pinMode(Valve_Pin, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Servo_Pin, OUTPUT);
	pinMode(LEDs_Pin, OUTPUT);

	pinMode(Nozzle_Cover_1, INPUT);
	pinMode(Nozzle_Cover_2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);

	Initialize(NULL);
#else
	wiringPiSetupGpio();
	pinMode(Valve_Pin, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Servo_Pin, OUTPUT);
	pinMode(LEDs_Pin, OUTPUT);

	pinMode(Nozzle_Cover_1, INPUT);
	pinMode(Nozzle_Cover_2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);

	pullUpDnControl(RPi_LO, PUD_DOWN);
	pullUpDnControl(RPi_SOE, PUD_DOWN);

	Initialize("");
	FailSafeRecovery();
#endif

	//ExperimentStatus: Lift_Off; Start_Experiment; End_Experiment; Mode
#ifdef DEBUG
	int ExperimentStatus = 0;
#endif
	struct parameter config;

	pthread_t logThread;
	//create a thread that runs LogThread function: success->parallel programm; failure->no threads logging and return to NULL
	//using if to let know if there is/are problem(s)
	if (pthread_create(&logThread, NULL, LogThread, (void*)&config)) {	//Create a thread for logging
		//LED blink for 5 times: logging thread failed to start
		for(int i=0;i<5;i++) {
			digitalWrite(LEDs_Pin, 1);
			delay(500);
			digitalWrite(LEDs_Pin, 0);
			delay(500);
		}
		return 1;
	}

	int EoECompleted = 0;

	while (!EoECompleted) {	
		//int flightmode = 1;
		//int testmode = 0;
		int LOSignal = digitalRead(RPi_LO);

#ifdef DEBUG
		int modeSel;
		printf("*Mode selection 1 for Flight, 0 for Test: "); scanf_s("%d", &modeSel);
#else
		DataFrame modeFrame = UpdateTC(); //Update the Tele Command frame from the Telemetry buffer
		int modeSel = ReadFrame(modeFrame, Mode_Change);	//Read the mode change from the Tele Command
#endif
		// Test Mode = 0, Flight Mode = 1

		if (modeSel == 1) {		//Flight Mode
#ifndef DEBUG
			ExperimentStatus = Mode;
#endif
			config = flightstandard;
#ifdef DEBUG
			printf("*LO Signal? 1 for YES, 0 for NO: "); scanf_s("%d", &LOSignal);
#endif
			if (LOSignal == 0) continue;

			currentState = WAIT_LO;
			ValveCompleted = 0;
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
					ExperimentStatus = Lift_Off; //LO Signal received
					delay(config.AfterLO);	//Wait for 55s after liftoff
#endif
					currentState = NOSECONE_SEPARATION;
					break;

				case NOSECONE_SEPARATION:
					digitalWrite(LEDs_Pin, 1);	//LED on
#ifdef DEBUG
					printf("Nose Cone Separation\n");
#endif
					delay(config.NoseConeSeparation);			//Wait for Nozzle Cone Separation
					digitalWrite(LEDs_Pin, 0);	//LED off
					currentState = WAIT_SOE;
					break;

				case WAIT_SOE:
					while (!SoESignal()) delay(100);
					SoEReceived = 1;
#ifndef DEBUG
					ExperimentStatus = Start_Experiment; //Experiment started
#endif
					currentState = VALVE_OPENED;
					break;

				case VALVE_OPENED:
					if (!ValveCompleted) {
						int ValveRunStatus = ValveRun(config);
						ValveCompleted = 1;
					}
					currentState = EXPERIMENT_RUNNING;
					break;

				case EXPERIMENT_RUNNING:
					if (!NozzleOpened) {
						int ExperimentRunStatus = ExperimentRun(config);
						experimentRunning = 1;

						if (ExperimentRunStatus == 43 || ExperimentRunStatus == 404) {
							currentState = NOZZLE_OPENED;
						}
					}
					break;

				case NOZZLE_OPENED:
					NozzleOpened = 1;
					currentState = END_OF_EXPERIMENT; //End of Experiment
					break;
				case END_OF_EXPERIMENT:
#ifdef DEBUG
					ExperimentStatus = 3;
#else
					ExperimentStatus = End_Experiment; //Experiment ended
#endif
					break;
				}
			}
			EoECompleted = 1;
			CloseAll();	//Close all files and threads
			break;
		}
		else if (modeSel == 0) {	//Test Mode
#ifndef DEBUG
			ExperimentStatus = Mode;
#endif
			while (!SoESignal()) delay(100);
			SoEReceived = 1;
#ifdef DEBUG
			config = dryrunstandard;
			int valveTest = ValveRun(config);
			if (valveTest != -1) {
				int experimentTest = ExperimentRun(config);
				if (experimentTest == -1) continue;
			}
			else if (valveTest == -1) {
				continue; //abort test
			}
#else
			DataFrame FrameTC = UpdateTC();
			int dryRun = ReadFrame(FrameTC, Dry_Run);
			int testRun = ReadFrame(FrameTC, Test_Run);

			if (dryRun == 1) {
				ExperimentStatus = Start_Experiment;
				config = dryrunstandard;
				int valveTest = ValveRun(config);
				if (valveTest != -1) {
					int experimentTest = ExperimentRun(config);
					if (experimentTest == -1) {
						ExperimentStatus = End_Experiment;
						continue; //abort test
					}
				}
				else if (valveTest == -1) {
					ExperimentStatus = End_Experiment;
					continue; //abort test
				}
			}
			else if (testRun == 1) {
				ExperimentStatus = Start_Experiment;
				config = testrun;
				config.ValveDelay = ReadFrame(FrameTC, Valve_Delay);		//Changeable Valve Delay from Ground Station
				config.ServoDelay = ReadFrame(FrameTC, Servo_Delay);		//Changeable Servo Delay from Ground Station
				config.EoEDelay = ReadFrame(FrameTC, EoE_Delay);			//Changebale End of Experiment Delay from Ground Station
				config.PoweroffDelay = ReadFrame(FrameTC, Power_Off_Delay);	//Changeable Power off Delay

				int valveTest = ValveRun(config);
				if (valveTest != -1) {
					int experimentTest = ExperimentRun(config);
					if (experimentTest == -1) {
						ExperimentStatus = End_Experiment;
						continue; //abort test
					}
				}
				else if (valveTest == -1) {
					ExperimentStatus = End_Experiment;
					continue; //abort test
				}
			}
			else {
				ExperimentControl();
			}
#endif
			ExperimentStatus = 0; //Reset Experiment Status

			continue;
		}
	}
	return 0;
}