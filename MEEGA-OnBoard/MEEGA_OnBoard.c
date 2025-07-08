#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <wiringPi.h>
#define LED 54
#define Valve 29
#define Servo 34

int main() {
	wiringPiSetupGpio();
	pinMode(Valve, output);		//output should be in wiringPi library as define output 1
	pinMode(Servo, output);
	pinMode(LED, output);
	struct params config;
	
	while (1) {
		printf("Select Mode (Flight / Test): ");
		fgets(config.Mode, sizeof(config.Mode), stdin);
		config.Mode[strcspn(config.Mode, "\n")] = 0;

		if (strcmp(config.Mode, "Flight") == 0) {
			config = flightstandard;
			printf("Flight Mode\n");
			printf("\nLO Signal (y/n): ");
			char LO[4];
			fgets(LO, sizeof(LO), stdin);
			LO[strcspn(LO, "\n")] = 0;
			if (strcmp(LO, "y") == 0) {
				delay(config.SoEDelay);
				digitalWrite(LED, 1);							//LED on
				while (1) {
					char SoE[4];
					printf("\nSoE Signal (y/n): ");					
					fgets(SoE, sizeof(SoE), stdin);
					SoE[strcspn(SoE, "\n")] = 0;
					if (strcmp(SoE, "y") == 0) {
						ExperimentRun(config);
						break;									//Back to mode selection?
					}
					else if (strcmp(SoE, "n") == 0) {
						continue;
					}
				}	
			}
			else if (strcmp(LO, "n") == 0) {
				continue;
			}
			else {
				continue;
			}
		}
		else if (strcmp(config.Mode, "Test") == 0) {
			config = teststandard;
			printf("Test Mode\n");
			while (1) {
				printf("\nSoE Signal (y/n): ");
				char SoE[4];
				fgets(SoE, sizeof(SoE), stdin);
				SoE[strcspn(SoE, "\n")] = 0;
				if (strcmp(SoE, "y") == 0) {
					ExperimentRun(config);
					break;
				}
				else if (strcmp(SoE, "n") == 0) {
					continue;
				}
			}
		}
	}

	return 0;
}

struct params {
	char Mode[10];
	int ValveDelay, ServoDelay, SoEDelay, EoEDelay, PoweroffDelay, FDA20, FDA2;
	double OnCDelay;
};
struct params flightstandard = { .Mode = "Flight", .SoEDelay = 55, .ValveDelay = 3, .ServoDelay = 6, .EoEDelay = 35, .PoweroffDelay = 1, .OnCDelay = 0.5, .FDA20 = 20 };
struct params teststandard = { .Mode = "Test", .ValveDelay = 3, .ServoDelay = 6, .FDA2 = 2};

int testAbort = 0;
int delay(int second) {
	int time = second * 1000;
	clock_t start_time = clock();
	while (clock() < start_time + time) if(testAbort) return 1;
	return 0;
}

int ValveOpen = 1, ValveClose = 0, ValveStuck = 3, valveStatus = 0, ValvePos = 0,  ServoOpen = 1, ServoClose = 0, ServoStuck = 3, servoStatus = 0, ServoPos = 0, EoE = 0, SoE = 0, LO = 0;

int ExperimentRun(struct params parameter) {
	digitalWrite(Valve,ValveOpen);								//command open valve
	ValvePos = digitalRead(Valve);	//FIX no Feedback signal
	if (ValvePos == ValveOpen) {
		delay(parameter.OnCDelay);								//delay for opening and closing valve
		printf("Valve is open\n");			
		valveStatus = ValveOpen;
		delay(parameter.ValveDelay);
	}
	else if (ValvePos == ValveClose) {
		printf("Valve error: in close position\n");
		valveStatus = ValveStuck;
		if (strcmp(parameter.Mode, "Test") == 0) return 1;				//abort test
	}
	digitalWrite(Valve, ValveClose);							//command close valve
	ValvePos = digitalRead(Valve);	//FIX no Feedback signal
	if (ValvePos == ValveClose) {								
		delay(parameter.OnCDelay);
		printf("Valve is close\n");	
		valveStatus = ValveClose;
		delay(parameter.ServoDelay);
	}
	else if (ValvePos == ValveOpen) {							
		printf("Valve error: in open position\n");
		valveStatus = ValveStuck;
		if (strcmp(parameter.Mode, "Test") == 0) return 2;				//abort test	
	}
	if (parameter.Mode == "Flight") {
		digitalWrite(Servo, ServoOpen);								//command open nozzle
		ServoPos = digitalRead(Servo);	//FIX no Feedback signal
	}
	else if (parameter.Mode == "Test") {
		printf("Simulating Nozzle Cover Open\n");					//simulate nozzle cover open
		delay(parameter.EoEDelay);
		digitalWrite(LED, 0);
		delay(parameter.FDA2);										//Basic Data Acquisition 2 seconds
		delay(parameter.PoweroffDelay);
		return 0;
	}
	if (ServoPos == ServoOpen) {
		delay(parameter.OnCDelay);
		printf("Nozzle Cover Opened\n");	
		servoStatus = ServoOpen;
		delay(parameter.EoEDelay);
		digitalWrite(LED,0);										//LED off
		delay(parameter.FDA20);										//Full Dáta Acquisition 20 seconds
		EoE = 1;
	}
	else if (ServoPos == ServoClose) {
		printf("Nozzle Cover Problem: in close position\n");
		servoStatus = ServoStuck;
		if (strcmp(parameter.Mode, "Test") == 0) return 3;				//abort test
	}

	if (EoE == 1) printf("End of Experiment\n"); delay(parameter.PoweroffDelay); return 0;			//End of Experiment
}

void DataAquisition() {
	return;
}
