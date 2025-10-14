#imports
from __future__ import annotations
from math import floor
import sys
import time
from tkinter import SE, SEL

from PySide6.QtGui import (QAction, QActionGroup, QIcon, QImage, QPixmap,)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QMainWindow, QDialog, QWidget)
from PySide6.QtCore import (Signal, Slot, QTranslator, QLocale, QThread)

from MEEGA_mainWindow import *
from MEEGA_calibration import *
from MEEGA_startup import *
from MEEGA_Connection import *
from MEEGA_time import *
from MEEGA_documentation import *
from MEEGA_error import *
from MEEGA_controlPanel import *
from MEEGA_results import *
from MEEGA_calibration import *

from MEEGA_PyDataHandling import *

#class to handle program settings
class Settings:
    AUTOMATIC = 0
    MANUAL = 1
    FLIGHT = 0
    TEST = 1
    defaultFilePath = "Default.meega"
    defaultLaunchTime = QTime(12,0,0)
    def __init__(self, locale: QLocale = None, mode: int = TEST, connectionMode: int = AUTOMATIC, filePath: str = defaultFilePath, launchTime: QTime = defaultLaunchTime):
        if locale == None:
            self.locale = QLocale()
        else:
            self.locale = QLocale(locale)
        self.mode = mode
        self.connectionMode = connectionMode
        self.filePath = filePath
        self.launchTime = launchTime

#class to handle telecommands
class Telecommand:
    def __init__(self):
        self.tcframe = DataHandling.CreateTC()
        self.sendCounter = 0

    def newTCFrame(self):
        self.tcframe = DataHandling.CreateTC()
        DataHandling.WriteFrame(self.tcframe, 0, self.collection.settings.mode)

    def sendInit(self):
        self.sendCounter = 10

    def sendStep(self):
        if self.sendCounter > 0:
            DataHandling.AddFrame(self.tcframe)
            self.sendCounter -= 1

