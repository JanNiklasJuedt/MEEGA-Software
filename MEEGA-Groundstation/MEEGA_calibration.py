# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_calibration.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
        Sensor_Calibration.resize(491, 209)
        self.verticalLayout = QVBoxLayout(Sensor_Calibration)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = QComboBox(Sensor_Calibration)
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
        self.pushButton = QPushButton(Sensor_Calibration)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton, 0, 3, 1, 1)

        self.pushButton_2 = QPushButton(Sensor_Calibration)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 3, 1, 1)

        self.label_2 = QLabel(Sensor_Calibration)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(Sensor_Calibration)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.radioButton_2 = QRadioButton(Sensor_Calibration)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.radioButton = QRadioButton(Sensor_Calibration)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(Sensor_Calibration)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

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

        self.label.setText(QCoreApplication.translate("Sensor_Calibration", u"0.001 \u00b0C", None))
        self.pushButton.setText(QCoreApplication.translate("Sensor_Calibration", u"Ok", None))
        self.pushButton_2.setText(QCoreApplication.translate("Sensor_Calibration", u"Ok", None))
        self.label_2.setText(QCoreApplication.translate("Sensor_Calibration", u"\u00b0C", None))
        self.radioButton_2.setText("")
        self.radioButton.setText("")
    # retranslateUi

