from ctypes import *

DataHandling = cdll.LoadLibrary("..\\x64\\Debug\\DataHandlingLibrary.dll")

print("DLL " + DataHandling._name + " successfully loaded")

PATH_LENGTH = c_int.in_dll(DataHandling, "PathLength").value
DATA_LENGTH = c_int.in_dll(DataHandling, "DataLength").value
CHKSM_LENGTH = c_int.in_dll(DataHandling, "ChksmLength").value

class DataFrame(Structure):
    _fields_ = [ ("sync", c_int16), ("flag", c_ubyte), ("data", c_ubyte * DATA_LENGTH), ("chksm", c_ubyte * CHKSM_LENGTH) ]

class SaveFileFrame(Structure):
    pass

SaveFileFrame._fields_ = [ ("data", DataFrame), ("nextFrame", POINTER(SaveFileFrame)), ("previousFrame", POINTER(SaveFileFrame)) ]

class CalibrationPoint(Structure):
    _fields_ = [ ("digital", c_int), ("analog", c_float), ("valid", c_byte)]

DataHandling.DebugLog.argtypes = [c_char_p]

DataHandling.MapSensorValue.argtypes = [c_int, c_int]
DataHandling.MapSensorValue.restype = c_float

DataHandling.AddPoint.argtypes = [c_int, c_int, CalibrationPoint]

DataHandling.ReadPoint.argtypes = [c_int, c_int]
DataHandling.ReadPoint.restype = CalibrationPoint

DataHandling.ReadCalibration.argtypes = [c_char_p]

DataHandling.CreateCalibration.argtypes = [c_char_p]

DataHandling.Initialize.argtypes = [c_char_p]

DataHandling.CreateFrame.argtypes = [c_uint16]
DataHandling.CreateFrame.restype = DataFrame

DataHandling.CreateTC.argtypes = [c_uint16]
DataHandling.CreateTC.restype = DataFrame

DataHandling.EmptyFrame.argtypes = [c_uint16]

DataHandling.EmptyTC.argtypes = [c_uint16]

DataHandling.WriteFrame.argtypes = [POINTER(DataFrame), c_int, c_int]

DataHandling.ReadFrame.argtypes = [DataFrame, c_int]

DataHandling.FrameIsEmpty.argtypes = [DataFrame]

DataHandling.FrameIsTC.argtypes = [DataFrame]

DataHandling.FrameHasFlag.argtypes = [DataFrame, c_int]

DataHandling.FrameAddFlag.argtypes = [POINTER(DataFrame), c_int]

DataHandling.AddOutFrame.argtypes = [DataFrame]

DataHandling.CreateSave.argtypes = [c_char_p]

DataHandling.ReadSave.argtypes = [c_char_p]

DataHandling.GetSaveFrame.argtypes = [c_int]
DataHandling.GetSaveFrame.restype = POINTER(SaveFileFrame)

DataHandling.UpdateTC.restype = DataFrame

DataHandling.AddSaveFrame.argtypes = [DataFrame]
DataHandling.AddSaveFrame.restype = POINTER(SaveFileFrame)

DataHandling.CreateSaveFrame.argtypes = [c_uint16]
DataHandling.CreateSaveFrame.restype = POINTER(SaveFileFrame)

DataHandling.AddFrame.argtypes = [DataFrame]