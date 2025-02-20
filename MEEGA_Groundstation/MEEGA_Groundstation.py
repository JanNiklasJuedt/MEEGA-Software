import sys
import random
from PySide6 import QtCore,QtWidgets,QtGui
from MEEGA_main import Ui_MainWindow

class NewWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon = QtGui.QIcon("meega_logo_small.ico")
        self.setIconSize(QtCore.QSize(100,100))
        self.setWindowIcon(self.icon)
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = NewWidget()
    widget.show()
    sys.exit(app.exec())
