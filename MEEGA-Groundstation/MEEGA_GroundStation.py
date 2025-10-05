#imports
from asyncio.windows_events import NULL
import sys
import time
from tkinter import SEL

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
    FLIGHT = 2
    TEST = 3
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

#class to define the Main Window
class GSMain(QMainWindow):
    def __init__(self, settings: Settings):
        super().__init__()

        #importing visuals from the ui-file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #creating variables
        self.ACTIVE = 0
        self.ISSUES = 1
        self.INACTIVE = 2

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

        self.settings = settings
        self.setLocale(settings.locale)

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
        self.ui.actionFlight_Mode.triggered.connect(self.fetchSettings)
        self.ui.actionTest_Mode.triggered.connect(self.fetchSettings)
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
            self.scalePixmaps(event)
            super().resizeEvent(event)
    def retranslateUi(self):
        self.ui.retranslateUi()
    def languageChanges(self):
        translator = QTranslator()
        locale = self.settings.locale
        language = QLocale.languageToCode(locale.language())
        for i in self.languageGroup.actions():
            if i.property("data") == language:
                i.setChecked(True)
        #Baustelle:
        if translator.load(locale, "MEEGA_Language"):
            self.app.removeTranslator(translator)
            self.app.installTranslator(translator)
            self.retranslateUi(self)
    def modeChanges(self):
        if settings.mode == Settings.TEST:
            self.ui.label_mode.setText("Test Mode")
            self.ui.actionControl_Panel.setEnabled(True)
        else:
            self.ui.label_mode.setText("Flight Mode")
            self.ui.actionControl_Panel.setEnabled(False)
    def connectionModeChanges(self):
        if settings.connectionMode == Settings.AUTOMATIC:
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
        if not bool(frame) == False:
            frame = frame.contents.data
            for i in range(12):
                self.status[i][0] = DataHandling.ReadFrame(frame, 12+i)
            self.status[12][0] = DataHandling.ReadFrame(frame, 25)
            self.status[13][0] = DataHandling.ReadFrame(frame, 26)
            self.status[14][0] = DataHandling.ReadFrame(frame, 28)
            self.status[15][0] = DataHandling.ReadFrame(frame, 29)
            self.status[16][0] = DataHandling.ReadFrame(frame, 30)
            self.status[17][0] = DataHandling.ReadFrame(frame, 31)
            self.status[18][0] = DataHandling.ReadFrame(frame, 33)
            self.status[19][0] = DataHandling.ReadFrame(frame, 34)
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
    def fetchSettings(self):
        if self.connectionModeGroup.checkedAction() == self.ui.actionAutomatic:
            connectionMode = Settings.AUTOMATIC
        else:
            connectionMode = Settings.MANUAL
        if self.modeGroup.checkedAction() == self.ui.actionFlight_Mode:
            mode = Settings.FLIGHT
        else:
            mode = Settings.TEST
        self.settings.mode = mode
        self.settings.connectionMode = connectionMode
        self.modeChanges()
        self.connectionModeChanges()
    @Slot()
    def applySettings(self):
        if self.settings.connectionMode == Settings.AUTOMATIC:
            self.ui.actionAutomatic.setChecked(True)
        else:
            self.ui.actionManual.setChecked(True)
        if self.settings.mode == Settings.FLIGHT:
            self.ui.actionFlight_Mode.setChecked(True)
        else:
            self.ui.actionTest_Mode.setChecked(True)
        self.setLocale(self.settings.locale)
        self.languageChanges()
        self.modeChanges()
        self.connectionModeChanges()
        self.filePathChanges()

#class to define the startup dialog window
class GSStart(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
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
        self.settings.language = self.ui.languageComboBox.currentData()
        self.settings.connectionMode = self.ui.connectionComboBox.currentData()
        self.settings.mode = self.ui.modeComboBox.currentData()
        self.settings.filepath = self.ui.saveFileEdit.text()
        self.settings.launchTime = self.ui.launchTimeTimeEdit.time()

class GSLaunchTime(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_LaunchTimeDialog()
        self.ui.setupUi(self)

        self.accepted.connect(self.fetchSettings)
    
    @Slot()
    def fetchSettings(self):
        self.settings.launchTime = self.ui.launchTimeEdit.time()

class GSResults(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ResultsWidget()
        self.ui.setupUi(self)

        self.ui.buttonBox.clicked.connect(self.hide)

class GSDocumentation(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Documentation()
        self.ui.setupUi(self)

class GSError(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self)

class GSControl(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_controlPanel()
        self.ui.setupUi(self)

class GSConnection(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

class GSCalibration(QDialog):
    selectedSensor = 0
    selectedEntry = 0
    currentUnit = ""
    calibrationPoints = [[0] * 3 for x in range(12)]
    def __init__(self):
        super().__init__()
        self.ui = Ui_Sensor_Calibration()
        self.ui.setupUi(self)

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
            mappedValue = DataHandling.MapSensorValue(self.selectedSensor, digitalValue)
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
    def __init__(self, mainWindow, calibrationWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.calibrationWindow = calibrationWindow
    def run(self):
        period_ms = 1000 / 20
        while True:
            clock = time.monotonic_ns()
            DataHandling.UpdateAll()
            self.mainWindow.fetchStatus()
            self.calibrationWindow.updateValue()
            if self.isInterruptionRequested():
               break
            self.msleep(period_ms - (time.monotonic_ns() - clock) / 1000000)

#Main
if __name__ == "__main__":
    GS = QApplication()
    icon = QIcon("Ressources\\meega_logo_small.ico")
    GS.setWindowIcon(icon)
    translator = QTranslator()
    QLocale.setDefault(QLocale.C)
    settings = Settings()
    if translator.load(settings.locale, "MEEGA_Language"):
        GS.installTranslator(translator)

    #window objects creation
    GSmain = GSMain(settings)
    GSstart = GSStart(settings)
    GScontrol = GSControl()
    GStime = GSLaunchTime(settings)
    GSdocument = GSDocumentation()
    GSerror = GSError()
    GSresults = GSResults()
    GSconnection = GSConnection()
    GScalibration = GSCalibration()

    #DataHandling setup
    DataHandling.Initialize(b"")
    dataHandlingThread = DataHandlingThread(GSmain, GScalibration)
    GS.aboutToQuit.connect(dataHandlingThread.requestInterruption)
    dataHandlingThread.start()

    #inter-window connections
    GSmain.ui.actionRestart.triggered.connect(GSstart.show)
    GSmain.ui.actionRestart.triggered.connect(GSmain.hide)
    GSmain.ui.actionControl_Panel.triggered.connect(GScontrol.show)
    GSmain.ui.actionDocumentation.triggered.connect(GSdocument.show)
    GSmain.ui.actionConnect.triggered.connect(GSconnection.show)
    GSmain.ui.actionResults.triggered.connect(GSresults.show)
    GSmain.ui.actionEstimated_Launch_Time.triggered.connect(GStime.show)
    GSstart.accepted.connect(GSmain.applySettings)
    GSstart.accepted.connect(GSmain.show)
    GStime.accepted.connect(GSmain.applySettings)
    GSmain.ui.actionCalibration.triggered.connect(GScalibration.show)
    
    #showing the startup screen
    GSstart.show()

    #starting the PyQt Application Loop (everything has to be defined prior to this)
    sys.exit(GS.exec())
#End