#class to define the Main Window
class GSMain(QMainWindow):
    def __init__(self, collection: Collection):
        super().__init__()

        #importing visuals from the ui-file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #creating variables
        self.ACTIVE = 0
        self.ISSUES = 1
        self.INACTIVE = 2
        self.collection = collection

        #creating local status list
        self.status = [[self.ACTIVE, ""] for _ in range(20)]
        self.status[0][1] = self.ui.statusLabelPAmbient
        self.status[1][1] = self.ui.statusLabelTCompare
        self.status[2][1] = self.ui.statusLabelPReservoir
        self.status[3][1] = self.ui.statusLabelTReservoir
        self.status[4][1] = self.ui.statusLabelPAccumulator
        self.status[5][1] = self.ui.statusLabelTAccumulator
        self.status[6][1] = self.ui.statusLabelPNozzle1
        self.status[7][1] = self.ui.statusLabelTNozzle1
        self.status[8][1] = self.ui.statusLabelPNozzle2
        self.status[9][1] = self.ui.statusLabelTNozzle2
        self.status[10][1] = self.ui.statusLabelPNozzle3
        self.status[11][1] = self.ui.statusLabelTNozzle3
        self.status[12][1] = self.ui.statusLabelServo
        self.status[13][1] = self.ui.statusLabelValve
        self.status[14][1] = self.ui.statusLabelLED
        self.status[15][1] = self.ui.statusLabelPChip
        self.status[16][1] = self.ui.statusLabelTChip
        self.status[17][1] = self.ui.statusLabelMainboard
        self.status[18][1] = self.ui.statusLabelLiftOff
        self.status[19][1] = self.ui.statusLabelSOE

        #creating status pixmaps
        self.activepix = QPixmap("Ressources\\active.png")
        self.issuespix = QPixmap("Ressources\\issues.png")
        self.inactivepix = QPixmap("Ressources\\inactive.png")

        self.scalePixmaps()        
        self.fetchStatus()

        self.setLocale(self.collection.settings.locale)

        #creating the big logo
        self.logo = QPixmap("Ressources\\meega_logo_small.png")
        self.ui.label_logo.setPixmap(self.logo)

        #creating menubar actiongroups (for exclusivity of selected options)
        self.languageGroup = QActionGroup(self.ui.menuLanguage)
        self.languageGroup.setExclusive(True)
        for i in self.ui.menuLanguage.actions():
            self.languageGroup.addAction(i)
        self.modeGroup = QActionGroup(self.ui.menuStart)
        self.modeGroup.setExclusive(True)
        self.modeGroup.addAction(self.ui.actionFlight_Mode)
        self.modeGroup.addAction(self.ui.actionTest_Mode)
        self.connectionModeGroup = QActionGroup(self.ui.menuConnection)
        self.connectionModeGroup.addAction(self.ui.actionAutomatic)
        self.connectionModeGroup.addAction(self.ui.actionManual)
        
        #reference to the application object
        self.app = QApplication.instance()
        
        #connection of signals and slots
        self.languageGroup.triggered.connect(self.languageChanges)
        self.ui.actionManual.triggered.connect(self.fetchSettings)
        self.ui.actionAutomatic.triggered.connect(self.fetchSettings)
        self.ui.actionFlight_Mode.triggered.connect(self.modeSwitched)
        self.ui.actionTest_Mode.triggered.connect(self.modeSwitched)
        self.ui.actionQuit.triggered.connect(self.app.quit) 

    #internal functions
    def scalePixmaps(self):
            #Pixmaps an die aktuelle Label-Groesse anpassen
            label_size = self.ui.statusLabelMainboard.size()
            circle_diameter = min(label_size.width(), label_size.height())
            self.activepix_scaled = self.activepix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.issuespix_scaled = self.issuespix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.inactivepix_scaled = self.inactivepix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    def resizeEvent(self, event):
            self.scalePixmaps()
            super().resizeEvent(event)
    def retranslateUi(self):
        self.ui.retranslateUi()
    def languageChanges(self):
        translator = QTranslator()
        locale = self.collection.settings.locale
        language = QLocale.languageToCode(locale.language())
        for i in self.languageGroup.actions():
            if i.property("data") == language:
                i.setChecked(True)
        #Baustelle:
        if translator.load(locale, "MEEGA_Language"):
            self.app.removeTranslator(translator)
            self.app.installTranslator(translator)
            self.retranslateUi(self)
    def connectionModeChanges(self):
        if self.collection.settings.connectionMode == Settings.AUTOMATIC:
            self.ui.actionConnect.setEnabled(False)
            self.ui.actionRetry.setEnabled(False)
            self.ui.actionDisconnect.setEnabled(False)
        else:
            self.ui.actionConnect.setEnabled(True)
            self.ui.actionRetry.setEnabled(True)
            self.ui.actionDisconnect.setEnabled(True)
            self.ui.menuSetup.popup(self.ui.menuSetup.pos())
            self.ui.menuConnection.popup(self.ui.menuConnection.pos())
    def filePathChanges(self):
        pass
    def fetchStatus(self):
        #update the local status list from DataHandling
        frame = DataHandling.GetSaveFrame(-1)
        #if not DataHandling.FrameIsEmpty(frame):
        if not bool(frame) == False:
            frame = frame.contents.data
            for i in range(12):
                self.status[i][0] = DataHandling.ReadFrame(frame, 12+i)
            self.status[12][0] = DataHandling.ReadFrame(frame, 26)
            self.status[13][0] = DataHandling.ReadFrame(frame, 27)
            self.status[14][0] = DataHandling.ReadFrame(frame, 29)
            self.status[15][0] = DataHandling.ReadFrame(frame, 30)
            self.status[16][0] = DataHandling.ReadFrame(frame, 31)
            self.status[17][0] = DataHandling.ReadFrame(frame, 32)
            self.status[18][0] = DataHandling.ReadFrame(frame, 34)
            self.status[19][0] = DataHandling.ReadFrame(frame, 35)
        #update the displayed status pixmaps
        for i in range(20):
            match self.status[i][0]:
                case self.ACTIVE:
                    self.status[i][1].setPixmap(self.activepix_scaled)
                case self.ISSUES:
                    self.status[i][1].setPixmap(self.issuespix_scaled)
                case self.INACTIVE:
                    self.status[i][1].setPixmap(self.inactivepix_scaled)
    
    #external functions (slots)
    @Slot()
    def modeSwitched(self):
        if self.modeGroup.checkedAction() == self.ui.actionFlight_Mode:
            self.collection.settings.mode = Settings.FLIGHT
            self.ui.label_mode.setText("Flight Mode")
            self.ui.actionControl_Panel.setEnabled(False)
            self.collection.controlPanel.clearPanel()
            self.collection.controlPanel.hide()
        else:
            self.collection.settings.mode = Settings.TEST
            self.ui.label_mode.setText("Test Mode")
            self.ui.actionControl_Panel.setEnabled(True)
        self.collection.telecommand.newTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def fetchSettings(self):
        if self.connectionModeGroup.checkedAction() == self.ui.actionAutomatic:
            connectionMode = Settings.AUTOMATIC
        else:
            connectionMode = Settings.MANUAL
        self.settings.connectionMode = connectionMode
        self.connectionModeChanges()
    @Slot()
    def applySettings(self):
        if self.collection.settings.connectionMode == Settings.AUTOMATIC:
            self.ui.actionAutomatic.setChecked(True)
        else:
            self.ui.actionManual.setChecked(True)
        if self.collection.settings.mode == Settings.FLIGHT:
            self.ui.actionFlight_Mode.setChecked(True)
        else:
            self.ui.actionTest_Mode.setChecked(True)
        self.setLocale(self.collection.settings.locale)
        self.languageChanges()
        self.modeChanges()
        self.connectionModeChanges()
        self.filePathChanges()

