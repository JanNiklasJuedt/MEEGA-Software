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
#define Camera xx

#define RPi_SOE 41	//pin
#define RPi_LO 47	//pin

int main() {
	wiringPiSetupGpio();
	pinMode(Reservoir_Valve, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Nozzle_Servo, OUTPUT);
	pinMode(LEDs, OUTPUT);
	pinMode(Camera, OUTPUT);

	pinMode(ServoSwitch_1, INPUT);
	pinMode(ServoSwitch_2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);
	
	struct params config;

	ExperimentStatus = 0;
	
	while (1) {															//raspberryPi, keine angabe. datahandling, declaration and input.
		//int flightmode = 1;	//Flight Mode Switch ?	Get telecommand first row 2mode bits! command from groundstation serial? MODE is from getinpacket from datahandling
		//int testmode = 0;		//Test Mode Switch ?
		int LOSignal = digitalRead(RPi_LO);						

		struct DataPacket mode = GetInPacket(&buffer);	//get packet from buffer
		int modeBit = mode.mode;	//get mode bit from packet
		// Test Mode = 0, Flight Mode = 1
		if (modeBit == 1) {		//Flight Mode
			config = flightstandard;
			//Flight Mode
			if (LOSignal == HIGH) {
				if (SoESignal()) {
					ExperimentRun(config);
					//int stat = ExperimentRun(config);
					WriteSave(&buffer, "MEEGA_Experiment.bin");
					if (ExperimentRun(config) == 43 || ExperimentRun(config) == 404) break;	//End of Experiment
				}
			}
			else if (LOSignal == LOW) {
				ExperimentStatus = 0;
				continue;
			}
		}
		else if (modeBit == 0) {	//Test Mode							//Manuel abbrechen
			config = teststandard;
			//Test Mode
			if (SoESignal()) {
				ExperimentRun(config);
				WriteSave(&buffer, "MEEGA_Test.bin");
				ExperimentStatus = 0;
			}
			else {
				ExperimentControl();
			}
			continue;
		}
	}
	return 0;
}

int SoESignal() {
	return (digitalRead(RPi_SOE) == HIGH);	//Check if SoE signal is HIGH, if so, start experiment
}

struct params {
	char Mode[10];
	int ValveDelay, ServoDelay, EoEDelay, PoweroffDelay, FDA20, FDA2, OnCDelay, ServoOnCDelay; //FDA here is frames = frequency x duration. With FullData 20Hz & BasicData 2Hz
};
struct params flightstandard = { .Mode = "Flight", .ValveDelay = 5000, .ServoDelay = 2000, .EoEDelay = 30000, .PoweroffDelay = 1000, .OnCDelay = 200, .ServoOnCDelay = 500, .FDA20 = 500 }; 
struct params teststandard = { .Mode = "Test", .ValveDelay = 5000, .ServoDelay = 2000, .FDA2 = 5000};

int testAbort = 0;

int delay(int millisecond) {	//1000x Second
	clock_t start_time = clock();
	clock_t wait_time = (millisecond * CLOCKS_PER_SEC) / 1000;
	while (clock() < start_time + wait_time) if(testAbort) return 1;
	return 0;
}

int ValveOpen = 1, ValveClose = 0, ValveStuck = 3, valveStatus = 0, ValvePos = 0, ServoRun = 1, ServoStop = 0, ServoStuck = 3, servoStatus = 0, nozzleStatus = 0, NozzleStuck = 3, NozzlePos = 0, NozzleOpen = 1, EoE = 0, SoE = 0, LO = 0, ExperimentStatus;

