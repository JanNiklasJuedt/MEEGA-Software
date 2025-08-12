from ctypes import *

DataHandling = cdll.LoadLibrary("..\\x64\\Debug\\DataHandlingLibrary.dll")

print("DLL " + DataHandling._name + " successfully loaded")

PATHLENGTH = c_int.in_dll(DataHandling, "PathLength").value
BUFFERLENGTH = c_int.in_dll(DataHandling, "BufferLength").value
DATALENGTH = c_int.in_dll(DataHandling, "DataLength").value
PAYLOADLENGTH = c_int.in_dll(DataHandling, "PayloadLength").value
CHKSMLENGTH = c_int.in_dll(DataHandling, "ChksmLength").value

class DataFrame(Structure):
    _fields_ = [ ("sync", c_int16), ("flag", c_ubyte), ("data", c_ubyte * DATALENGTH) ]

class DataPacket(Structure):
    _fields_ = [ ("sync", c_int16), ("mode", c_ubyte), ("id", c_ubyte), ("payload", c_ubyte * PAYLOADLENGTH), ("chksm", c_ubyte * CHKSMLENGTH), ("crc", c_ubyte * CHKSMLENGTH) ]

class DataBuffer(Structure):
    _fields_ = [ ("incoming", DataPacket * BUFFERLENGTH), ("outgoing", DataPacket * BUFFERLENGTH), ("frameStack", DataFrame * BUFFERLENGTH), ("TCStack", DataFrame * BUFFERLENGTH) ]

class FailSafe(Structure):
    _fields_ = [ ("version", c_ubyte), ("dateTime", c_time_t), ("saveFilePath", c_wchar_p), ("complete", c_byte), ("nominalExit", c_byte), ("mode", c_char), ("conn", c_char), ("lang", c_char) ]

class SaveFileFrame(Structure):
    pass

SaveFileFrame._fields_ = [ ("data", DataFrame), ("nextFrame", POINTER(SaveFileFrame)), ("previousFrame", POINTER(SaveFileFrame)) ]

class SaveFile(Structure):
    _fields_ = [ ("version", c_ubyte), ("dateTime", c_time_t), ("firstFrame", POINTER(SaveFileFrame)), ("lastFrame", POINTER(SaveFileFrame)), ("frameAmount", c_int), ("savedAmount", c_int), ("currentTC", POINTER(DataFrame)), ("saveFilePath", c_wchar_p) ]

class StorageHub(Structure):
    _fields_ = [ ("saveFile", POINTER(SaveFile)), ("failSafe", POINTER(FailSafe)), ("buffer", POINTER(DataBuffer)) ]

DataHandling.Update.argtypes = [POINTER(StorageHub)]

DataHandling.Initialize.argtypes = [c_wchar_p]
DataHandling.Initialize.restype = StorageHub

DataHandling.CreateFrame.argtypes = [c_int16]
DataHandling.CreateFrame.restype = DataFrame

DataHandling.CreateTC.argtypes = [c_int16]
DataHandling.CreateTC.restype = DataFrame

DataHandling.WriteFrame.argtypes = [POINTER(DataFrame), c_int, c_int]

DataHandling.WriteTC.argtypes = [POINTER(DataFrame), c_int, c_int]

DataHandling.ReadFrame.argtypes = [POINTER(DataFrame), c_int]

DataHandling.ReadTC = [POINTER(DataFrame), c_int]

DataHandling.FrameIsEmpty.argtypes = [POINTER(DataFrame)]

DataHandling.FrameIsTC.argtypes = [POINTER(DataFrame)]

DataHandling.WritePacket.argtypes = [DataPacket]
DataHandling.WritePacket.restype = POINTER(c_ubyte)

DataHandling.ReadPacket.argtypes = [POINTER(c_ubyte)]
DataHandling.ReadPacket.restype = DataPacket

DataHandling.FormPackets.argtypes = [POINTER(DataBuffer)]

DataHandling.FormFrames.argtypes = [POINTER(DataBuffer)]

DataHandling.GetOutPacket.argtypes = [POINTER(DataBuffer)]
DataHandling.GetOutPacket.restype = DataPacket

DataHandling.GetInPacket.argtypes = [POINTER(DataBuffer)]
DataHandling.GetInPacket.restype = DataPacket

DataHandling.GetBufferFrame.argtypes = [POINTER(DataBuffer)]
DataHandling.GetBufferFrame.restype = DataFrame

DataHandling.GetBufferTC.argtypes = [POINTER(DataBuffer)]
DataHandling.GetBufferTC.restype = DataFrame

DataHandling.AddBufferFrame.argtypes = [POINTER(DataBuffer), DataFrame]

DataHandling.AddBufferTC.argtypes = [POINTER(DataBuffer), DataFrame]

DataHandling.AddInPacket.argtypes = [POINTER(DataBuffer), DataPacket]

DataHandling.AddOutPacket.argtypes = [POINTER(DataBuffer), DataPacket]

DataHandling.CreateBuffer.restype = POINTER(DataBuffer)

DataHandling.CreateFailSafe.restype = POINTER(FailSafe)

DataHandling.ReadFailSafe.restype = POINTER(FailSafe)

DataHandling.UpdateFailSafe.argtypes = [POINTER(FailSafe)]

DataHandling.WriteSave.argtypes = [POINTER(SaveFile)]

DataHandling.CreateSave.argtypes = [c_wchar_p]
DataHandling.CreateSave.restype = POINTER(SaveFile)

DataHandling.VirtualSave.restype = POINTER(SaveFile)

DataHandling.ReadSave.argtypes = [c_wchar_p]
DataHandling.ReadSave.restype = POINTER(SaveFile)

DataHandling.GetSaveFrame.argtypes = [POINTER(SaveFile), c_int]
DataHandling.GetSaveFrame.restype = POINTER(SaveFileFrame)

DataHandling.UpdateTC.argtypes = [POINTER(SaveFile)]
DataHandling.UpdateTC.restype = POINTER(DataFrame)

DataHandling.AddSaveFrame.argtypes = [POINTER(SaveFile), DataFrame]
DataHandling.AddSaveFrame.restype = POINTER(SaveFileFrame)

DataHandling.CreateSaveFrame.argtypes = [POINTER(SaveFile), c_int16]
DataHandling.CreateSaveFrame.restype = POINTER(SaveFileFrame)
