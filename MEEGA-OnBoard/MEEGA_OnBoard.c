#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <wiringPi.h>
#include "MEEGA_DataHandling.c"

#define LEDs 54	//pin
#define Reservoir_Valve 29	//pin
#define Nozzle_Servo 34	//pin
#define ServoSwitch_1 50	// Deckel ganz zu Feedback
#define ServoSwitch_2 48	// Deckel ganz auf Feedback

#define RPi_SOE 41	//pin
#define RPi_LO 47	//pin
#define CS_PSB 37	//pin
#define CS_TSB 39	//pin

int main() {
	wiringPiSetupGpio();
	pinMode(Reservoir_Valve, output);	//output should be in wiringPi library as define output 1
	pinMode(Nozzle_Servo, output);
	pinMode(LEDs, output);

	pinMode(CS_PSB, input);				//input should be in wiringPi library as define input 1
	pinMode(CS_TSB, input);
	pinMode(RPi_SOE, input);
	pinMode(RPi_LO, input);
	
	struct params config;
	
	while (1) {															//raspberryPi, keine angabe. datahandling, declaration and input.
		int flightmode = digitalRead(CS_PSB);	//Flight Mode Switch
		int testmode = digitalRead(CS_TSB);		//Test Mode Switch
		int LOSignal = rBit(RPi_LO);						

		if (flightmode && !testmode) {		//Flight Mode
			config = flightstandard;
			//Flight Mode												//1.bit = lo; 2.bit = soe; 3.bit = eoe		alle mit binären signalen FIX!!!
			if (LOSignal == 1) {
				delay(config.SoEDelay);
				digitalWrite(LEDs, 1);							//LED on
				if (SoESignal()) {
					ExperimentRun(config);
				}
			}
			else if (LOSignal == 0) {
				continue;
			}
		}
		else if (testmode && !flightmode) {	//Test Mode							//Manuel abbrechen
			config = teststandard;
			//Test Mode
			if (SoESignal()) {
				ExperimentRun(config);
			}
		}
	}
	return 0;
}

int rBit(int gpiopin) {
	return digitalRead(gpiopin);	//returns the value of the pin, 0 or 1
}

int SoESignal() {
	while (1) {
		if (rBit(RPi_SOE) == 1) {
			return 1;
		}
		else if (rBit(RPi_SOE) == 0) {
			continue;
		}
	}
}

struct params {
	char Mode[10];
	int ValveDelay, ServoDelay, SoEDelay, EoEDelay, PoweroffDelay, FDA20, FDA2, OnCDelay, ServoOnCDelay; 
};
struct params flightstandard = { .Mode = "Flight", .SoEDelay = 550, .ValveDelay = 30, .ServoDelay = 60, .EoEDelay = 350, .PoweroffDelay = 10, .OnCDelay = 5, .ServoOnCDelay = 10, .FDA20 = 200 };
struct params teststandard = { .Mode = "Test", .ValveDelay = 30, .ServoDelay = 60, .FDA2 = 20};

int testAbort = 0;

int delay(int second) {	//10tel Sekunden
	int time = second * 100;
	clock_t start_time = clock();
	while (clock() < start_time + time) if(testAbort) return 1;
	return 0;
}

int ValveOpen = 1, ValveClose = 0, ValveStuck = 3, valveStatus = 0, ValvePos = 0,  ServoOpen = 1, ServoClose = 0, ServoStuck = 3, servoStatus = 0, ServoPos = 0, EoE = 0, SoE = 0, LO = 0;

