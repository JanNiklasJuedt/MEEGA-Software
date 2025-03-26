import sys
from PySide6.QtGui import (QAction, QActionGroup, QIcon, QImage, QPixmap,)
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog)
from PySide6.QtCore import (Signal, Slot, QTranslator, QLocale)

from MEEGA_mainWindow import Ui_MainWindow
from MEEGA_startup import Ui_StartDialog

class Settings:
    class Mode:
        automatic = 0
        recording = 1
        replaying = 2
        testing = 3
    class ConnectionMode:
        automatic = 10
        manual = 11
        once = 12
        never = 13
    defaultFilePath = "Default.meega"
    def __init__(self, locale: QLocale = None, mode: int = Mode.automatic, connectionMode: int = ConnectionMode.automatic, filePath: str = defaultFilePath):
        if locale == None:
            self.locale = QLocale()
        else:
            self.locale = QLocale(locale)
        self.mode = mode
        self.connectionMode = connectionMode
        self.filePath = filePath

    def change(self, changes):
        if changes is Settings:
            self.locale = QLocale(changes.locale)
            self.mode = changes.mode
            self.connectionMode = changes.connctionMode
            self.filePath = changes.filePath
        elif changes is [object]:
            for i in changes:
                if i is QLocale:
                    self.locale = QLocale(i)
                elif i is int & i < 14 & i%10 < 4:
                    if i < 10:
                        self.mode = i
                    else:
                        self.connectionMode = i
                if i is str:
                    self.filePath = i

class MainGS(QMainWindow):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.setLocale(settings.locale)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.languageGroup = QActionGroup(self.ui.menuLanguage)
        self.languageGroup.setExclusive(True)
        for i in self.ui.menuLanguage.actions():
            self.languageGroup.addAction(i)
        self.modeGroup = QActionGroup(self.ui.menuMode)
        self.modeGroup.setExclusive(True)
        for i in self.ui.menuMode.actions():
            self.modeGroup.addAction(i)
        self.connectionModeGroup = QActionGroup(self.ui.menuConnectionMode)
        self.connectionModeGroup.setExclusive(True)
        for i in self.ui.menuConnectionMode.actions():
            self.connectionModeGroup.addAction(i)
        self.app = QApplication.instance()
        self.languageGroup.triggered.connect(self.languageChange)
    def retranslateUi(self):
        self.ui.retranslateUi()
    @Slot()
    def languageChange(self, fromSettings = False):
        translator = QTranslator()
        if  not fromSettings:
            language = self.languageGroup.checkedAction().property("data")
            locale = QLocale(language)
            self.settings.change([locale])
        else:
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
    @Slot()
    def modeChange(self, fromSettings = False):
        pass
    @Slot()
    def connectionModeChange(self, fromSettings = False):
        pass
    @Slot()
    def filePathChange(self, fromSettings = False):
        pass
    @Slot(Settings)
    def acceptSettings(self, settings: Settings):
        self.settings.change(settings)
        self.setLocale(settings.locale)
        self.languageChange(True)
        self.modeChange(True)
        self.connectionModeChange(True)
        self.filePathChange(True)


class StartGS(QDialog):
    transmitSettings = Signal(Settings)
    def __init__(self, mainWidget: MainGS):
        super().__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
        self.ui.languageComboBox.setItemData(0, "en")
        self.ui.languageComboBox.setItemData(1, "de")
        self.ui.connectionComboBox.setItemData(0,Settings.ConnectionMode.automatic)
        self.ui.connectionComboBox.setItemData(1,Settings.ConnectionMode.once)
        self.ui.connectionComboBox.setItemData(2,Settings.ConnectionMode.manual)
        self.ui.connectionComboBox.setItemData(3,Settings.ConnectionMode.never)
        self.ui.modeComboBox.setItemData(0, Settings.Mode.automatic)
        self.ui.modeComboBox.setItemData(1, Settings.Mode.testing)
        self.ui.modeComboBox.setItemData(2, Settings.Mode.recording)
        self.ui.modeComboBox.setItemData(3, Settings.Mode.replaying)
        self.mainWidget = mainWidget
        self.rejected.connect(QApplication.instance().quit)
        self.accepted.connect(self.handleSettings)
    @Slot()
    def handleSettings(self):
        language = self.ui.languageComboBox.currentData()
        connection = self.ui.connectionComboBox.currentData()
        mode = self.ui.modeComboBox.currentData()
        filepath = self.ui.saveFileEdit.text()
        settings = Settings(language,mode,connection,filepath)
        self.transmitSettings.emit(settings)
#Main
if __name__ == "__main__":
    GS = QApplication()
    icon = QIcon("meega_logo_small.png")
    GS.setWindowIcon(icon)
    translator = QTranslator()
    QLocale.setDefault(QLocale.C)
    settings = Settings()
    if translator.load(settings.locale, "MEEGA_Language"):
        GS.installTranslator(translator)

    mainWidget = MainGS(settings)
    startWidget = StartGS(mainWidget)
    
    language = translator.language()
    activeMode = "Recording"
    connectionMode = "None"
    connection = None
    file = None

    mainWidget.ui.actionQuit.triggered.connect(GS.quit)
    mainWidget.ui.actionRestart.triggered.connect(startWidget.show)
    mainWidget.show()
    startWidget.show()
    sys.exit(GS.exec())