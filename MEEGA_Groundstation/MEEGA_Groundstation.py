import sys
import random
from PySide6 import QtCore,QtWidgets,QtGui
from MEEGA_mainWindow import Ui_MainWindow

class Groundstation(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon = QtGui.QIcon("meega_logo_small.ico")
        self.setWindowIcon(self.icon)
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Groundstation()
    widget.show()
    sys.exit(app.exec())
