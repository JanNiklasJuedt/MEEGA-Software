import sys
from PySide6.QtGui import (QAction, QActionGroup, QIcon,)
from PySide6.QtWidgets import (QApplication,QMainWindow,QDialog,)
from PySide6.QtCore import (Signal, Slot,QTranslator,QLocale,)

from MEEGA_mainWindow import Ui_MainWindow
from MEEGA_startup import Ui_StartDialog

class Settings:
    class Mode:
        automatic = 00
        recording = 01
        replaying = 02
        testing = 03
    class ConnectionMode:
        automatic = 10
        manual = 11
        once = 12
        never = 13
    defaultFilePath = "Default.meega"
    def __init__(self):
        self.language = QLocale.English
        self.mode = self.Mode.automatic
        self.connectionMode = self.ConnectionMode.automatic
        self.filePath = self.defaultFilePath

    def __init__(self, language: int, mode: int, connectionMode: int, filePath: str):
        self.language = language
        self.mode = mode
        self.connectionMode = connectionMode
        self.filePath = filePath

    def change(Settings):
        pass 

class MainGS(QMainWindow):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.languageGroup = QActionGroup(self.ui.menuLanguage)
        self.languageGroup.setExclusive(True)
        for i in self.ui.menuLanguage.actions():
            self.languageGroup.addAction(i)
        self.icon = QIcon("meega_logo_small.ico")
        self.setWindowIcon(self.icon)
        self.translator: QTranslator = QApplication.instance().findChild(QTranslator, name = "translator")
        self.languageGroup.triggered.connect(self.languageChange)

    #Baustelle
    @Slot(QAction)
    def languageChange(self, language: QAction):
        if self.translator.load(QLocale(language.property("lang")), "MEEGA_Language"):
            print("why?")
            self.ui.retranslateUi(self)

    @Slot(Settings)
    def acceptSettings(self, settings: Settings):
        self.settings.change(settings)
        #execute changes


class StartGS(QDialog):
    def __init__(self, mainWidget: MainGS):
        super().__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
        self.icon = QIcon("meega_logo_small.ico")
        self.setWindowIcon(self.icon)
        self.mainWidget = mainWidget
        self.rejected.connect(QApplication.instance().quit)
        self.accepted.connect(self.handleSettings)
        self.transmitSettings = Signal(Settings)
    @Slot()
    def handleSettings(self):
        language = self.ui.languageComboBox.currentText()
        connection = self.ui.connectionComboBox.currentText()
        mode = self.ui.modeComboBox.currentText()
        filepath = self.ui.saveFileEdit.text()
        # Baustelle
        settings = Settings(language,mode,connection,filepath)
        self.transmitSettings.emit(settings)
#Main
if __name__ == "__main__":
    GS = QApplication()
    translator = QTranslator(GS)
    settings = Settings()
    if translator.load(QLocale(), "MEEGA_Language"):
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