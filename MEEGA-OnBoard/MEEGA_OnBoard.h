//Header File for MEEGA OnBoard 
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include "DataHandlingLibrary.h"
#include <stdlib.h>
#include <stdint.h>


#define WINDOWS 0
#define LINUX 1

#define DEBUG 0
#define RELEASE 1

#define TEST 0
#define RUN 1

#define SERVO_v1 0
#define SERVO_v2 1

#define WIRINGPISPI 0
#define SPIDEV 1

//OnBoard Settings
#define ONBOARD_OS WINDOWS
#define MODE DEBUG
#define EXPERIMENT TEST
#define SERVO_VERSION SERVO_v1
#define SENSORS_SPI_VERSION WIRINGPISPI


//PinOut for CM5
#define LEDs_Pin 4	//pin
#define Valve_Pin 16	//pin
#define ValveSwitch 01	//pin
#define Servo_Pin 12	//pin
#define Servo_On 5	//pin
#define Nozzle_Cover_S1 17	//Nozzle Cover fully closed Feedback
#define Nozzle_Cover_S2 27	//Nozzle Cover fully opened Feedback

#define RPi_SOE 25	//pin
#define RPi_LO 23	//pin


#if (ONBOARD_OS == WINDOWS)

#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define INPUT 0

//DEBUG for GPIO control from RaspberryPi
static inline void pinMode(int pin, int mode) {
	char* pinStr = " ", * modeStr = " ";
	switch (pin) {
	case 54: pinStr = "LEDs_Pin"; break;
	case 29: pinStr = "Valve_Pin"; break;
	case 01: pinStr = "ValveSwitch"; break;
	case 34: pinStr = "Servo_Pin"; break;
	case 50: pinStr = "Nozzle_Cover_S1"; break;
	case 48: pinStr = "Nozzle_Cover_S2"; break;
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
	case 50: pinStr = "Nozzle_Cover_S1"; break;
	case 48: pinStr = "Nozzle_Cover_S2"; break;
	case 41: pinStr = "RPi_SOE"; break;
	case 47: pinStr = "RPi_LO";break;
	default: break;
	}
	printf("[DEBUG] Reading value from pin %d (%s)\n", pin, pinStr);
	return LOW;	//return LOW for debug testing
}

static inline void softPwmWrite(int pin, int Value) {
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
//Delay function for milliseconds
int Abort = 0;
int delay(int millisecond) {	//1000x Second
	clock_t start_time = clock();
	clock_t wait_time = (millisecond * CLOCKS_PER_SEC) / 1000;
	while (clock() < start_time + wait_time) if (Abort) return 1;
	return 0;
}

#elif (ONBOARD_OS == LINUX)

#include <wiringPi.h>	//Include wiringPi library for GPIO control
#include <sys/time.h>
#include <softPwm.h>	//Include softPwm library for PWM control without PWM-Board

#if (SENSORS_SPI_VERSION == WIRINGPISPI)

#include <wiringPiSPI.h>	//Include wiringPiSPI library for SPI control

#define SPI_PRESSURE 1	//SPI Channel 0
#define PRESSURE_SENSORS 6

#define SPI_TEMPERATURE 0	//SPI Channel 1
#define TEMPERATURE_SENSORS 6

float pressureRead[PRESSURE_SENSORS];
float temperatureRead[TEMPERATURE_SENSORS];

#elif (SENSORS_SPI_VERSION == SPIDEV)

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

#define SPI_PRESSURE "/dev/spidev0.1"
#define SPI_TEMPERATURE "/dev/spidev0.0"
#endif

#endif

//Global Variables Declaration
#if (MODE == DEBUG)
int NozzlePos = 0,
	SoE = 0;
#endif
int ValveOpen = 1,
	ValveClose = 0,
	ValveStuck = 3,
	valveStatus = 0,
	ValvePos = 0,
	ValveCompleted = 0,
	ServoStuck = 3,
	servoStatus = 0,
	nozzleStatus = 0,
	NozzleStuck = 3,
	NozzleOpen = 1,
	NozzleOpened = 0,
	
	ExperimentStatus,
	TestStatus = 0,
	LOSignal,
	SoEReceived = 0,
	EoE = 0,
	modeSel;

//Parameters Declaration
struct parameter {
	int Mode, ValveDelay, ServoDelay, EoEDelay, PoweroffDelay, FDA20, BDA2, NozzleOnCDelay, NoseConeSeparation, AfterLO, ServoAngle, ServoAngleReset, ServoRetryDelay;
};
#define DEFAULT_PARAMETER \
	.ValveDelay = 5000, \
	.ServoDelay = 6000, \
	.EoEDelay = 30000, \
	.PoweroffDelay = 1000, \
	.NozzleOnCDelay = 1500, \
	.ServoAngleReset = 0, \
	.ServoRetryDelay = 3000
//Default Parameters
struct parameter flightstandard = { .Mode = 1, DEFAULT_PARAMETER, .NoseConeSeparation = 10000, .AfterLO = 55000, .ServoAngle = 90 };
struct parameter dryrunstandard = { .Mode = 2, DEFAULT_PARAMETER, .ServoAngle = 30 };
struct parameter testrun = { .Mode = 2, .ServoAngle = 30 };
struct parameter DEBUGstandard = { .Mode = 3, .AfterLO = 5000, .EoEDelay = 3000 };

//FailSafe Experiment Status
typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, VALVE_OPENED, EXPERIMENT_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;
int experimentRunning = 0;


//EXPERIMENT
//Function receiving the SOE signal from the RPi
int SoESignal();
//Function to SetUp the Servo
void ServoRotation(int degree);
//Function in Experiment controlling the Valve operation
int ValveRun(struct parameter parameter);
//Function in Experiment controlling the Servo operation
int ServoRun(struct parameter parameter);
//Functiong in Test Mode manually controlling the Experiment from the Ground Station
int ExperimentControl();

//DATA LOGGING
//Function acquiring the Data from the Sensors and writing it into a DataFrame
void DataAcquisition(DataFrame* frame);
//Function running the Data Logging in a thread
void Log();
//Thread function for Data Logging
void* LogThread(void* arg);
//FailSafe Function to recover the last experiment state
void FailSafeRecovery();

//Read Pressure sensors from SPI
void ReadPressureSensors(float* Sensors);
//Read Temperature sensors from SPI
void ReadTemperatureSensors(float* Sensors);