#class to define the startup dialog window
class GSStart(QDialog):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
        self.collection = collection
        self.ui.languageComboBox.setItemData(0, "en")
        self.ui.languageComboBox.setItemData(1, "de")
        self.ui.connectionComboBox.setItemData(0,Settings.AUTOMATIC)
        self.ui.connectionComboBox.setItemData(1,Settings.MANUAL)
        self.ui.modeComboBox.setItemData(0, Settings.TEST)
        self.ui.modeComboBox.setItemData(1, Settings.FLIGHT)

        self.rejected.connect(QApplication.instance().quit)
        self.accepted.connect(self.fetchSettings)

    @Slot()
    def fetchSettings(self):
        self.collection.settings.language = self.ui.languageComboBox.currentData()
        self.collection.settings.connectionMode = self.ui.connectionComboBox.currentData()
        self.collection.settings.mode = self.ui.modeComboBox.currentData()
        self.collection.settings.filepath = self.ui.saveFileEdit.text()
        self.collection.settings.launchTime = self.ui.launchTimeTimeEdit.time()

class GSLaunchTime(QDialog):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_LaunchTimeDialog()
        self.ui.setupUi(self)
        self.collection = collection

        self.accepted.connect(self.fetchSettings)
    
    @Slot()
    def fetchSettings(self):
        self.collection.settings.launchTime = self.ui.launchTimeEdit.time()

class GSResults(QWidget):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_ResultsWidget()
        self.ui.setupUi(self)
        self.collection = collection

        self.ui.buttonBox.clicked.connect(self.hide)

class GSDocumentation(QWidget):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_Documentation()
        self.ui.setupUi(self)
        self.collection = collection

class GSError(QDialog):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self)
        self.collection = collection

 ###Baustelle:
        
        #Hook, wenn sich ein knopf �ndert
        # Kn�pfe per enable ausschalten
  
