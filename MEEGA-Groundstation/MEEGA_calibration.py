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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QWidget)

class Ui_Calibration(object):
    def setupUi(self, Calibration):
        if not Calibration.objectName():
            Calibration.setObjectName(u"Calibration")
        Calibration.resize(400, 280)
        Calibration.setMinimumSize(QSize(400, 280))
        Calibration.setMaximumSize(QSize(400, 280))
        self.currentValue = QLabel(Calibration)
        self.currentValue.setObjectName(u"currentValue")
        self.currentValue.setGeometry(QRect(20, 40, 361, 27))
        font = QFont()
        font.setPointSize(12)
        self.currentValue.setFont(font)
        self.currentValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.useCurrentDigital = QCheckBox(Calibration)
        self.useCurrentDigital.setObjectName(u"useCurrentDigital")
        self.useCurrentDigital.setGeometry(QRect(10, 80, 321, 24))
        self.useCurrentDigital.setChecked(True)
        self.okButton = QPushButton(Calibration)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setEnabled(True)
        self.okButton.setGeometry(QRect(10, 240, 381, 29))
        self.sensorSelect = QComboBox(Calibration)
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
        self.sensorSelect.setGeometry(QRect(10, 10, 381, 26))
        self.layoutWidget = QWidget(Calibration)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 110, 381, 121))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton3 = QRadioButton(self.layoutWidget)
        self.radioButton3.setObjectName(u"radioButton3")

        self.gridLayout.addWidget(self.radioButton3, 3, 0, 1, 1)

        self.radioButton2 = QRadioButton(self.layoutWidget)
        self.radioButton2.setObjectName(u"radioButton2")

        self.gridLayout.addWidget(self.radioButton2, 2, 0, 1, 1)

        self.digitalEdit1 = QLineEdit(self.layoutWidget)
        self.digitalEdit1.setObjectName(u"digitalEdit1")

        self.gridLayout.addWidget(self.digitalEdit1, 1, 4, 1, 1)

        self.radioButton1 = QRadioButton(self.layoutWidget)
        self.radioButton1.setObjectName(u"radioButton1")

        self.gridLayout.addWidget(self.radioButton1, 1, 0, 1, 1)

        self.digitalEdit3 = QLineEdit(self.layoutWidget)
        self.digitalEdit3.setObjectName(u"digitalEdit3")

        self.gridLayout.addWidget(self.digitalEdit3, 3, 4, 1, 1)

        self.analogEdit2 = QLineEdit(self.layoutWidget)
        self.analogEdit2.setObjectName(u"analogEdit2")
        self.analogEdit2.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit2, 2, 2, 1, 1)

        self.unitLabel1 = QLabel(self.layoutWidget)
        self.unitLabel1.setObjectName(u"unitLabel1")

        self.gridLayout.addWidget(self.unitLabel1, 1, 3, 1, 1)

        self.analogEdit1 = QLineEdit(self.layoutWidget)
        self.analogEdit1.setObjectName(u"analogEdit1")
        self.analogEdit1.setEnabled(True)
        self.analogEdit1.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit1, 1, 2, 1, 1)

        self.unitLabel3 = QLabel(self.layoutWidget)
        self.unitLabel3.setObjectName(u"unitLabel3")

        self.gridLayout.addWidget(self.unitLabel3, 3, 3, 1, 1)

        self.digitalEdit2 = QLineEdit(self.layoutWidget)
        self.digitalEdit2.setObjectName(u"digitalEdit2")

        self.gridLayout.addWidget(self.digitalEdit2, 2, 4, 1, 1)

        self.unitLabel2 = QLabel(self.layoutWidget)
        self.unitLabel2.setObjectName(u"unitLabel2")

        self.gridLayout.addWidget(self.unitLabel2, 2, 3, 1, 1)

        self.analogValueLabel = QLabel(self.layoutWidget)
        self.analogValueLabel.setObjectName(u"analogValueLabel")

        self.gridLayout.addWidget(self.analogValueLabel, 0, 2, 1, 1)

        self.digitalValueLabel = QLabel(self.layoutWidget)
        self.digitalValueLabel.setObjectName(u"digitalValueLabel")

        self.gridLayout.addWidget(self.digitalValueLabel, 0, 4, 1, 1)

        self.analogEdit3 = QLineEdit(self.layoutWidget)
        self.analogEdit3.setObjectName(u"analogEdit3")
        self.analogEdit3.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.analogEdit3, 3, 2, 1, 1)


        self.retranslateUi(Calibration)

        QMetaObject.connectSlotsByName(Calibration)
    # setupUi

    def retranslateUi(self, Calibration):
        Calibration.setWindowTitle(QCoreApplication.translate("Calibration", u"Calibration", None))
        self.currentValue.setText(QCoreApplication.translate("Calibration", u"0.001 \u00b0C", None))
        self.useCurrentDigital.setText(QCoreApplication.translate("Calibration", u"Use current digital value", None))
        self.okButton.setText(QCoreApplication.translate("Calibration", u"Ok", None))
        self.sensorSelect.setItemText(0, QCoreApplication.translate("Calibration", u"P Ambient", None))
        self.sensorSelect.setItemText(1, QCoreApplication.translate("Calibration", u"T Compare", None))
        self.sensorSelect.setItemText(2, QCoreApplication.translate("Calibration", u"P Accumulator", None))
        self.sensorSelect.setItemText(3, QCoreApplication.translate("Calibration", u"T Accumulator", None))
        self.sensorSelect.setItemText(4, QCoreApplication.translate("Calibration", u"P Chamber", None))
        self.sensorSelect.setItemText(5, QCoreApplication.translate("Calibration", u"T Chamber 1", None))
        self.sensorSelect.setItemText(6, QCoreApplication.translate("Calibration", u"T Chamber 2", None))
        self.sensorSelect.setItemText(7, QCoreApplication.translate("Calibration", u"P Nozzle 1", None))
        self.sensorSelect.setItemText(8, QCoreApplication.translate("Calibration", u"T Nozzle 1", None))
        self.sensorSelect.setItemText(9, QCoreApplication.translate("Calibration", u"P Nozzle 2", None))
        self.sensorSelect.setItemText(10, QCoreApplication.translate("Calibration", u"T Nozzle 2", None))
        self.sensorSelect.setItemText(11, QCoreApplication.translate("Calibration", u"P Nozzle 3", None))
        self.sensorSelect.setItemText(12, QCoreApplication.translate("Calibration", u"T Nozzle 3", None))

        self.radioButton3.setText("")
        self.radioButton2.setText("")
        self.radioButton1.setText("")
        self.unitLabel1.setText(QCoreApplication.translate("Calibration", u"\u00b0C", None))
        self.unitLabel3.setText(QCoreApplication.translate("Calibration", u"\u00b0C", None))
        self.unitLabel2.setText(QCoreApplication.translate("Calibration", u"\u00b0C", None))
        self.analogValueLabel.setText(QCoreApplication.translate("Calibration", u"Analog Value", None))
        self.digitalValueLabel.setText(QCoreApplication.translate("Calibration", u"Digital Value", None))
    # retranslateUi

