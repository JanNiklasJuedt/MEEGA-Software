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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Sensor_Calibration(object):
    def setupUi(self, Sensor_Calibration):
        if not Sensor_Calibration.objectName():
            Sensor_Calibration.setObjectName(u"Sensor_Calibration")
        Sensor_Calibration.resize(491, 350)
        self.verticalLayout = QVBoxLayout(Sensor_Calibration)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sensorSelect = QComboBox(Sensor_Calibration)
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.addItem("")
        self.sensorSelect.setObjectName(u"sensorSelect")

        self.verticalLayout.addWidget(self.sensorSelect)

        self.currentValue = QLabel(Sensor_Calibration)
        self.currentValue.setObjectName(u"currentValue")
        font = QFont()
        font.setPointSize(12)
        self.currentValue.setFont(font)
        self.currentValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.currentValue)

        self.line = QFrame(Sensor_Calibration)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.useCurrentDigital = QCheckBox(Sensor_Calibration)
        self.useCurrentDigital.setObjectName(u"useCurrentDigital")
        self.useCurrentDigital.setChecked(True)

        self.verticalLayout.addWidget(self.useCurrentDigital)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioButton3 = QRadioButton(Sensor_Calibration)
        self.radioButton3.setObjectName(u"radioButton3")

        self.gridLayout.addWidget(self.radioButton3, 3, 0, 1, 1)

        self.radioButton2 = QRadioButton(Sensor_Calibration)
        self.radioButton2.setObjectName(u"radioButton2")

        self.gridLayout.addWidget(self.radioButton2, 2, 0, 1, 1)

        self.digitalEdit1 = QLineEdit(Sensor_Calibration)
        self.digitalEdit1.setObjectName(u"digitalEdit1")

        self.gridLayout.addWidget(self.digitalEdit1, 1, 4, 1, 1)

        self.radioButton1 = QRadioButton(Sensor_Calibration)
        self.radioButton1.setObjectName(u"radioButton1")

        self.gridLayout.addWidget(self.radioButton1, 1, 0, 1, 1)

        self.analogEdit3 = QLineEdit(Sensor_Calibration)
        self.analogEdit3.setObjectName(u"analogEdit3")
        self.analogEdit3.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit3, 3, 2, 1, 1)

        self.digitalEdit3 = QLineEdit(Sensor_Calibration)
        self.digitalEdit3.setObjectName(u"digitalEdit3")

        self.gridLayout.addWidget(self.digitalEdit3, 3, 4, 1, 1)

        self.analogEdit2 = QLineEdit(Sensor_Calibration)
        self.analogEdit2.setObjectName(u"analogEdit2")
        self.analogEdit2.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit2, 2, 2, 1, 1)

        self.unitLabel1 = QLabel(Sensor_Calibration)
        self.unitLabel1.setObjectName(u"unitLabel1")

        self.gridLayout.addWidget(self.unitLabel1, 1, 3, 1, 1)

        self.analogEdit1 = QLineEdit(Sensor_Calibration)
        self.analogEdit1.setObjectName(u"analogEdit1")
        self.analogEdit1.setEnabled(True)
        self.analogEdit1.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit1, 1, 2, 1, 1)

        self.unitLabel3 = QLabel(Sensor_Calibration)
        self.unitLabel3.setObjectName(u"unitLabel3")

        self.gridLayout.addWidget(self.unitLabel3, 3, 3, 1, 1)

        self.digitalEdit2 = QLineEdit(Sensor_Calibration)
        self.digitalEdit2.setObjectName(u"digitalEdit2")

        self.gridLayout.addWidget(self.digitalEdit2, 2, 4, 1, 1)

        self.unitLabel2 = QLabel(Sensor_Calibration)
        self.unitLabel2.setObjectName(u"unitLabel2")

        self.gridLayout.addWidget(self.unitLabel2, 2, 3, 1, 1)

        self.analogValueLabel = QLabel(Sensor_Calibration)
        self.analogValueLabel.setObjectName(u"analogValueLabel")

        self.gridLayout.addWidget(self.analogValueLabel, 0, 2, 1, 1)

        self.digitalValueLabel = QLabel(Sensor_Calibration)
        self.digitalValueLabel.setObjectName(u"digitalValueLabel")

        self.gridLayout.addWidget(self.digitalValueLabel, 0, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.okButton = QPushButton(Sensor_Calibration)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setEnabled(True)

        self.verticalLayout.addWidget(self.okButton)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

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
        self.sensorSelect.setItemText(0, QCoreApplication.translate("Sensor_Calibration", u"P Ambient", None))
        self.sensorSelect.setItemText(1, QCoreApplication.translate("Sensor_Calibration", u"T Compare", None))
        self.sensorSelect.setItemText(2, QCoreApplication.translate("Sensor_Calibration", u"P Accumulator", None))
        self.sensorSelect.setItemText(3, QCoreApplication.translate("Sensor_Calibration", u"T Accumulator", None))
        self.sensorSelect.setItemText(4, QCoreApplication.translate("Sensor_Calibration", u"P Chamber", None))
        self.sensorSelect.setItemText(5, QCoreApplication.translate("Sensor_Calibration", u"T Chamber 2", None))
        self.sensorSelect.setItemText(6, QCoreApplication.translate("Sensor_Calibration", u"T Chamber 2", None))
        self.sensorSelect.setItemText(7, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 1", None))
        self.sensorSelect.setItemText(8, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 1", None))
        self.sensorSelect.setItemText(9, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 2", None))
        self.sensorSelect.setItemText(10, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 2", None))
        self.sensorSelect.setItemText(11, QCoreApplication.translate("Sensor_Calibration", u"P Nozzle 3", None))
        self.sensorSelect.setItemText(12, QCoreApplication.translate("Sensor_Calibration", u"T Nozzle 3", None))

        self.currentValue.setText(QCoreApplication.translate("Sensor_Calibration", u"0.001 \u00b0C", None))
        self.useCurrentDigital.setText(QCoreApplication.translate("Sensor_Calibration", u"Use current digital value", None))
        self.radioButton3.setText("")
        self.radioButton2.setText("")
        self.radioButton1.setText("")
        self.unitLabel1.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.unitLabel3.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.unitLabel2.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.analogValueLabel.setText(QCoreApplication.translate("Sensor_Calibration", u"Analog Value", None))
        self.digitalValueLabel.setText(QCoreApplication.translate("Sensor_Calibration", u"Digital Value", None))
        self.okButton.setText(QCoreApplication.translate("Sensor_Calibration", u"Ok", None))
    # retranslateUi