int ExperimentRun(struct params parameter) {
	ExperimentStatus = 1;	//Experiment started
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
		if (parameter.Mode == "Test") {
			ExperimentStatus = 3;
			return 1;//abort test
		}
	}
	digitalWrite(Reservoir_Valve, ValveClose);	//command close valve
	delay(parameter.OnCDelay);					//delay for opening and closing valve 0,5s
	ValvePos = ValveClose;	//ValvePos = digitalRead(Valve)		//Feedback signal
	if (ValvePos == ValveClose) {
		//Valve is close
		valveStatus = ValveClose;
		delay(parameter.ServoDelay);
	}
	else {
		//Valve error: in open position / cont. error
		valveStatus = ValveStuck;
		if (parameter.Mode == "Test") {
			ExperimentStatus = 3;
			return 2;//abort test
		}
	}
	if (parameter.Mode == "Flight") {
		digitalWrite(LEDs, 1);					//LED on
		digitalWrite(Nozzle_Servo, ServoRun);	//command rotate the serve
		servoStatus = ServoRun;
		if (servoStatus == ServoRun) {
			delay(parameter.ServoOnCDelay);			//delay for opening and closing Servo 0.5s for 90°
			digitalWrite(Nozzle_Servo, ServoStop);	//command stop the servo
			servoStatus = ServoStop;
			delay(parameter.ServoOnCDelay);
			if (NozzlePos == digitalRead(ServoSwitch_1)) {
				//Feedback signal
				//Nozzle Cover Problem: in close position
				nozzleStatus = NozzleStuck;
				delay(parameter.EoEDelay);
				digitalWrite(LEDs, 0);			//LED off
				ExperimentStatus = 3;
				EoE = 2; //Unsuccessful End of Experiment NozzleStuck

				if (parameter.Mode == "Test") {
					ExperimentStatus = 3;
					return 4;//abort test
				}
			}
			else if (NozzlePos == digitalRead(ServoSwitch_2)) {
				//Feedback signal: Nozzle Cover is open
				nozzleStatus = NozzleOpen;
				delay(parameter.EoEDelay);
				digitalWrite(LEDs, 0);			//LED off
				EoE = 1; //Successful End of Experiment
			}
		}
		else if (servoStatus == ServoStop) {
			//Servo error: not running
			servoStatus = ServoStuck;
			ExperimentStatus = 3;
			if (parameter.Mode == "Test") {
				ExperimentStatus = 3;
				return 3;//abort test
			}
		}
	}
	else if (parameter.Mode == "Test") {
		digitalWrite(LEDs, 1);					//LED on
		nozzleStatus = NozzleOpen;				//simulate nozzle cover open
		delay(parameter.EoEDelay);
		digitalWrite(LEDs, 0);
		nozzleStatus = 0;						//Reset simulation of nozzle cover open
		ExperimentStatus = 2;
		delay(parameter.PoweroffDelay);
	}
	if (EoE == 1) {
		ExperimentStatus = 2;
		delay(parameter.PoweroffDelay);
		return 43;	//End of Experiment
	}
	else {
		ExperimentStatus = 3;
		delay(parameter.PoweroffDelay);
		return 404;	//Error in Experiment
	}
	return 0;
}

//BETA Control Panel Functions not yet implemented from DataHandling
int ExperimentControl() {
	ExperimentStatus = 1;
	while (1) {
		//Valve Control
		if (telecommand(&Valvecmd, sizeof(Valvecmd))) {
			if (Valvecmd == 1) {
				digitalWrite(Reservoir_Valve, ValveOpen);	//command open valve
			}
			else {
				digitalWrite(Reservoir_Valve, ValveClose);	//command close valve
			}
		}
		//Servo Control
			//manual control, command from control panel. Not yet implemented
		//LED Control
		if (telecommand(&LEDscmd, sizeof(LEDscmd))) {
			if (LEDscmd == 1) {
				digitalWrite(LEDs, 1);	//command turn on LEDs
			}
			else {
				digitalWrite(LEDs, 0);	//command turn off LEDs
			}
		}
		if (telecommand(&Cameracmd, sizeof(Cameracmd))) {
			if (Cameracmd == 1) {
				digitalWrite(Camera, 1);	//command turn on Camera
			}
			else {
				digitalWrite(Camera, 0);	//command turn off Camera
			}
		}
		if (telecommand(&cmd, sizeof(cmd))) {
			if (cmd == 0) break;
		}
	}

	return 0;
}

//Householding Data Acquisition
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

