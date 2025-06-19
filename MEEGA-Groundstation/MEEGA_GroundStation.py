#imports
import sys
from PySide6.QtGui import (QAction, QActionGroup, QIcon, QImage, QPixmap,)
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QWidget)
from PySide6.QtCore import (Signal, Slot, QTranslator, QLocale)

from MEEGA_mainWindow import *
from MEEGA_startup import *
from MEEGA_connection import *
from MEEGA_time import *
from MEEGA_documentation import *
from MEEGA_error import *
from MEEGA_controlPanel import *
from MEEGA_results import *

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

        self.settings = settings
        self.setLocale(settings.locale)

        #importing visuals from the ui-file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
    def filePathChanges(self):
        pass
    
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
    def __init__(self):
        super().__init__()
        self.ui = Ui_LaunchTimeDialog()
        self.ui.setupUi(self)

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
    mainWindow = GSMain(settings)
    start = GSStart(settings)
    control = GSControl()
    time = GSLaunchTime()
    document = GSDocumentation()
    error = GSError()
    results = GSResults()
    connectionWindow = GSConnection()

    #inter-window connections
    mainWindow.ui.actionRestart.triggered.connect(start.show)
    mainWindow.ui.actionRestart.triggered.connect(mainWindow.hide)
    mainWindow.ui.actionControl_Panel.triggered.connect(control.show)
    mainWindow.ui.actionDocumentation.triggered.connect(document.show)
    mainWindow.ui.actionConnect.triggered.connect(connectionWindow.show)
    mainWindow.ui.actionResults.triggered.connect(results.show)
    mainWindow.ui.actionEstimated_Launch_Time.triggered.connect(time.show)
    start.accepted.connect(mainWindow.applySettings)
    start.accepted.connect(mainWindow.show)
    
    #showing the startup screen
    start.show()

    #starting the PyQt Application Loop (everything has to be defined prior to this)
    sys.exit(GS.exec())
#End