import sys
from PySide6 import QtCore,QtWidgets,QtGui
from MEEGA_mainWindow import Ui_MainWindow
from MEEGA_startup import Ui_Dialog

class MainGS(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon = QtGui.QIcon("meega_logo_small.ico")
        self.setWindowIcon(self.icon)
        self.activeLanguage = "English"

class StartGS(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.icon = QtGui.QIcon("meega_logo_small.ico")
        self.setWindowIcon(self.icon)

#Main
if __name__ == "__main__":
    GS = QtWidgets.QApplication()
    mainWidget = MainGS()
    startWidget = StartGS()
    mainWidget.ui.actionQuit.triggered.connect(GS.quit)
    mainWidget.ui.actionRestart.triggered.connect(startWidget.show)
    mainWidget.show()
    startWidget.show()
    sys.exit(GS.exec())