class GSControl(QWidget):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_controlPanel()
        self.ui.setupUi(self)
        self.collection = collection

        # Initialize control states
        self.valveControl = 0  # closed
        self.ledState = 0      # False (Off)
        self.servoAngle = 0 # in 1/10 °
        self.dryRunActive = 0
        self.testRunStart = 0
        self.testRunStop = 0
        # Initialize duration values
        self.valveDelay = QTime(0, 0, 0)
        self.servoDelay = QTime(0, 0, 0)
        self.EOEDelay = QTime(0, 0, 0)
        # Connect signals to slots
        self.connectSignals()
        
    def connectSignals(self):
        # Valve controls
        self.ui.openValveButton.clicked.connect(self.openValve)
        self.ui.closeValveButton.clicked.connect(self.closeValve)
        # Servo controls
        self.ui.setServoButton.clicked.connect(self.setServoAngle)
        # LED controls
        self.ui.ledOnButton.clicked.connect(self.onLED)
        self.ui.ledOffButton.clicked.connect(self.offLED)
        # Test run controls
        self.ui.startTestButton.clicked.connect(self.startTest)
        self.ui.stopTestButton.clicked.connect(self.stopTest)
        # Dry run control
        self.ui.dryRunOnButton.clicked.connect(self.dryRunSwitch)
        # Reset buttons
        self.ui.valveResetButton.clicked.connect(self.resetValveDelay)
        self.ui.servoResetButton.clicked.connect(self.resetServoDelay)
        self.ui.EOEResetButton.clicked.connect(self.resetEOEDelay)
    
    # external functions for ui controls
    # Valve control slots
    @Slot()
    def openValve(self):
        self.valveControl = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def closeValve(self):
        self.valveControl = 0
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # Servo control slot
    @Slot()
    def setServoAngle(self):
        self.servoAngle = self.ui.servoValueBox.value()
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # LED control slots
    @Slot()
    def onLED(self):
        self.ledState = 0
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def offLED(self):
        self.ledState = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # Test run control slots
    @Slot()
    def startTest(self):
        self.setDelays()
        self.testRunStart = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
        self.testRunStart = 0
    @Slot()
    def stopTest(self):
        self.testRunStop = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
        self.testRunStop = 0
    # Dry run control slot
    @Slot()
    def dryRunSwitch(self):
        if self.ui.dryRunOnButton.isChecked():
            self.dryRunActive = 1
        else:
            self.dryRunActive = 0
    # Reset duration slots
    @Slot()
    def resetValveDelay(self):
        self.ui.valveTimeEdit.setTime(QTime(0, 0, 0))
        self.ui.valveMilliEdit.setText("000")
        self.valveDelay = QTime(0, 0, 0)
    @Slot()
    def resetServoDelay(self):
        self.ui.servoTimeEdit.setTime(QTime(0, 0, 0))
        self.ui.servoMilliEdit.setText("000")
        self.servoDelay = QTime(0, 0, 0)
    @Slot()
    def resetEOEDelay(self):
        self.ui.EOETimeEdit.setTime(QTime(0, 0, 0))
        self.ui.EOEMilliEdit.setText("000")
        self.EOEDelay = QTime(0, 0, 0)

    # internal functions
    # Duration changes
    def setDelays(self):
        self.valveDelay = self.ui.valveTimeEdit.time().addMSecs(int(self.ui.valveMilliEdit.text()))
        self.servoDelay = self.ui.servoTimeEdit.time().addMSecs(int(self.ui.servoMilliEdit.text()))
        self.EOEDelay = self.ui.EOETimeEdit.time().addMSecs(int(self.ui.EOEMilliEdit.text()))
    # Update the telecommand frame with current control states and durations
    def updateTCFrame(self):
        DataHandling.WriteFrame(self.collection.tcframe, 1, (self.valveDelay.minute()*60 + self.valveDelay.second())*1000 + self.valveDelay.msec())
        DataHandling.WriteFrame(self.collection.tcframe, 2, (self.servoDelay.minute()*60 + self.servoDelay.second())*1000 + self.servoDelay.msec())
        DataHandling.WriteFrame(self.collection.tcframe, 3, (self.EOEDelay.minute()*60 + self.EOEDelay.second())*1000 + self.EOEDelay.msec())
        #PowerOffDelay fehlt
        #NozzleOnDelay fehlt
        DataHandling.WriteFrame(self.collection.tcframe, 6, self.dryRunActive)
        DataHandling.WriteFrame(self.collection.tcframe, 7, self.ledState)
        DataHandling.WriteFrame(self.collection.tcframe, 8, floor(self.servoAngle*10))
        DataHandling.WriteFrame(self.collection.tcframe, 9, self.valveControl)
        #Camera control fehlt
        DataHandling.WriteFrame(self.collection.tcframe, 11, self.testRunStop)
        DataHandling.WriteFrame(self.collection.tcframe, 12, self.testRunStart)
    def clearPanel(self):
        self.valveControl = 0
        self.ledState = 0
        self.servoAngle = 0
        self.ui.servoValueBox.setValue(0)
        self.dryRunActive = 0
        self.ui.dryRunOnButton.setChecked(False)
        self.testRunStart = 0
        self.testRunStop = 0
        self.resetValveDelay()
        self.resetServoDelay()
        self.resetEOEDelay()

