# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_calibration.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Sensor_Calibration(object):
    def setupUi(self, Sensor_Calibration):
        if not Sensor_Calibration.objectName():
            Sensor_Calibration.setObjectName(u"Sensor_Calibration")
        Sensor_Calibration.resize(491, 285)
        self.verticalLayout = QVBoxLayout(Sensor_Calibration)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = QComboBox(Sensor_Calibration)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.label = QLabel(Sensor_Calibration)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(Sensor_Calibration)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit = QLineEdit(Sensor_Calibration)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(True)
        self.lineEdit.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)

        self.radioButton_3 = QRadioButton(Sensor_Calibration)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout.addWidget(self.radioButton_3, 2, 0, 1, 1)

        self.radioButton_2 = QRadioButton(Sensor_Calibration)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.label_3 = QLabel(Sensor_Calibration)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 3, 1, 1)

        self.label_4 = QLabel(Sensor_Calibration)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 3, 1, 1)

        self.lineEdit_2 = QLineEdit(Sensor_Calibration)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.lineEdit_2, 1, 2, 1, 1)

        self.label_2 = QLabel(Sensor_Calibration)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)

        self.lineEdit_3 = QLineEdit(Sensor_Calibration)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.lineEdit_3, 2, 2, 1, 1)

        self.radioButton = QRadioButton(Sensor_Calibration)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.pushButton = QPushButton(Sensor_Calibration)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Sensor_Calibration)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Sensor_Calibration)
        self.buttonBox.accepted.connect(Sensor_Calibration.accept)
        self.buttonBox.rejected.connect(Sensor_Calibration.reject)

        QMetaObject.connectSlotsByName(Sensor_Calibration)
    # setupUi

    def retranslateUi(self, Sensor_Calibration):
        Sensor_Calibration.setWindowTitle(QCoreApplication.translate("Sensor_Calibration", u"MEEGA - Sensor Calibration", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Sensor_Calibration", u"P Ambient", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Sensor_Calibration", u"T Compare", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Sensor_Calibration", u"P Reservoir", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Sensor_Calibration", u"T Reservoir", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Sensor_Calibration", u"P Accumulator", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Sensor_Calibration", u"T Accumulator", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 1", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 1", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 2", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 2", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 3", None))
        self.comboBox.setItemText(11, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 3", None))

        self.label.setText(QCoreApplication.translate("Sensor_Calibration", u"0.001 \u00b0C", None))
        self.radioButton_3.setText("")
        self.radioButton_2.setText("")
        self.label_3.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.label_4.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.label_2.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.radioButton.setText("")
        self.pushButton.setText(QCoreApplication.translate("Sensor_Calibration", u"Ok", None))
    # retranslateUi

