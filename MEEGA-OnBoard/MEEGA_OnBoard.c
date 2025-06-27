#include <math.h>
#include <stdio.h>
#include <time.h>
//#include <wiringPi.h>
//#define LED xx
//#define valve xx

int main() {
	//Here comes the money
	return 0;
}

struct params {
	int Mode;
};

void delay(int second) {
	int time = second * 1000;
	clock_t start_time = clock();
	while (clock() < start_time + time);
}

int ExperimentRun(struct params parameter) {
	//wiringPiSetup();
	//pinMode(valve,output);
	if (1) {
		//digitalWrite(valve,1);
		printf("Valve Opened\n");			//command open valve
		delay(3);
	}
	else {
		printf("Valve error: in close position\n");
		return;
	}
	if (1) {								//value depends on valve position
		//digitalWrite(valve,0);
		printf("Valve Closed\n");			//command close valve
		delay(6);
	}
	else if (0) {							//value depends on valve position
		printf("Valve error: in open position\n");
		return;
	}
	if (1) {
		printf("Nozzle Cover Opened\n");	//command open nozzle
		delay(35);
	}
	else {
		printf("Nozzle Cover Problem: in close position\n");
		return;
	}
	
	int EoE = 1;
	printf("End of Experiment\n");
	return 0;
}

void DataAquisition() {
	return;
}
