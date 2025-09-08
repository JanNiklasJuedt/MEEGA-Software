#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <pthread.h>

#define DEBUG
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
#endif

#ifndef DEBUG
#ifdef SERVO_WO_PWM
#include <softPwm.h>	//Include softPwm library for PWM control without PWM-Board
#else
#include <pigpio.h>		//Include pigpio library for PWM control with PWM-Board
#endif
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

struct parameter {
	int Mode, ValveDelay, ServoDelay, ManualServoDelay, EoEDelay, PoweroffDelay, FDA20, FDA2, NozzleOnCDelay, NoseConeSeparation, AfterLO, ServoAngle, ServoAngleReset;
};
struct parameter flightstandard = { .Mode = 1, .NoseConeSeparation = 10000, .AfterLO = 55000, .ValveDelay = 5000, .ServoDelay = 6000, .ManualServoDelay = 20000, .EoEDelay = 30000, .PoweroffDelay = 1000, .NozzleOnCDelay = 1000, .ServoAngle = 90 };
struct parameter dryrunstandard = { .Mode = 2, .ValveDelay = 5000, .ServoDelay = 6000, .EoEDelay = 30000, .PoweroffDelay = 1000, .NozzleOnCDelay = 3000, .ServoAngle = 30, .ServoAngleReset = 0 };
struct parameter testrun = { .Mode = 2, .ServoAngle = 30, .ServoAngleReset = 0 };
struct parameter DEBUGstandard = { .Mode = 3, .AfterLO = 5000, .EoEDelay = 3000 };
struct parameter datalogging = { .FDA20 = 500, .FDA2 = 5000 }; //FDA here is frames = frequency x duration. With FullData 20Hz & BasicData 2Hz

#ifdef DEBUG
int Test_Abort = 0;
#endif
int delay(int millisecond) {	//1000x Second
	clock_t start_time = clock();
	clock_t wait_time = (millisecond * CLOCKS_PER_SEC) / 1000;
#ifdef DEBUG
	while (clock() < start_time + wait_time) if (Test_Abort) return 1;
#else
	while (clock() < start_time + wait_time) if(Test_Abort) return 1;
#endif
	return 0;
}

#ifdef SERVO_WO_PWM		//Assume the servo 90° rotation is 1ms=0° to 2ms=90°
void ServoRotation(int degree) {
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	int pwmWidth = 10 + (degree * 10) / 90;	//pwm Width value from 10 = 0° to 20 = 90° in x10 of millisecond
	softPwmCreate(Nozzle_Servo, 0, 100); //100%
	softPwmWrite(Nozzle_Servo, pwmWidth);
}
#else
void ServoRotation(int degree) {
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	int pwmWidth = 1000 + (degree * 1000) / 90;	//pwm Width value from 1000 = 0° to 2000 = 90° in microsecond
	gpioServo(Nozzle_Servo, pwmWidth);
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
	digitalWrite(LEDs, 1);			//LED on
	digitalWrite(Reservoir_Valve, ValveOpen);	//command open valve
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
			if (ReadFrame(FrameTC, Test_Abort) == 1) {
				ExperimentStatus = 3;
				return -1; //abort test
			}
#endif
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
		printf("Valve Status: Valve is closed\n");
#else
		valveStatus = ValveClose;
		ValveCompleted = 1; //Valve operation completed
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
		if (parameter.Mode == 2) {
#ifdef DEBUG
			printf("Valve Error Code 2, Return ...\n");
			return -1;
#else
			FrameTC = UpdateTC();
			if (ReadFrame(FrameTC, Test_Abort) == 1) {
				ExperimentStatus = 3;
				return -1; //abort test
			}
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
		if (digitalRead(ServoSwitch_2)) {
#endif
			//Feedback signal
			//Nozzle Cover Problem: in close position
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
		else if (digitalRead(ServoSwitch_1)) {
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
			if (digitalRead(ServoSwitch_2)) {
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
					if (digitalRead(ServoSwitch_2)) break;
#endif
				}
#ifdef DEBUG
				if (NozzlePos == 1) {
#else
				if (digitalRead(ServoSwitch_2)) {
					nozzleStatus = NozzleOpen;
#endif
					delay(parameter.EoEDelay);
					EoE = 1; //Successful End of Experiment
				}
#ifdef DEBUG
				else if (NozzlePos == 0) printf("Nozzle Cover is stuck in close position\n");
#else
				else if (digitalRead(ServoSwitch_1)) nozzleStatus = NozzleStuck;
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
			ExperimentStatus = 3;
			return -1; //abort test
		}
		else if (parameter.ServoAngle == 30) {
			delay(parameter.NozzleOnCDelay);
			ServoRotation(parameter.ServoAngleReset);
		}
		FrameTC = UpdateTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) {
			ExperimentStatus = 3;
			return -1; //abort test
		}
		//nozzleStatus = NozzleOpen;				//simulate nozzle cover open
#endif
#ifdef DEBUG
		delay(DEBUGstandard.EoEDelay);
#else
		FrameTC = UpdateTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) {
			ExperimentStatus = 3;
			return -1; //abort test
		}
		delay(parameter.EoEDelay);
#endif
		digitalWrite(LEDs, 0);
		nozzleStatus = 0;						//Reset simulation of nozzle cover open
		delay(parameter.PoweroffDelay);
	}
	if (EoE == 1) {
#ifdef DEBUG
		printf("Experiment: Successful\n");
#else
		ExperimentStatus = 3;
#endif
		digitalWrite(LEDs, 0);			//LED off
		delay(parameter.PoweroffDelay);
#ifdef DEBUG
		printf("End of Experiment: Successful\n");
#endif
		return 43;	//End of Experiment
	}
	else if (parameter.Mode == 2) {
#ifdef DEBUG
		printf("End of Experiment: Test Mode\n");
#else
		ExperimentStatus = 3;
#endif
	}
	else if (-1){
#ifdef DEBUG
		printf("End of Experiment: Error\n");
#endif
		digitalWrite(LEDs, 0);			//LED off
		delay(parameter.PoweroffDelay);
		return 404;	//Error in Experiment
	}
	return 0;
}

