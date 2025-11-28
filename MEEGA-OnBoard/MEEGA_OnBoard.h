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
#define ONBOARD_OS LINUX
#define MODE RELEASE
#define EXPERIMENT RUN
#define SERVO_VERSION SERVO_v1
#define SENSORS_SPI_VERSION SPIDEV


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

#elif (ONBOARD_OS == LINUX)

#include <wiringPi.h>	//Include wiringPi library for GPIO control
#include <sys/time.h>
#include <softPwm.h>	//Include softPwm library for PWM control without PWM-Board

#if (SENSORS_SPI_VERSION == WIRINGPISPI)

#include <wiringPiSPI.h>	//Include wiringPiSPI library for SPI control

#define SPI_TEMPERATURE 0	//SPI Channel 0
#define SPI_PRESSURE 1	//SPI Channel 1

#elif (SENSORS_SPI_VERSION == SPIDEV)

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

#define SPI_PRESSURE "/dev/spidev1.0"
#define SPI_TEMPERATURE "/dev/spidev0.0"
int SPI_fd_T = -1;
int SPI_fd_P = -1;
#endif

//SETUP for Sensors Reading
#define SPI_SPEED 1000000	//1MHz - MPR_P_SPI max 800kHz; AD7793_ADC max 4MHz; LTC2450_ADC max 2MHz  - Test with 500kHz, 1MHz
#define CMD_READ 0xA1 //Command to read data from the sensors

#define P_TxPACKET_LENGTH 17 //bytes
#define PRESSURE_SENSORS 6

#define T_TxPACKET_LENGTH 19 //bytes
#define TEMPERATURE_SENSORS 6

uint32_t pressureRead[PRESSURE_SENSORS];
uint32_t temperatureRead[TEMPERATURE_SENSORS];

#endif

//Global Variables Declaration
const int ValveOpen = 1,
ValveClose = 0,
ValveStuck = 3,
ServoOn = 1,
ServoOff = 0,
ServoStuck = 3,
NozzleStuck = 3,
NozzleOpen = 1,
LEDsOn = 0,
LEDsOff = 1,
flight = 1,
test = 0;

int
NozzleOpened = 0,
LOSignal = 0,
SoESignal = 0,
SoEReceived = 0,
EoE = 0,
modeSel = 1;

//Parameters
#define Delay_OnGoingValve 5000
#define Delay_to_OpenNozzleCover 6000
#define Delay_NoseConeSeparation 10000
#define Delay_to_NoseConeSeparation 55000
#define Delay_to_EoE 30000
#define Delay_PowerOff 1000
#define Delay_NozzleCoverFeedback 1500
#define Angle_ServoReset 91
#define Angle_Servo 0
#define Delay_ServoRetry 3000
#if (MODE == DEBUG)
#define Delay_to_NoseConeSeparation 5000
#define Delay_to_EoE 3000
#endif

//FailSafe Experiment Status
typedef enum { WAIT_LO, AFTER_LO, NOSECONE_SEPARATION, WAIT_SOE, AFTER_SOE, VALVE_CLOSED, SERVO_RUNNING, NOZZLE_OPENED, END_OF_EXPERIMENT } ExperimentState;
ExperimentState currentState = WAIT_LO;


//EXPERIMENT
//Function receiving the SOE signal from the RPi
//int SoESignal();
//Function to SetUp the Servo
void ServoInit(void);
void ServoRotation(int degree);
//Function in Experiment controlling the Valve operation
int ValveRun(int openDelay);
//Function in Experiment controlling the Servo operation
int ServoRun(int angle);
//Functiong in Test Mode manually controlling the Experiment from the Ground Station
void ExperimentControl();
//Waits or aborts if modeSel == test and Test_Abort in TC is true
int delay_abortable(int milliseconds);

//DATA LOGGING
//Function acquiring the Data from the Sensors and writing it into a DataFrame
void DataAcquisition(DataFrame* frame);
//Function running the Data Logging in a thread
void Log();
//Thread function for Data Logging
void* LogThread();
//FailSafe Function to recover the last experiment state
void FailSafeRecovery();

int InitializeSPI(const char* device);
void TransferSPI(int fd, uint8_t * txBuf, uint8_t * rxBuf, size_t length);
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