void DataAcquisition(struct DataFrame* frame) {
	int SystemTime = clock();	//System Time
	int AmbientPressure = analogRead(0);																//alle sensor daten etc lesen und in Data Handling int speichern. 2mode full & basic data acquisition. Hausholdong data speichern. 
	int CompareTemperature = analogRead(1);
	int TankPressure = analogRead(2);
	int TankTemperature = analogRead(3);
	int ChamberPressure = analogRead(4);
	int ChamberTemperature = analogRead(5);
	int NozzlePressure = analogRead(6);
	int NozzleTemperature = analogRead(7);
	int NozzleCover = digitalRead(ServoSwitch_2);	//Nozzle Cover Feedback: fully open
	int NozzleServo = digitalRead(Nozzle_Servo);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Reservoir_Valve);	//Reservoir Valve
	int Camerastat = digitalRead(Camera);
	int LEDsStat = digitalRead(LEDs);
	int Sensorboard = 0;		//Sensorboard is not implemented yet ?
	int Mainboard = 0;			//Mainboard is not implemented yet ?
	//Experiment Status CHECK!

	//Local
	WriteFrame(frame, id_System_Time, SystemTime);
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
	WriteFrame(frame, id_Camera, Camerastat);
	WriteFrame(frame, id_LEDs, LEDsStat);
	WriteFrame(frame, id_Sensorboard, Sensorboard);
	WriteFrame(frame, id_Mainboard, Mainboard);
	WriteFrame(frame, id_Experiment_Status, ExperimentStatus);

	//Transmit
	WriteTC(frame, id_System_Time, SystemTime);
	WriteTC(frame, id_Ambient_Pressure, AmbientPressure);
	WriteTC(frame, id_Compare_Temperature, CompareTemperature);
	WriteTC(frame, id_Tank_Pressure, TankPressure);
	WriteTC(frame, id_Tank_Temperature, TankTemperature);
	WriteTC(frame, id_Chamber_Pressure, ChamberPressure);
	WriteTC(frame, id_Chamber_Temperature, ChamberTemperature);
	WriteTC(frame, id_Nozzle_Pressure, NozzlePressure);
	WriteTC(frame, id_Nozzle_Temperature, NozzleTemperature);
	WriteTC(frame, id_Nozzle_Cover, NozzleCover);
	WriteTC(frame, id_Nozzle_Servo, NozzleServo);
	WriteTC(frame, id_Reservoir_Valve, ReservoirValve);
	WriteTC(frame, id_Camera, Camerastat);
	WriteTC(frame, id_LEDs, LEDsStat);
	WriteTC(frame, id_Sensorboard, Sensorboard);
	WriteTC(frame, id_Mainboard, Mainboard);
	WriteTC(frame, id_Experiment_Status, ExperimentStatus);
}

void Log(struct StorageHub* storage) {
	struct params freq;
	struct DataBuffer buffer;	//Initialize the DataBuffer
	int sync = 0;				//Sync value for the DataFrame
	int syncLimit = 0;			//Sync limit for the DataFrame, every 10 Frames a new Sync value is set

	while (1) {
		struct DataFrame frame = CreateFrame(sync++);
		DataAcquisition(&frame);	//DataAcquisition function to fill the frame with data
		AddSaveFrame(storage->savefile, frame);	//Add the frame to the save file
		AddBufferFrame(storage->buffer, frame);	//Add the frame to the buffer
		syncLimit++;
		if (syncLimit >= 10) {
			struct DataFrame upTC = CreateTC(sync++);	//Create a new TeleCommand DataFrame with the current sync value
			AddBufferTC(storage->buffer, upTC);			//Add the TeleCommand DataFrame to the buffer
			FormPackets(storage->buffer);				//Form the packets from the buffer
			syncLimit = 0;								//Reset the sync limit
		}

		if (SoESignal()) {
			delay(freq.FDA20);		//Full Data Acquisition 20Hz every 10 Frames
		}
		else {
			delay(freq.FDA2);		//Basic Data Acquisition 2Hz every 10 Frames
		}
	}
}