class GSConnection(QDialog):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)
        self.collection = collection

class GSCalibration(QDialog):
    def __init__(self, collection: Collection):
        super().__init__()
        self.ui = Ui_Sensor_Calibration()
        self.ui.setupUi(self)
        self.collection = collection

        #initialize variables
        self.selectedSensor = 0
        self.selectedEntry = 0
        self.currentUnit = ""
        self.calibrationPoints = [[0] * 3 for x in range(12)]

        #create exclusive button group for radio buttons and add automatic disabling/enabling of lineEdits
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.ui.radioButton)
        self.buttonGroup.addButton(self.ui.radioButton_2)
        self.buttonGroup.addButton(self.ui.radioButton_3)
        self.buttonGroup.setExclusive(True)
        self.ui.radioButton.clicked.connect(self.selectEntry)
        self.ui.radioButton_2.clicked.connect(self.selectEntry)
        self.ui.radioButton_3.clicked.connect(self.selectEntry)
        self.ui.radioButton.click()

        self.selectSensor()
        self.ui.comboBox.currentIndexChanged.connect(self.selectSensor)
        self.ui.pushButton.clicked.connect(self.newCalibrationPoint)
    

    #update the displayed sensor value
    def updateValue(self):
        frame = DataHandling.GetSaveFrame(-1)
        if not bool(frame) == False:
            frame = frame.contents.data
            digitalValue = DataHandling.ReadFrame(frame, self.selectedSensor)
            mappedValue = str(DataHandling.MapSensorValue(self.selectedSensor, digitalValue))
            self.ui.label.setText(mappedValue + " " + self.currentUnit)
    
    #select sensor and display already existing calibration points, according Units
    @Slot()
    def selectSensor(self):
        self.selectedSensor = self.ui.comboBox.currentIndex()
        self.ui.lineEdit.setText(str(self.calibrationPoints[self.selectedSensor][0]))
        self.ui.lineEdit_2.setText(str(self.calibrationPoints[self.selectedSensor][1]))
        self.ui.lineEdit_3.setText(str(self.calibrationPoints[self.selectedSensor][2]))
        if self.selectedSensor in [0,2,4,6,8,10]:
            self.currentUnit = "Pa"
        else:
            self.currentUnit = "K"
        self.ui.label_2.setText(self.currentUnit)
        self.ui.label_3.setText(self.currentUnit)
        self.ui.label_4.setText(self.currentUnit)

    #enable lineEdit corresponding to selected radioButton, disable the others
    @Slot()
    def selectEntry(self):
        match self.buttonGroup.checkedButton():
            case self.ui.radioButton:
                self.ui.lineEdit.setEnabled(True)
                self.ui.lineEdit_2.setDisabled(True)
                self.ui.lineEdit_3.setDisabled(True)
                self.selectedEntry = 0
            case self.ui.radioButton_2:
                self.ui.lineEdit.setDisabled(True)
                self.ui.lineEdit_2.setEnabled(True)
                self.ui.lineEdit_3.setDisabled(True)
                self.selectedEntry = 1
            case self.ui.radioButton_3:
                self.ui.lineEdit.setDisabled(True)
                self.ui.lineEdit_2.setDisabled(True)
                self.ui.lineEdit_3.setEnabled(True)
                self.selectedEntry = 2
    
    #save the currently selected calibration point
    @Slot()
    def newCalibrationPoint(self):
        currentEntry = ""
        match self.selectedEntry:
            case 0:
                currentEntry = self.ui.lineEdit.text()
            case 1:
                currentEntry = self.ui.lineEdit_2.text()
            case 2:
                currentEntry = self.ui.lineEdit_3.text()
        frame = DataHandling.GetSaveFrame(-1)
        if not bool(frame) == False:
            frame = frame.contents.data
            digitalValue = DataHandling.ReadFrame(frame, self.selectedSensor)
            DataHandling.writePoint(self.selectedSensor, self.selectedEntry, digitalValue, currentEntry)
        self.calibrationPoints[self.selectedSensor][self.selectedEntry] = float(currentEntry)