#ifndef DEBUG
//BETA Control Panel Functions not yet implemented from DataHandling
int ExperimentControl() {
	ExperimentStatus = 4;
	while (1) {
		DataFrame FrameTC = UpdateTC();
		//Valve Control
		if (!FrameIsEmpty(FrameTC)) {

			//Valve Control
			if (ReadFrame(FrameTC, Valve_Control) == 1) digitalWrite(Reservoir_Valve, ValveOpen);	//command open valve
			else if (ReadFrame(FrameTC, Valve_Control) == 0) digitalWrite(Reservoir_Valve, ValveClose);	//command close valve

			//LEDs Control
			if (ReadFrame(FrameTC, LED_Control) == 1) digitalWrite(LEDs, ValveOpen);	//command open valve
			else if (ReadFrame(FrameTC, LED_Control) == 0) digitalWrite(LEDs, ValveClose);	//command close valve

			//Servo Control
			if (ReadFrame(FrameTC, Servo_Control) >= 0 && ReadFrame(FrameTC, Servo_Control) <= 90) ServoRotation(ReadFrame(FrameTC, Servo_Control));	//command rotate the servo to the specified degree
		}
		delay(500);
	}
	return 0;
}
#endif



//###########################################################################################################################################################################//
//################################################################## START OF DATA ACQUISITION AND LOGGING ##################################################################//
//###########################################################################################################################################################################//
#ifndef DEBUG
void DataAcquisition(DataFrame* frame) {
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
	int NozzleCover = digitalRead(ServoSwitch_2);	//Nozzle Cover Feedback: fully open
	int NozzleServo = digitalRead(Nozzle_Servo);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Reservoir_Valve);	//Reservoir Valve
	int LEDsStat = digitalRead(LEDs);
	int Sensorboard_1 = 0;		//Sensorboard is not implemented yet ?
	int Sensorboard_2 = 0;
	int Mainboard = 0;			//Mainboard is not implemented yet ?
	//Experiment Status CHECK!

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
	WriteFrame(frame, Sensorboard_1, Sensorboard_1);
	WriteFrame(frame, Sensorboard_2, Sensorboard_2);
	WriteFrame(frame, Mainboard, Mainboard);
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
		clock_t start = clock();
		DataFrame frame = CreateFrame(sync++);
		DataAcquisition(&frame);	//DataAcquisition function to fill the frame with data
		AddOutFrame(frame);	//Add the frame to the save file
		syncLimit++;
		if (syncLimit >= 10) {
			Update();	//Update the storage hub, this will write the packets to the harddrive if necessary
			syncLimit = 0;								//Reset the sync limit
		}
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
	Log();	//Start the logging function
	return NULL;	//Return NULL to end the thread
}
#endif



//######################################################################################################################################################//
//################################################################## FAILSAFE PROGRAM ##################################################################//
//######################################################################################################################################################//

typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, VALVE_OPENED, EXPERIMENT_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;
int experimentRunning = 0;

