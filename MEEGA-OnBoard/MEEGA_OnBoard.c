#include "MEEGA_OnBoard.h"

//START OF MAIN PROGRAM
int main() {
#if (MODE == RELEASE)
	wiringPiSetupGpio();
	wiringPiSPISetup(SPI_PRESSURE, SPI_SPEED);
	wiringPiSPISetup(SPI_TEMPERATURE, SPI_SPEED);
#endif
	pinMode(Valve_Pin, OUTPUT);	//output should be in wiringPi library as define output 1
	pinMode(Servo_Pin, OUTPUT);
	pinMode(LEDs_Pin, OUTPUT);
	pinMode(Servo_On, OUTPUT);

	pinMode(Nozzle_Cover_S1, INPUT);
	pinMode(Nozzle_Cover_S2, INPUT);
	pinMode(RPi_SOE, INPUT);			//input should be in wiringPi library as define input 1
	pinMode(RPi_LO, INPUT);

	softPwmCreate(Servo_Pin, 0, 200); //50Hz refresh rate, cycle: 20ms/50Hz

#if (MODE == RELEASE)
	pullUpDnControl(RPi_LO, PUD_UP);
	pullUpDnControl(RPi_SOE, PUD_UP);
#endif

	Initialize();
	FailSafeRecovery();

	//Experiment: Lift_Off; Start_Experiment; End_Experiment; Mode
	struct parameter config;

	pthread_t logThread;
	//create a thread that runs LogThread function: success->parallel programm; failure->no threads logging and return to NULL
	//using if to let know if there is/are problem(s)
	if (pthread_create(&logThread, NULL, LogThread, (void*)&config)) {	//Create a thread for logging
		//LED blink for 5 times: logging thread failed to start
		for (int i = 0;i < 5;i++) {
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
		LOSignal = digitalRead(RPi_LO);

		//RESET
		//TestStatus = 0;
		SoEReceived = 0;
		ServoRotation(Angle_ServoReset);
		digitalWrite(Servo_On, 0);
		//RESET

#if (MODE == DEBUG)
		int modeSel;
		printf("*Mode selection 1 for Flight, 0 for Test: "); scanf_s("%d", &modeSel);
#elif (MODE == RELEASE)
		DataFrame modeFrame = GetTC(); //Update the Tele Command frame from the Telemetry buffer
		modeSel = ReadFrame(modeFrame, Mode_Change);	//Read the mode change from the Tele Command
#endif
		// Test Mode = 0, Flight Mode = 1

		if (modeSel == flight) {		//Flight Mode
			config = Standard;
#if (MODE == DEBUG)
			printf("*LO Signal? 1 for YES, 0 for NO: "); scanf_s("%d", &LOSignal);
#endif
			if (LOSignal == 0) continue; //-------------------------------------------------------------------change to HIGH if connected to RaspberryPi PULL UP resistor

			while (1) {
				switch (currentState) {
				case WAIT_LO:
					if (LOSignal == 1) {	//----------------------------------------------------------------change to LOW if connected to RaspberryPi PULL UP resistor
#if (EXPERIMENT == TEST)
						printf("Lift Off Signal Received\n");
#endif
						currentState = AFTER_LO;
					}
					break;

				case AFTER_LO:
#if (MODE == DEBUG)
					delay(DEBUGstandard.Delay_to_NoseConeSeparation);
#elif (MODE == RELEASE)
					delay(config.Delay_to_NoseConeSeparation);	//Wait for 55s after liftoff
#endif
					currentState = NOSECONE_SEPARATION;
					break;

				case NOSECONE_SEPARATION:
					digitalWrite(LEDs_Pin, 1);	//LED on
#if (MODE == DEBUG)
					printf("Nose Cone Separation\n");
#endif
#if (EXPERIMENT == TEST)
					printf("Nose Cone Separation\n");
#endif
					delay(config.Delay_NoseConeSeparation);			//Wait for Nozzle Cone Separation
					digitalWrite(LEDs_Pin, 0);	//LED off
					currentState = WAIT_SOE;
					break;

				case WAIT_SOE:
					while (!SoESignal()) delay(100);
					SoEReceived = 1;
#if (EXPERIMENT == TEST)
					printf("SoE Signal Received\n");
#endif
					digitalWrite(Servo_On, 1);
					digitalWrite(LEDs_Pin, 1);
					currentState = VALVE_OPENED;
					break;

				case VALVE_OPENED:
					if (!ValveCompleted) {
						int ValveRunStatus = ValveRun(config,flight);
						ValveCompleted = 1;
					}
					currentState = SERVO_RUNNING;
					break;

				case SERVO_RUNNING:
					if (!NozzleOpened) {
						int ServoStatus = ServoRun(config,flight);
						ServoRunning = 1;
					}
					currentState = NOZZLE_OPENED;
					break;

				case NOZZLE_OPENED:
					NozzleOpened = 1;
					digitalWrite(Servo_On, 0);
					digitalWrite(LEDs_Pin, 0);			//LED off
					currentState = END_OF_EXPERIMENT; //End of Experiment
					break;
				case END_OF_EXPERIMENT:
					if (EoE == 1) {
#if (MODE == DEBUG || EXPERIMENT == TEST)
						printf("Experiment: Successful\n");
#endif
#if (MODE == DEBUG || EXPERIMENT == TEST)
						printf("End of Experiment: Successful\n");
#endif
						delay(Delay_PowerOff);
						CloseAll();	//Close all files and threads
						return 43;	//End of Experiment
					}
					else {
#if (MODE == DEBUG)
						printf("End of Experiment: Error\n");
#endif
						delay(Delay_PowerOff);
						CloseAll();	//Close all files and threads
						return 404;	//Error in Experiment
					}
					break;
				}
			}
			EoECompleted = 1;
			break;
		}
		else if (modeSel == test) {	//Test Mode
#if (MODE == DEBUG)
			config = Standard;
			SoEReceived = 1;
			printf("SoE Signal Received\n");
			int valveTest = ValveRun(config,test);
			if (valveTest != -1) {
				int servoTest = ServoRun(config,test);
				if (servoTest == -1) {
					digitalWrite(Servo_On, 0);
					digitalWrite(LEDs_Pin, 0);
					continue;
				}
			}
			else if (valveTest == -1) {
				digitalWrite(Servo_On, 0);
				digitalWrite(LEDs_Pin, 0);
				continue; //abort test
			}
#elif (MODE == RELEASE)
			DataFrame FrameTC = GetTC();
			dryRun = ReadFrame(FrameTC, Dry_Run);
			testRun = ReadFrame(FrameTC, Test_Run);

			if (testRun == 1) {
				SoEReceived = 1;
				digitalWrite(Servo_On, 1);
				digitalWrite(LEDs_Pin, 1);
				config = Standard;
				config.Angle_Servo = (dryRun == 1) ? 30 : 90;
				
				int GS_Delay_OnGoingValve = ReadFrame(FrameTC, Valve_Delay); //Changeable Valve Delay from Ground Station
				int GS_Delay_to_OpenNozzleCover = ReadFrame(FrameTC, Servo_Delay); //Changeable Servo Delay from Ground Station
				int GS_Delay_to_EoE = ReadFrame(FrameTC, EoE_Delay);	 //Changebale End of Experiment Delay from Ground Station

				config.Delay_OnGoingValve = (GS_Delay_OnGoingValve != 0) ? GS_Delay_OnGoingValve : Standard.Delay_OnGoingValve; 	//If the value from ground station is 0, use the default value
				config.Delay_to_OpenNozzleCover = (GS_Delay_to_OpenNozzleCover != 0) ? GS_Delay_to_OpenNozzleCover : Standard.Delay_to_OpenNozzleCover; 	//If the value from ground station is 0, use the default value
				config.Delay_to_EoE = (GS_Delay_to_EoE != 0) ? GS_Delay_to_EoE : Standard.Delay_to_EoE;				//If the value from ground station is 0, use the default value

				if(dryRun == 0) {
					int valveTest = ValveRun(config,test);
					if (valveTest == -1) {
						digitalWrite(LEDs_Pin, 0);
						digitalWrite(Servo_On, 0);
						continue; //abort test
					}
				}
				else if (testRun == 1 && dryRun == 1) {
					int servoTest = ServoRun(config, test);
					if (servoTest == -1) {
						digitalWrite(LEDs_Pin, 0);
						digitalWrite(Servo_On, 0);
						continue; //abort test
					}
				}
			}
			
			else {
				ExperimentControl();
				if (ExperimentControl() == 0) continue;
				
			}

#endif
			TestStatus = 0; //Reset Test Status

			continue;
		}
	}
	return 0;
}
//END OF MAIN PROGRAM



//START OF EXPERIMENT PROGRAM
//Valve Control Function
int ValveRun(struct parameter parameter, int modeSel) {
#if (MODE == RELEASE)
	DataFrame FrameTC = GetTC();
#endif
	digitalWrite(Valve_Pin, ValveOpen);	//command open valve
#if (MODE == DEBUG)
	printf("Command opening Valve\n");
	ValvePos = digitalRead(ValveSwitch);		//Feedback signal
	ValvePos = ValveOpen; //For debug testing
	printf("*Input Valve 1 for open, 0 for close (std: open): "); scanf_s("%d", &ValvePos); //scanf_s is just for safety and used only in debug mode in visual studio
#elif (MODE == RELEASE)
	ValvePos = ValveOpen;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveOpen) {
		//Valve is open			
#if (MODE == DEBUG)
		printf("Valve Status: Valve is opened\n");
#elif (MODE == RELEASE)
		valveStatus = ValveOpen;
#endif
		delay(parameter.Delay_OnGoingValve);
	}
	else if (ValvePos == ValveClose) {//Valve error: in close position
#if (MODE == DEBUG)
		printf("Valve Status: Valve is stuck in close position\n");
#elif (MODE == RELEASE)
		valveStatus = ValveStuck;
#endif
		if (modeSel == test) {
#if (MODE == DEBUG)
			printf("Valve Error Code 1, Return ...\n");
			return -1;
#elif (MODE == RELEASE)
			FrameTC = GetTC();
			if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
#endif
		}
	}
	digitalWrite(Valve_Pin, ValveClose);	//command close valve
#if (MODE == DEBUG)
	printf("Command closing Valve\n");
	printf("*Input Valve 1 for open, 0 for close (std: close): "); scanf_s("%d", &ValvePos);
#elif (MODE == RELEASE)
#if (EXPERIMENT == TEST)
	printf("Valve Status: Valve is closed\n");
#endif
	ValvePos = ValveClose;	//ValvePos = digitalRead(ValveSwitch)		//Feedback signal
#endif
	if (ValvePos == ValveClose) {
		//Valve is close
#if (MODE == DEBUG)
		printf("Valve Status: Valve is closed\n");
#elif (MODE == RELEASE)
#if (EXPERIMENT == TEST)
		printf("Valve Status: Valve is closed\n");
#endif
		valveStatus = ValveClose;
#endif
		delay(parameter.Delay_to_OpenNozzleCover);
	}
	else if (ValvePos == ValveOpen) {
		//Valve error: in open position / cont. error
#if (MODE == DEBUG)
		printf("Valve Status: Valve is stuck in open position\n");
#elif (MODE == RELEASE)
		valveStatus = ValveStuck;
#endif
		if (modeSel == test) {
#if (MODE == DEBUG)
			printf("Valve Error Code 2, Return ...\n");
			return -1;
#elif (MODE == RELEASE)
			FrameTC = GetTC();
			if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
#endif
		}
	}
	return 0;
}