int ExperimentRun(struct params parameter) {
	digitalWrite(Reservoir_Valve,ValveOpen);	//command open valve
	delay(parameter.OnCDelay);					//delay for opening and closing valve 0,5s
	ValvePos = ValveOpen;	//ValvePos = digitalRead(Valve)		//Feedback signal
	if (ValvePos == ValveOpen) {
		//Valve is open			
		valveStatus = ValveOpen;
		delay(parameter.ValveDelay);
	}
	else if (ValvePos == ValveClose) {//Valve error: in close position
		valveStatus = ValveStuck;
		if (parameter.Mode, "Test") return 1;//abort test
	}
	digitalWrite(Reservoir_Valve, ValveClose);	//command close valve
	delay(parameter.OnCDelay);					//delay for opening and closing valve 0,5s
	ValvePos = ValveClose;	//ValvePos = digitalRead(Valve)		//Feedback signal
	if (ValvePos == ValveClose) {
		//Valve is close
		valveStatus = ValveClose;
		delay(parameter.ServoDelay);
	}
	else if (ValvePos == ValveOpen) {
		//Valve error: in open position
		valveStatus = ValveStuck;
		if (parameter.Mode, "Test") return 2;//abort test	
	}
	if (parameter.Mode == "Flight") {
		digitalWrite(Nozzle_Servo, ServoOpen);	//command open nozzle
		delay(parameter.ServoOnCDelay);			//delay for opening and closing Servo 1s
		ServoPos = digitalRead(ServoSwitch_2);		//Feedback signal
		if (parameter.Mode == "Flight") {
			ServoPos = digitalRead(ServoSwitch_1);	//Feedback signal
			//Nozzle Cover Problem: in close position
			servoStatus = ServoStuck;
			if (parameter.Mode, "Test") return 3;//abort test
		}
	}
	else if (parameter.Mode == "Test") {
		printf("Simulating Nozzle Cover Open\n");					//simulate nozzle cover open
		delay(parameter.EoEDelay);
		digitalWrite(LEDs, 0);
		delay(parameter.FDA2);				//Basic Data Acquisition 2 seconds
		delay(parameter.PoweroffDelay);
		return 0;
	}
	if (ServoPos == ServoOpen) {
		//Nozzle Cover is open
		servoStatus = ServoOpen;
		delay(parameter.EoEDelay);
		digitalWrite(LEDs,0);				//LED off
		delay(parameter.FDA20);				//Full Dáta Acquisition 20 seconds
		EoE = 1;
	}
	if (EoE == 1) printf("End of Experiment\n"); delay(parameter.PoweroffDelay); return 0;	//End of Experiment
}

#define id_Ambient_Pressure "AmbientPressure"
#define id_Compare_Temperature "CompareTemperature"
#define id_Tank_Pressure "TankPressure"
#define id_Tank_Temperature "TankTemperature"
#define id_Chamber_Pressure "ChamberPressure"
#define id_Chamber_Temperature "ChamberTemperature"
#define id_Nozzle_Pressure "NozzlePressure"
#define id_Nozzle_Temperature "NozzleTemperature"
#define id_Nozzle_Cover "NozzleCover"
#define id_Nozzle_Servo "NozzleServo"
#define id_Reservoir_Valve "ReservoirValve"
#define id_Camera "Camera"
#define id_LEDs "LEDs"
#define id_Sensorboard "Sensorboard"
#define id_Mainboard "Mainboard"
#define id_System_Time "SystemTime"
#define id_Experiment_Status "ExperimentStatus"

void DataAquisition(struct DataFrame* frame) {
	int AmbientPressure = analogRead(0);																//alle sensor daten etc lesen und in Data Handling int speichern. 2mode full & basic data acquisition. Hausholdong data speichern. 
	int CompareTemperature = analogRead(1);
	int TankPressure = analogRead(2);
	int TankTemperature = analogRead(3);
	int ChamberPressure = analogRead(4);
	int ChamberTemperature = analogRead(5);
	int NozzlePressure = analogRead(6);
	int NozzleTemperature = analogRead(7);
	int NozzleCover = digitalRead(ServoSwitch_2);	//Nozzle Cover Feedback
	int NozzleServo = digitalRead(Nozzle_Servo);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Reservoir_Valve);	//Reservoir Valve
	int Camera = 0;				//Camera is not implemented yet ?
	int LEDsStat = digitalRead(LEDs);
	int Sensorboard = 0;		//Sensorboard is not implemented yet ?
	int Mainboard = 0;			//Mainboard is not implemented yet ?
	int SystemTime = clock();	//System Time
	int ExperimentStatus = 0;	//Experiment Status, 0 = not started, 1 = running, 2 = finished, 3 = error ?

	WriteFrame(frame, id_Ambient_Pressure, AmbientPressure);
	WriteFrame(frame, id_Compare_Temperature, CompareTemperature);
	WriteFrame(frame, id_Tank_Pressure, TankPressure);
	WriteFrame(frame, id_Tank_Temperature, TankTemperature);
	WriteFrame(frame, id_Chamber_Pressure, ChamberPressure);
	WriteFrame(frame, id_Chamber_Temperature, ChamberTemperature);
	WriteFrame(frame, id_Nozzle_Pressure, NozzlePressure);
	WriteFrame(frame, id_Nozzle_Temperature, NozzleTemperature);
	WriteFrame(frame, id_Nozzle_Cover, NozzleCover);
	WriteFrame(frame, id_Nozzle_Servo, NozzleServo);
	WriteFrame(frame, id_Reservoir_Valve, ReservoirValve);
	WriteFrame(frame, id_Camera, Camera);
	WriteFrame(frame, id_LEDs, LEDsStat);
	WriteFrame(frame, id_Sensorboard, Sensorboard);
	WriteFrame(frame, id_Mainboard, Mainboard);
	WriteFrame(frame, id_System_Time, SystemTime);
	WriteFrame(frame, id_Experiment_Status, ExperimentStatus);
	return;
}
