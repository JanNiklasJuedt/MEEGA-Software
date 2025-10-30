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
#define CS_PSB 7
#define CS_TSB 8

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

//SETUP for Sensors Reading
#define SPI_SPEED 1000000	//1MHz - MPR_P_SPI max 800kHz; AD7793_ADC max 4MHz; LTC2450_ADC max 2MHz  - Test with 500kHz, 1MHz
#define CMD_READ 0xA1 //Command to read data from the sensors

#define P_TxPACKET_LENGTH 17 //bytes
#define SPI_PRESSURE 1	//SPI Channel 1
#define PRESSURE_SENSORS 6

#define T_TxPACKET_LENGTH 19 //bytes
#define SPI_TEMPERATURE 0	//SPI Channel 0
#define TEMPERATURE_SENSORS 6

uint32_t pressureRead[PRESSURE_SENSORS];
uint32_t temperatureRead[TEMPERATURE_SENSORS];

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
const int ValveOpen = 1,
ValveClose = 0,
ValveStuck = 3,
ServoStuck = 3,
NozzleStuck = 3,
NozzleOpen = 1,
flight = 1,
test = 0;

int ExperimentStatus,
valveStatus = 0,
ValvePos = 0,
ValveCompleted = 0,
servoStatus = 0,
ServoRunning = 0,
nozzleStatus = 0,
NozzleOpened = 0,
TestStatus = 0,
LOSignal,
SoEReceived = 0,
EoE = 0,
modeSel,
dryRun,
testRun;

//Parameters Declaration
struct parameter {
	int Delay_OnGoingValve, Delay_to_OpenNozzleCover, Delay_to_EoE, Delay_NoseConeSeparation, Delay_to_NoseConeSeparation, Angle_Servo;
};
#define DEFAULT_PARAMETER \
	.Delay_OnGoingValve = 5000, \
	.Delay_to_OpenNozzleCover = 6000, \
	.Delay_to_EoE = 30000
//Unchangeable Parameters
#define Delay_PowerOff 1000
#define Delay_NozzleCoverFeedback 1500
#define Angle_ServoReset 0
#define Delay_ServoRetry 3000

//Default Parameters
struct parameter Standard = { DEFAULT_PARAMETER, .Delay_NoseConeSeparation = 10000, .Delay_to_NoseConeSeparation = 55000, .Angle_Servo = 90 };
struct parameter DEBUGstandard = { .Delay_to_NoseConeSeparation = 5000, .Delay_to_EoE = 3000 }; //For Debug Mode only

//FailSafe Experiment Status
typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, VALVE_OPENED, SERVO_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;

//EXPERIMENT
//Function receiving the SOE signal from the RPi
int SoESignal();
//Function to SetUp the Servo
void ServoRotation(int degree);
//Function in Experiment controlling the Valve operation
int ValveRun(struct parameter parameter, int modeSel);
//Function in Experiment controlling the Servo operation
int ServoRun(struct parameter parameter, int modeSel);
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
void ReadPressureSensors(uint32_t* Sensors);
//Read Temperature sensors from SPI
void ReadTemperatureSensors(uint32_t* Sensors);

//Mainboard Status
uint8_t mainboardStatus(uint8_t tempStat, uint8_t voltStat);
//Temperature Status
float temp_data(void);
uint8_t temp_stat(float temp);
//Voltage Status
uint8_t volt_stat(void);