class DataHandlingThread(QThread):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
    def run(self):
        period_ms = 1000 / 20
        while True:
            clock = time.monotonic_ns()
            self.collection.mainWindow.fetchStatus()
            self.collection.calibrationWindow.updateValue()
            self.collection.telecommand.sendStep()
            DataHandling.UpdateAll()
            if self.isInterruptionRequested():
               break
            self.msleep(period_ms - (time.monotonic_ns() - clock) / 1000000)

class Collection:
    def __init__(self):
        self.settings = Settings()
        self.telecommand = Telecommand()
        self.mainWindow = GSMain(self)
        self.startWindow = GSStart(self)
        self.controlPanel = GSControl(self)
        self.timeWindow = GSLaunchTime(self)
        self.documentationWindow = GSDocumentation(self)
        self.errorWindow = GSError(self)
        self.resultsWindow = GSResults(self)
        self.connectionWindow = GSConnection(self)
        self.calibrationWindow = GSCalibration(self)
    
    def interWindowConnection(self):
        self.mainWindow.ui.actionRestart.triggered.connect(self.startWindow.show)
        self.mainWindow.ui.actionRestart.triggered.connect(self.mainWindow.hide)
        self.mainWindow.ui.actionControl_Panel.triggered.connect(self.controlPanel.show)
        self.mainWindow.ui.actionDocumentation.triggered.connect(self.documentationWindow.show)
        self.mainWindow.ui.actionConnect.triggered.connect(self.connectionWindow.show)
        self.mainWindow.ui.actionResults.triggered.connect(self.resultsWindow.show)
        self.mainWindow.ui.actionEstimated_Launch_Time.triggered.connect(self.timeWindow.show)
        self.startWindow.accepted.connect(self.mainWindow.applySettings)
        self.startWindow.accepted.connect(self.mainWindow.show)
        self.timeWindow.accepted.connect(self.mainWindow.applySettings)
        self.mainWindow.ui.actionCalibration.triggered.connect(self.calibrationWindow.show)

#Main
if __name__ == "__main__":
    GS = QApplication()
    icon = QIcon("Ressources\\meega_logo_small.ico")
    GS.setWindowIcon(icon)
    translator = QTranslator()
    QLocale.setDefault(QLocale.C)
    collection = Collection()

    #Hier Datahandling (Data Storage Variable)

    if translator.load(collection.settings.locale, "MEEGA_Language"):
        GS.installTranslator(translator)

    #DataHandling setup
    DataHandling.Initialize(b"")
    dataHandlingThread = DataHandlingThread(collection)
    GS.aboutToQuit.connect(dataHandlingThread.requestInterruption)
    dataHandlingThread.start()

    #inter-window connections
    collection.interWindowConnection()
    
    #showing the startup screen
    collection.startWindow.show()

    #starting the PyQt Application Loop (everything has to be defined prior to this)
    sys.exit(GS.exec())
#End