# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_controlPanel.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDoubleSpinBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_controlPanel(object):
    def setupUi(self, controlPanel):
        if not controlPanel.objectName():
            controlPanel.setObjectName(u"controlPanel")
        controlPanel.resize(421, 448)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(controlPanel.sizePolicy().hasHeightForWidth())
        controlPanel.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(controlPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(controlPanel)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.openValveButton = QPushButton(self.groupBox)
        self.openValveButton.setObjectName(u"openValveButton")

        self.horizontalLayout.addWidget(self.openValveButton)

        self.closeValveButton = QPushButton(self.groupBox)
        self.closeValveButton.setObjectName(u"closeValveButton")

        self.horizontalLayout.addWidget(self.closeValveButton)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.servoValueBox = QDoubleSpinBox(self.groupBox)
        self.servoValueBox.setObjectName(u"servoValueBox")
        self.servoValueBox.setMinimum(-1.000000000000000)
        self.servoValueBox.setMaximum(360.000000000000000)
        self.servoValueBox.setValue(-1.000000000000000)

        self.horizontalLayout_2.addWidget(self.servoValueBox)

        self.setServoButton = QPushButton(self.groupBox)
        self.setServoButton.setObjectName(u"setServoButton")

        self.horizontalLayout_2.addWidget(self.setServoButton)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(150, 0))

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ledOnButton = QPushButton(self.groupBox)
        self.ledOnButton.setObjectName(u"ledOnButton")

        self.horizontalLayout_4.addWidget(self.ledOnButton)

        self.ledOffButton = QPushButton(self.groupBox)
        self.ledOffButton.setObjectName(u"ledOffButton")

        self.horizontalLayout_4.addWidget(self.ledOffButton)


        self.formLayout_3.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)


        self.verticalLayout_2.addLayout(self.formLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(controlPanel)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.startTestButton = QPushButton(self.groupBox_2)
        self.startTestButton.setObjectName(u"startTestButton")

        self.horizontalLayout_3.addWidget(self.startTestButton)

        self.stopTestButton = QPushButton(self.groupBox_2)
        self.stopTestButton.setObjectName(u"stopTestButton")

        self.horizontalLayout_3.addWidget(self.stopTestButton)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout_2.setItem(1, QFormLayout.ItemRole.LabelRole, self.verticalSpacer)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.valveTimeEdit = QTimeEdit(self.groupBox_2)
        self.valveTimeEdit.setObjectName(u"valveTimeEdit")
        self.valveTimeEdit.setMaximumTime(QTime(0, 59, 59))
        self.valveTimeEdit.setCurrentSection(QDateTimeEdit.Section.MinuteSection)

        self.horizontalLayout_6.addWidget(self.valveTimeEdit)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(5, 16777215))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.valveMilliEdit = QLineEdit(self.groupBox_2)
        self.valveMilliEdit.setObjectName(u"valveMilliEdit")
        sizePolicy.setHeightForWidth(self.valveMilliEdit.sizePolicy().hasHeightForWidth())
        self.valveMilliEdit.setSizePolicy(sizePolicy)
        self.valveMilliEdit.setMaximumSize(QSize(35, 16777215))
        self.valveMilliEdit.setBaseSize(QSize(0, 0))
        self.valveMilliEdit.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.valveMilliEdit.setMaxLength(3)

        self.horizontalLayout_6.addWidget(self.valveMilliEdit)

        self.valveResetButton = QPushButton(self.groupBox_2)
        self.valveResetButton.setObjectName(u"valveResetButton")

        self.horizontalLayout_6.addWidget(self.valveResetButton)


        self.formLayout_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.servoTimeEdit = QTimeEdit(self.groupBox_2)
        self.servoTimeEdit.setObjectName(u"servoTimeEdit")
        self.servoTimeEdit.setMaximumTime(QTime(0, 59, 59))
        self.servoTimeEdit.setCurrentSection(QDateTimeEdit.Section.MinuteSection)

        self.horizontalLayout_7.addWidget(self.servoTimeEdit)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(5, 16777215))

        self.horizontalLayout_7.addWidget(self.label_10)

        self.servoMilliEdit = QLineEdit(self.groupBox_2)
        self.servoMilliEdit.setObjectName(u"servoMilliEdit")
        sizePolicy.setHeightForWidth(self.servoMilliEdit.sizePolicy().hasHeightForWidth())
        self.servoMilliEdit.setSizePolicy(sizePolicy)
        self.servoMilliEdit.setMaximumSize(QSize(35, 16777215))
        self.servoMilliEdit.setBaseSize(QSize(0, 0))
        self.servoMilliEdit.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.servoMilliEdit.setMaxLength(3)

        self.horizontalLayout_7.addWidget(self.servoMilliEdit)

        self.servoResetButton = QPushButton(self.groupBox_2)
        self.servoResetButton.setObjectName(u"servoResetButton")

        self.horizontalLayout_7.addWidget(self.servoResetButton)


        self.formLayout_2.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.EOETimeEdit = QTimeEdit(self.groupBox_2)
        self.EOETimeEdit.setObjectName(u"EOETimeEdit")
        self.EOETimeEdit.setMaximumTime(QTime(0, 59, 59))
        self.EOETimeEdit.setCurrentSection(QDateTimeEdit.Section.MinuteSection)

        self.horizontalLayout_8.addWidget(self.EOETimeEdit)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(5, 16777215))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.EOEMilliEdit = QLineEdit(self.groupBox_2)
        self.EOEMilliEdit.setObjectName(u"EOEMilliEdit")
        sizePolicy.setHeightForWidth(self.EOEMilliEdit.sizePolicy().hasHeightForWidth())
        self.EOEMilliEdit.setSizePolicy(sizePolicy)
        self.EOEMilliEdit.setMaximumSize(QSize(35, 16777215))
        self.EOEMilliEdit.setBaseSize(QSize(0, 0))
        self.EOEMilliEdit.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.EOEMilliEdit.setMaxLength(3)

        self.horizontalLayout_8.addWidget(self.EOEMilliEdit)

        self.EOEResetButton = QPushButton(self.groupBox_2)
        self.EOEResetButton.setObjectName(u"EOEResetButton")

        self.horizontalLayout_8.addWidget(self.EOEResetButton)


        self.formLayout_2.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.dryRunOnButton = QPushButton(self.groupBox_2)
        self.dryRunOnButton.setObjectName(u"dryRunOnButton")
        self.dryRunOnButton.setCheckable(True)

        self.horizontalLayout_9.addWidget(self.dryRunOnButton)


        self.formLayout_2.setLayout(5, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_9)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(150, 0))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_7)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.retranslateUi(controlPanel)

        QMetaObject.connectSlotsByName(controlPanel)
    # setupUi

    def retranslateUi(self, controlPanel):
        controlPanel.setWindowTitle(QCoreApplication.translate("controlPanel", u"MEEGA - Control Panel", None))
        self.groupBox.setTitle(QCoreApplication.translate("controlPanel", u"Experiment Control", None))
        self.label.setText(QCoreApplication.translate("controlPanel", u"Valve", None))
        self.openValveButton.setText(QCoreApplication.translate("controlPanel", u"Open", None))
        self.closeValveButton.setText(QCoreApplication.translate("controlPanel", u"Close", None))
        self.label_2.setText(QCoreApplication.translate("controlPanel", u"Servo", None))
        self.setServoButton.setText(QCoreApplication.translate("controlPanel", u"Set", None))
        self.label_4.setText(QCoreApplication.translate("controlPanel", u"LEDs", None))
        self.ledOnButton.setText(QCoreApplication.translate("controlPanel", u"On", None))
        self.ledOffButton.setText(QCoreApplication.translate("controlPanel", u"Off", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("controlPanel", u"Test Mode", None))
        self.startTestButton.setText(QCoreApplication.translate("controlPanel", u"Start", None))
        self.stopTestButton.setText(QCoreApplication.translate("controlPanel", u"Stop", None))
        self.valveTimeEdit.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.label_5.setText(QCoreApplication.translate("controlPanel", u",", None))
        self.valveMilliEdit.setText(QCoreApplication.translate("controlPanel", u"000", None))
        self.valveResetButton.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_6.setText(QCoreApplication.translate("controlPanel", u"Servo Cycle Time", None))
        self.servoTimeEdit.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.label_10.setText(QCoreApplication.translate("controlPanel", u",", None))
        self.servoMilliEdit.setText(QCoreApplication.translate("controlPanel", u"000", None))
        self.servoResetButton.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_8.setText(QCoreApplication.translate("controlPanel", u"Active Experiment Time", None))
        self.EOETimeEdit.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.label_11.setText(QCoreApplication.translate("controlPanel", u",", None))
        self.EOEMilliEdit.setText(QCoreApplication.translate("controlPanel", u"000", None))
        self.EOEResetButton.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_9.setText(QCoreApplication.translate("controlPanel", u"Dry Run", None))
        self.dryRunOnButton.setText(QCoreApplication.translate("controlPanel", u"On", None))
        self.label_3.setText(QCoreApplication.translate("controlPanel", u"Test Run", None))
        self.label_7.setText(QCoreApplication.translate("controlPanel", u"Valve Open Time", None))
    # retranslateUi