#ifndef DEBUG
void FailSafeRecovery() {
	if (ReadFailSafe() == 0) {
		if (HasFlag(UpdateTC(),Experiment) == 0) {
			currentState = WAIT_LO;
			ValveCompleted = 0;
			NozzleOpened = 0;
			experimentRunning = 0;
		}
	}
	else {
		CreateFailSafe();
		currentState = WAIT_LO;
		ValveCompleted = 0;
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

	pullUpDnControl(RPi_LO, PUD_DOWN);
	pullUpDnControl(RPi_SOE, PUD_DOWN);

	Initialize(NULL);
	FailSafeRecovery();
#endif

	//LO: 1; SoE: 2; EoE: 3; Experiment Contol Panel/Mode: 4 
	ExperimentStatus = 0;
	struct parameter config;

#ifndef DEBUG
	pthread_t logThread;
	//create a thread that runs LogThread function: success->parallel programm; failure->no threads logging and return to NULL
	//using if to let know if there is/are problem(s)
	if (pthread_create(&logThread, NULL, LogThread, (void*)&config)) {	//Create a thread for logging
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
		int modeSel;
		printf("*Mode selection 1 for Flight, 0 for Test: "); scanf_s("%d", &modeSel);
#else
		DataFrame modeFrame = UpdateTC(); //Update the Tele Command frame from the Telemetry buffer
		int modeSel = ReadFrame(modeFrame, Mode_Change);	//Read the mode change from the Tele Command
#endif
		// Test Mode = 0, Flight Mode = 1

		if (modeSel == 1) {		//Flight Mode
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
						UpdateFailSafe(); //Update the failsafe file to indicate that the LO signal has been received
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
					UpdateFailSafe(); //Update the failsafe file to indicate that the After LO delay has been completed
					break;

				case NOSECONE_SEPARATION:
					digitalWrite(LEDs, 1);	//LED on
#ifdef DEBUG
					printf("Nose Cone Separation\n");
#endif
					delay(config.NoseConeSeparation);			//Wait for Nozzle Cone Separation
					digitalWrite(LEDs, 0);	//LED off
					currentState = WAIT_SOE;
					UpdateFailSafe(); //Update the failsafe file to indicate that the Nose Cone Separation has been completed
					break;

				case WAIT_SOE:
					while (!SoESignal()) delay(100);
					ExperimentStatus = 2; //Experiment started
					currentState = VALVE_OPENED;
					UpdateFailSafe(); //Update the failsafe file to indicate that the SoE signal has been received
					break;

				case VALVE_OPENED:
					if (!ValveCompleted) {
						int ValveRunStatus = ValveRun(config);
						ValveCompleted = 1;
						UpdateFailSafe(); //Update the failsafe file to indicate that the Valve operation has been completed
					}
					currentState = EXPERIMENT_RUNNING;
					break;

				case EXPERIMENT_RUNNING:
					if (!NozzleOpened) {
						int ExperimentRunStatus = ExperimentRun(config);
						experimentRunning = 1;

						if (ExperimentRunStatus == 43 || ExperimentRunStatus == 404) {
							NozzleOpened = 1;
							currentState = END_OF_EXPERIMENT; //End of Experiment
							UpdateFailSafe(); //Update the failsafe file to indicate that the Experiment has been completed
						}
					}
					break;

				case NOZZLE_OPENED:
				case END_OF_EXPERIMENT:
					break;
				}
			}
			EoECompleted = 1;
			UpdateFailSafe();
#ifndef DEBUG
			CloseAll();	//Close all files and threads
#endif
		}
		else if (modeSel == 0) {	//Test Mode
			ExperimentStatus = 4;
			while (!SoESignal()) delay(100);
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
				config = dryrunstandard;
				int valveTest = ValveRun(config);
				if (valveTest != -1) {
					int experimentTest = ExperimentRun(config);
					if (experimentTest == -1) {
						UpdateFailSafe();
						continue; //abort test
					}
				}
				else if (valveTest == -1) {
					UpdateFailSafe();
					continue; //abort test
				}
			}
			else if (testRun == 1) {
				config = testrun;
				config.ValveDelay = ReadFrame(FrameTC, Valve_Delay);		//Changeable Valve Delay from Ground Station
				config.ServoDelay = ReadFrame(FrameTC, Servo_Delay);		//Changeable Servo Delay from Ground Station
				config.EoEDelay = ReadFrame(FrameTC, EoE_Delay);			//Changebale End of Experiment Delay from Ground Station
				config.PoweroffDelay = ReadFrame(FrameTC, Power_Off_Delay);	//Changeable Power off Delay

				int valveTest = ValveRun(config);
				if (valveTest != -1) {
					int experimentTest = ExperimentRun(config);
					if (experimentTest == -1) {
						UpdateFailSafe();
						continue; //abort test
					}
				}
				else if (valveTest == -1) {
					UpdateFailSafe();
					continue; //abort test
				}
			}
			else ExperimentControl();
#endif
			ExperimentStatus = 0;

			continue;
		}
	}
	return 0;
}