//Servo Control Function
int ServoRun(struct parameter parameter, int modeSel) {
#if (MODE == RELEASE)
	DataFrame FrameTC = GetTC();
#endif
	if (modeSel == flight) {
		ServoRotation(parameter.Angle_Servo); //command rotate the serve 90� first attempt*
#if (MODE == DEBUG)
		printf("Command to run Servo\n");
		printf("Servo run for 90 Degree\n");
#endif
		delay(Delay_NozzleCoverFeedback);
#if (MODE == DEBUG)
		printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
		if (NozzlePos == 1) {
#elif (MODE == RELEASE)
		if (digitalRead(Nozzle_Cover_S2)) {
#endif
			//Feedback signal
#if (MODE == DEBUG)
			printf("Nozzle Cover is opened\n");
#elif (MODE == RELEASE)
#if (EXPERIMENT == TEST)
			printf("Nozzle Cover is opened\n");
#endif
			nozzleStatus = NozzleOpen;
#endif
#if (MODE == DEBUG)
			delay(DEBUGstandard.Delay_to_EoE);
#elif (MODE == RELEASE)
			delay(parameter.Delay_to_EoE);
#endif
			EoE = 1; //Successful End of Experiment
		}
#if (MODE == DEBUG)
		else if (NozzlePos == 0) {
#elif (MODE == RELEASE)
		else if (digitalRead(Nozzle_Cover_S1)) {
#if (EXPERIMENT == TEST)
			printf("Second attempt\n");
			printf("Servo run for 90 Degree\n");
#endif
#endif
			//Nozzle Cover Problem: in close position
			ServoRotation(parameter.Angle_Servo); //command rotate the serve 90� second attempt*
#if (MODE == DEBUG)
			printf("Second attempt\n");
			printf("Servo run for 90 Degree\n");
			printf("*Input Nozzle Status 1 for fully open, 0 for stuck close (std: fully open): "); scanf_s("%d", &NozzlePos);
#endif
			delay(Delay_NozzleCoverFeedback);
#if (MODE == DEBUG)
			if (NozzlePos == 1) {
#elif (MODE == RELEASE)
			if (digitalRead(Nozzle_Cover_S2)) {
#if (EXPERIMENT == TEST)
				printf("Nozzle Cover is opened\n");
#endif
#endif
#if (MODE == DEBUG)
				printf("Nozzle Cover is opened\n");
#endif
				nozzleStatus = NozzleOpen;

#if (MODE == DEBUG)
				delay(DEBUGstandard.Delay_to_EoE);
#elif (MODE == RELEASE)
				delay(parameter.Delay_to_EoE);
#endif
				EoE = 1; //Successful End of Experiment
			}
			else {
				//Attempt to open the nozzle cover
				int Nozzle_Cover = 0; // Close
				for (int i = 0; i < 3; i++) {	//-------------------------------------------------CHANGEABLE NUMBER OF ATTEMPTS--------------------------------------------------
#if (MODE == DEBUG)
					printf("Attempt open nozzle: "); scanf_s("%d", &NozzlePos);
					delay(Delay_NozzleCoverFeedback);
#elif (MODE == RELEASE)
#if (EXPERIMENT == TEST)
					printf("Attempt %d to open nozzle\n", i + 1);
#endif
					digitalWrite(Servo_Pin, 1);
					delay(Delay_ServoRetry);
					digitalWrite(Servo_Pin, 0);
					delay(Delay_NozzleCoverFeedback);
#endif
#if (MODE == DEBUG)
					if (NozzlePos == 1) {
#elif (MODE == RELEASE)
					if (digitalRead(Nozzle_Cover_S2)) {
#endif
						Nozzle_Cover = 1; // Open
						EoE = 1;
						break;
					}
					}

				if (Nozzle_Cover == 1) {
#if (MODE == DEBUG)
					printf("Nozzle Cover is opened\n");
#elif (MODE == RELEASE)
#if (EXPERIMENT == TEST)
					printf("Nozzle Cover is opened\n");
#endif
					nozzleStatus = NozzleOpen;
#endif
					delay(parameter.Delay_to_EoE);
					EoE = 1; //Successful End of Experiment
				}
#if (MODE == DEBUG)
				else if (NozzlePos == 0) printf("Nozzle Cover is stuck in close position\n");
#elif (MODE == RELEASE)
				else if (digitalRead(Nozzle_Cover_S1)) nozzleStatus = NozzleStuck;
#endif
				}
			}
			}
	else if (modeSel == test) {
#if (MODE == DEBUG)
		printf("Simulating nozzle cover open (Success = 1; Fail = 0): "); scanf_s("%d", &NozzlePos);
		if (NozzlePos == 0) {
			printf("End of Experiment: Test Mode Error\n");
			//TestStatus = 99;
			return -1; //abort test
		}
#elif (MODE == RELEASE)
		ServoRotation(parameter.Angle_Servo);
		delay(Delay_NozzleCoverFeedback);
		FrameTC = GetTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
		//-----------------------------------------------------------------------------------------------------FIX ANGLE SERVO IN DRY RUN----------------------------------------------------------------
		if (dryRun && parameter.Angle_Servo <= 10) {
#if (MODE == DEBUG)
			printf("End of Experiment: Test Mode Error\n");
#endif
			//TestStatus = 99;
			FrameTC = GetTC();
			return -1; //abort test
		}
		else if (dryRun && parameter.Angle_Servo >= 30) {
			ServoRotation(Angle_ServoReset); //command rotate the serve 90� first attempt*
#if (MODE == DEBUG || EXPERIMENT == TEST)
			printf("End of Experiment: Test Mode\n");
#endif
			TestStatus = 70;
		}
		else if (testRun && digitalRead(Nozzle_Cover_S2)) {
			TestStatus = 70;
		}
		else if (testRun && digitalRead(Nozzle_Cover_S1)) {
			//TestStatus = 99;
			FrameTC = GetTC();
			return -1; //abort test
		}
		FrameTC = GetTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
		
#endif
#if (MODE == DEBUG)
		delay(DEBUGstandard.Delay_to_EoE);
#elif (MODE == RELEASE)
		FrameTC = GetTC();
		if (ReadFrame(FrameTC, Test_Abort) == 1) return -1; //abort test
		delay(parameter.Delay_to_EoE);
#endif
		nozzleStatus = 0;						//Reset simulation of nozzle cover open
		delay(Delay_PowerOff);
	}
	return 0;
}

#if (MODE == RELEASE)
//Control Panel Function
int ExperimentControl() {
	while (1) {
		DataFrame FrameTC = GetTC();
		//Valve Control
		if (!FrameIsEmpty(FrameTC)) {

			//Valve Control
			if (ReadFrame(FrameTC, Valve_Control) == 1) digitalWrite(Valve_Pin, ValveOpen);	//command open valve
			else if (ReadFrame(FrameTC, Valve_Control) == 0) digitalWrite(Valve_Pin, ValveClose);	//command close valve

			//LEDs Control
			if (ReadFrame(FrameTC, LED_Control) == 1) digitalWrite(LEDs_Pin, 1);	//command open valve
			else if (ReadFrame(FrameTC, LED_Control) == 0) digitalWrite(LEDs_Pin, 0);	//command close valve

			//Servo Control
			if (ReadFrame(FrameTC, Servo_Control) >= 0 && ReadFrame(FrameTC, Servo_Control) <= 90) ServoRotation(ReadFrame(FrameTC, Servo_Control));	//command rotate the servo to the specified degree
		}
		delay(500);
	}
	return 0;
}
#endif
//END OF EXPERIMENT PROGRAM



//START OF DATA ACQUISITION PROGRAM
//Data Acquisition Function
void DataAcquisition(DataFrame * frame) {
#if (MODE == DEBUG)
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
	int NozzleCover_1 = 0;	//Nozzle Cover Feedback: fully close
	int NozzleCover_2 = 1;	//Nozzle Cover Feedback: fully open
	int NozzleServo = 1;	//Nozzle Servo Switch
	int ReservoirValve = 1;	//Reservoir Valve
	int LEDsStat = 1;
	int Sensorboard_Pressure = 0;		//Sensorboard is not implemented yet ?
	int Sensorboard_Temperature = 0;
	int mainboard = 0;			//Mainboard is not implemented yet ?
	int ExperimentStatus = 1;
#elif (MODE == RELEASE)
	//Sensor Readings Declaration
	ReadPressureSensors(pressureRead);
	ReadTemperatureSensors(temperatureRead);

	//Mainboard Functions Declaration
	float mainboard_Temp = temp_data();
	uint8_t Mainboard_TempStat = temp_stat(mainboard_Temp);
	uint8_t Mainboard_VoltStat = volt_stat();

	int SystemTime = clock();	//System Time
	uint32_t AmbientPressure = pressureRead[0];
	uint32_t CompareTemperature = temperatureRead[0];
	uint32_t TankPressure = pressureRead[1];
	uint32_t TankTemperature = temperatureRead[1];
	uint32_t ChamberPressure = pressureRead[2];
	uint32_t ChamberTemperature = temperatureRead[2];
	uint32_t NozzlePressure_1 = pressureRead[3];
	uint32_t NozzlePressure_2 = pressureRead[4];
	uint32_t NozzlePressure_3 = pressureRead[5];
	uint32_t NozzleTemperature_1 = temperatureRead[3];
	uint32_t NozzleTemperature_2 = temperatureRead[4];
	uint32_t NozzleTemperature_3 = temperatureRead[5];
	int NozzleCover_1 = digitalRead(Nozzle_Cover_S1);	//Nozzle Cover Feedback: fully close
	int NozzleCover_2 = digitalRead(Nozzle_Cover_S2);	//Nozzle Cover Feedback: fully open
	int NozzleServo = digitalRead(Servo_Pin);	//Nozzle Servo Switch
	int ReservoirValve = digitalRead(Valve_Pin);	//Reservoir Valve
	int LEDsStat = digitalRead(LEDs_Pin);
	int Sensorboard_Pressure = pressureRead[6];
	int Sensorboard_Temperature = temperatureRead[6];
	uint8_t mainboard = mainboardStatus(Mainboard_TempStat, Mainboard_VoltStat);
#endif //MODE

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
	WriteFrame(frame, Nozzle_Closed, NozzleCover_1);
	WriteFrame(frame, Nozzle_Open, NozzleCover_2);
	WriteFrame(frame, Nozzle_Servo, NozzleServo);
	WriteFrame(frame, Reservoir_Valve, ReservoirValve);
	WriteFrame(frame, LEDs, LEDsStat);
	WriteFrame(frame, Sensorboard_P, Sensorboard_Pressure);
	WriteFrame(frame, Sensorboard_T, Sensorboard_Temperature);
	WriteFrame(frame, Mainboard, mainboard);
	WriteFrame(frame, Mode, modeSel);
	WriteFrame(frame, Lift_Off, LOSignal);
	WriteFrame(frame, Start_Experiment, SoEReceived);
	WriteFrame(frame, End_Experiment, EoE);
	WriteFrame(frame, Experiment_State, currentState);
}

void Log() {
	while (1) {
#if (ONBOARD_OS == WINDOWS)
		clock_t start = clock();
#elif (ONBOARD_OS == LINUX)
		struct timeval start, end;
		gettimeofday(&start, NULL);
#endif
		DataFrame frame = CreateFrame();
		DataAcquisition(&frame);	//DataAcquisition function to fill the frame with data
		AddFrame(frame);	//func from UPDATED DataHandlingLib
		UpdateAll();

		if (SoEReceived == 1) {
#if (ONBOARD_OS == WINDOWS)
			//printf("Full Data Acquisition\n");
			clock_t end = clock();
			long duration = ((end - start) * 1000) / CLOCKS_PER_SEC;
			long wait = (1000 * 1 / 20) - duration;	//Full Data 20Hz Frequency -> 50ms period
			if (wait > 0) delay(wait);
#elif (ONBOARD_OS == LINUX)
			gettimeofday(&end, NULL);
			suseconds_t duration = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
			suseconds_t wait = (1000000 * 1 / 20) - duration;	//Full Data 20Hz Frequency -> 50000us period
			if (wait > 0) usleep(wait);
#endif
		}
		else {
#if (ONBOARD_OS == WINDOWS)
			//printf("Basic Data Acquisition\n");
			delay(1000 * 1 / 2);		//Basic Data 2Hz Frequency -> 500ms period
#elif (ONBOARD_OS == LINUX)
			gettimeofday(&end, NULL);
			suseconds_t duration = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
			suseconds_t wait = (1000000 * 1 / 2) - duration;	//Basic Data 2Hz Frequency -> 500000us period
			if (wait > 0) usleep(wait);
#endif
		}
		if (modeSel == test) {
#if (MODE == DEBUG)
			if (Abort == 1) SoEReceived = 0;
#elif (MODE == RELEASE)
			if (ReadFrame(GetTC(), Test_Abort)) SoEReceived = 0;
#endif
		}
		else if (TestStatus == 70) SoEReceived = 0;
		else SoEReceived = 0;
	}
}
void* LogThread(void* arg) {
	Log();	//Start the logging function
	return NULL;	//Return NULL to end the thread
}
//END OF DATA ACQUISITION PROGRAM



//Receiving SoE Signal from RaspberryPi
int SoESignal() {
#if (ONBOARD_OS == WINDOWS)
	int SoE;
	printf("*SoE Signal? 1 for YES, 0 for NO: "); scanf_s("%d", &SoE);
	if (SoE == 1) return (digitalRead(RPi_SOE) == 0);
	else return (digitalRead(RPi_SOE) == 1);
#elif (ONBOARD_OS == LINUX)
	return (digitalRead(RPi_SOE) == LOW);	//PULL UP Resistor using LOW. Func. -> Check if SoE signal is HIGH, if so, start experiment. change to HIGH if connected to RaspberryPi
#endif //ONBOARD_OS
}



//Servo Control Function
 //The servo 90� rotation is 1ms=0� to 2ms=90�
void ServoRotation(int degree) {
#if (SERVO_VERSION == SERVO_v1)
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	//Range: 1000-2000us Theoretisch; Range: 1050-2050us Real (Excel Table and Calculation)
	int minR = 1000;
	int maxR = 2000;
	int pulse_us = minR + degree * (maxR - minR) / 90;
	int pwmWidth = pulse_us / 100;	//pwm Width value from 10 = 0� to 20 = 90� in x10 of millisecond
	softPwmWrite(Servo_Pin, pwmWidth);
#elif (SERVO_VERSION == SERVO_v2)
	if (degree < 0) degree = 0;
	if (degree > 90) degree = 90;
	int minR = 1052;
	int maxR = 2060;
	double pulse_us = minR + degree * (maxR - minR) / 90;
	double Width = pulse_us / 100;
	int intWidth = (int)Width;
	if (Width - intWidth >= 0.6) {
		int pwmWidth = intWidth + 1;
		softPwmWrite(Servo_Pin, pwmWidth);
	}
	else {
		int pwmWidth = intWidth;
		softPwmWrite(Servo_Pin, pwmWidth);
	}
#endif //SERVO_VERSION
}



//Sensors Reading Functions
#if (MODE == RELEASE)
#if (SENSORS_SPI_VERSION == SPIDEV)
static int InitializeSPI(const char* device, uint8_t mode, uint32_t speed) {
	int fd = open(device, O_RDWR);
	uint8_t mode = SPI_MODE_0;
	uint32_t speed = 1000000;

	if (fd < 0) return -1; // Failed to open device

	// Set SPI mode
	if (ioctl(fd, SPI_IOC_WR_MODE, &mode) == -1) { // Failed to set SPI mode
		close(fd);
		return -1;
	}

	// Set max speed
	if (ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) == -1) { // Failed to set max speed
		close(fd);
		return -1;
	}
	return fd;
}

static void TransferSPI(int fd, uint8_t * txBuf, uint8_t * rxBuf, size_t length) {
	struct spi_ioc_transfer trf = {
		.tx_buf = (unsigned long)txBuf,
		.rx_buf = (unsigned long)rxBuf,
		.len = length,
		.delay_usecs = 0,
		.speed_hz = 1000000,
		.bits_per_word = 8,
	};
	ioctl(fd, SPI_IOC_MESSAGE(1), &trf);
}


#elif (SENSORS_SPI_VERSION == WIRINGPISPI)
void ReadPressureSensors(uint32_t* Sensors) {
	uint8_t txBuf = CMD_READ; // Request data from channel 1
	uint8_t rxBuf[P_TxPACKET_LENGTH];
	uint8_t rxLatest[P_TxPACKET_LENGTH];

	digitalWrite(CS_PSB, HIGH);
	wiringPiSPIDataRW(SPI_PRESSURE, &txBuf, 1);
	wiringPiSPIDataRW(SPI_PRESSURE, rxBuf, P_TxPACKET_LENGTH);
	digitalWrite(CS_PSB, LOW);

	memcpy(rxLatest, rxBuf, P_TxPACKET_LENGTH);

	Sensors[0] = (rxBuf[0] << 8) | rxBuf[1];						//TPR280 Ambient Pressure
	Sensors[1] = (rxBuf[2] << 8) | rxBuf[3];						//PT5494 Accumulator Pressure
	Sensors[2] = (rxBuf[4] << 16) | (rxBuf[5] << 8) | rxBuf[6];		//P0 Chamber Pressure
	Sensors[3] = (rxBuf[7] << 16) | (rxBuf[8] << 8) | rxBuf[9];		//P1 Nozzle Throat Pressure
	Sensors[4] = (rxBuf[10] << 16) | (rxBuf[11] << 8) | rxBuf[12];	//P2 Nozzle Midspan Pressure
	Sensors[5] = (rxBuf[13] << 16) | (rxBuf[14] << 8) | rxBuf[15];	//P3 Nozzle Exit Pressure
	Sensors[6] = rxBuf[16];											//Flag
}

void ReadTemperatureSensors(uint32_t* Sensors) {
	uint8_t txBuf = CMD_READ; // Request data from channel 0
	uint8_t rxBuf[T_TxPACKET_LENGTH];
	uint8_t rxLatest[T_TxPACKET_LENGTH];

	digitalWrite(CS_TSB, HIGH);
	wiringPiSPIDataRW(SPI_TEMPERATURE, &txBuf, 1);
	wiringPiSPIDataRW(SPI_TEMPERATURE, rxBuf, T_TxPACKET_LENGTH);
	digitalWrite(CS_TSB, LOW);

	memcpy(rxLatest, rxBuf, T_TxPACKET_LENGTH);

	Sensors[0] = (rxBuf[0] << 16) | (rxBuf[1] << 8) | rxBuf[2];		//TPR280 Ambient Pressure
	Sensors[1] = (rxBuf[3] << 16) | (rxBuf[4] << 8) | rxBuf[5];		//PT5494 Accumulator Pressure
	Sensors[2] = (rxBuf[6] << 16) | (rxBuf[7] << 8) | rxBuf[8];		//P0 Chamber Pressure
	Sensors[3] = (rxBuf[9] << 16) | (rxBuf[10] << 8) | rxBuf[11];	//P1 Nozzle Throat Pressure
	Sensors[4] = (rxBuf[12] << 16) | (rxBuf[13] << 8) | rxBuf[14];	//P2 Nozzle Midspan Pressure
	Sensors[5] = (rxBuf[15] << 16) | (rxBuf[16] << 8) | rxBuf[17];	//P3 Nozzle Exit Pressure
	Sensors[6] = rxBuf[18];											//Flag
}
#endif //SENSORS_SPI_VERSION
#endif //MODE



//Fail-Safe Recovery Function
void FailSafeRecovery() { 
	DataFrame lastFrame = GetSaveFrame(-1); //Get the last DataFrame
	if (!FrameIsEmpty(lastFrame)) { //---------------------------------------------------------------------------FIX---------------------------------------------------------------------------------
		currentState = ReadFrame(lastFrame, Experiment_State);
		if (currentState >= VALVE_OPENED && currentState < SERVO_RUNNING) {
			if (ValveCompleted == 1) currentState = SERVO_RUNNING;
		}
		if (currentState >= SERVO_RUNNING && currentState < NOZZLE_OPENED) {
			if (ServoRunning == 1) currentState = NOZZLE_OPENED;
		}
		if (currentState >= NOZZLE_OPENED) {
			if (NozzleOpened == 1) currentState = END_OF_EXPERIMENT;
		}
	}
	else {
		currentState = WAIT_LO;
		ValveCompleted = 0;
		ServoRunning = 0;
		NozzleOpened = 0;
	}
}


//Mainboard CM5 Temperature and Voltage Status
#if (ONBOARD_OS == LINUX)
//TEMPERATURE
float temp_data(void) {
	FILE* fp = fopen("/sys/class/thermal/thermal_zone0/temp", "r");
	if (!fp) return -1;
	int temp_millideg;
	fscanf_s(fp, "%d", &temp_millideg);
	fclose(fp);
	return temp_millideg / 1000.0;
}
uint8_t temp_stat(float temp) {
	if (temp < 5.0) return 1;		//cold
	else if (temp < 30.0) return 2;	//normal
	else if (temp < 55.0) return 3;	//warm
	else return 4;					//hot
}

//VOLTAGE
uint8_t volt_stat(void) {
	FILE* fp = popen("vcgencmd get_throttled", "r");
	if (!fp) return -1;

	char output[64];
	if (!fgets(output, sizeof(output), fp)) {pclose(fp); return 1;}
	pclose(fp);

	unsigned int volt = 0;
	sscanf_s(output, "throttled=0x%x", &volt);

	if (volt & 0x1) return 0;			//low
	else if (volt & 0x10000) return 0;	//low
	else return 1;						//normal
}

uint8_t mainboardStatus(uint8_t tempStat, uint8_t voltStat) {
	uint8_t Temp = (tempStat - 1) & 0x03;	//2 bits
	uint8_t Volt = (voltStat == 1) ? 1:0;	//1 bit
	return (Volt << 3) | Temp;
}
#endif