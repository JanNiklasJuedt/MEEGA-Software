from ctypes import *
from enum import IntEnum

DataHandling = cdll.LoadLibrary("..\\x64\\Debug\\DataHandlingLibrary.dll")

print("DLL " + DataHandling._name + " successfully loaded")

PATH_LENGTH = c_int.in_dll(DataHandling, "PathLength").value
DATA_LENGTH = c_int.in_dll(DataHandling, "DataLength").value

class DataFrame(Structure):
    _fields_ = [("start", c_ubyte), ("flag", c_ubyte), ("sync", c_uint16), ("data", c_ubyte * DATA_LENGTH), ("chksm", c_uint16) ]

class CalibrationPoint(Structure):
    _fields_ = [ ("digital", c_int64), ("analog", c_float), ("valid", c_byte)]

class c_enum(IntEnum):
    def __init__(self, value):
        self._as_parameter_ = int(value)
    @classmethod
    def from_param(cls, obj):
        return int(obj)

class TMID(c_enum):
    #Sensors:
    Ambient_Pressure = 0
    Compare_Temperature = 1
    Tank_Pressure = 2
    Tank_Temperature = 3
    Chamber_Pressure = 4
    Chamber_Temperature_1 = 5
    Chamber_Temperature_2 = 6
    Nozzle_Pressure_1 = 7
    Nozzle_Temperature_1 = 8
    Nozzle_Pressure_2 = 9
    Nozzle_Temperature_2 = 10
    Nozzle_Pressure_3 = 11
    Nozzle_Temperature_3 = 12
	#Householding Sensors:
    Ambient_Pressure_Health = 13
    Compare_Temperature_Health = 14
    Tank_Pressure_Health = 15
    Tank_Temperature_Health = 16
    Chamber_Pressure_Health = 17
    Chamber_Temperature_1_Health = 18
    Chamber_Temperature_2_Health = 19
    Nozzle_Pressure_1_Health = 20
    Nozzle_Temperature_1_Health = 21
    Nozzle_Pressure_2_Health = 22
    Nozzle_Temperature_2_Health = 23
    Nozzle_Pressure_3_Health = 24
    Nozzle_Temperature_3_Health = 25
    #Householding Misc:
    Nozzle_Open = 26
    Nozzle_Closed = 27
    Nozzle_Servo = 28
    Reservoir_Valve = 29
    Camera = 30
    LEDs = 31
    Sensorboard_P = 32
    Sensorboard_T = 33
    Mainboard = 34
    Mainboard_T = 35
    Mainboard_V = 36
    System_Time = 37
    Lift_Off = 38
    Start_Experiment = 39
    End_Experiment = 40
    Mode = 41
    Experiment_State = 42

class TCID(c_enum):
    Mode_Change = 0
    Valve_Delay = 1
    Servo_Delay = 2
    EoE_Delay = 3
    Power_Off_Delay = 4
    Nozzle_On_Delay = 5
    Dry_Run = 6
    LED_Control = 7
    Servo_Control = 8
    Valve_Control = 9
    Camera_Control = 10
    Test_Abort = 11
    Test_Run = 12

class Flag(c_enum):
    Source = 0
    OK = 1
    Biterror = 2
    Partial = 3
    TeleMetry = 4
    TeleCommand = 5

DataHandling.DebugLog.argtypes = [c_char_p]

DataHandling.MapSensorValue.argtypes = [c_int, c_int64]
DataHandling.MapSensorValue.restype = c_float

DataHandling.Initalize.argtypes = [c_char_p, c_char_p, c_char_p, c_byte, c_byte]

DataHandling.AddPoint.argtypes = [c_int, c_int, CalibrationPoint]

DataHandling.ReadPoint.argtypes = [c_int, c_int]
DataHandling.ReadPoint.restype = CalibrationPoint

DataHandling.WritePoint.argtypes = [c_int, c_int, c_int64, c_float]

DataHandling.ReadCalibration.argtypes = [c_char_p]

DataHandling.CreateCalibration.argtypes = [c_char_p]

DataHandling.CreateFrame.restype = DataFrame

DataHandling.CreateTC.restype = DataFrame

DataHandling.WriteFrame.argtypes = [POINTER(DataFrame), c_int, c_int64]
DataHandling.WriteFrame.restype = c_int64

DataHandling.ReadFrame.argtypes = [DataFrame, c_int]
DataHandling.ReadFrame.restype = c_int64

DataHandling.FrameIsEmpty.argtypes = [DataFrame]

DataHandling.FrameIsTC.argtypes = [DataFrame]

DataHandling.FrameHasFlag.argtypes = [DataFrame, Flag]

DataHandling.FrameSetFlag.argtypes = [POINTER(DataFrame), Flag]

DataHandling.AddOutFrame.argtypes = [DataFrame]

DataHandling.CreateSave.argtypes = [c_char_p]

DataHandling.ReadSave.argtypes = [c_char_p]

DataHandling.GetSaveFrame.argtypes = [c_int]
DataHandling.GetSaveFrame.restype = DataFrame

DataHandling.GetNextFrame.restype = DataFrame

DataHandling.GetTC.restype = DataFrame

DataHandling.AddSaveFrame.argtypes = [DataFrame]

DataHandling.AddFrame.argtypes = [DataFrame]

DataHandling.SetPort.argtypes = [c_char_p]