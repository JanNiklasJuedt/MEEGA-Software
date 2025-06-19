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
    QPushButton, QSizePolicy, QSpacerItem, QTimeEdit,
    QVBoxLayout, QWidget)

class Ui_controlPanel(object):
    def setupUi(self, controlPanel):
        if not controlPanel.objectName():
            controlPanel.setObjectName(u"controlPanel")
        controlPanel.resize(400, 411)
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
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximum(360.000000000000000)

        self.horizontalLayout_2.addWidget(self.doubleSpinBox)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


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
        self.pushButton_6 = QPushButton(self.groupBox)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_4.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.groupBox)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_4.addWidget(self.pushButton_7)


        self.formLayout_3.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_8 = QPushButton(self.groupBox)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_5.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.groupBox)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_5.addWidget(self.pushButton_9)


        self.formLayout_3.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_5)


        self.verticalLayout_2.addLayout(self.formLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(controlPanel)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(150, 0))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_4 = QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout_2.setItem(1, QFormLayout.ItemRole.LabelRole, self.verticalSpacer)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.timeEdit_2 = QTimeEdit(self.groupBox_2)
        self.timeEdit_2.setObjectName(u"timeEdit_2")
        self.timeEdit_2.setMaximumTime(QTime(0, 59, 59))
        self.timeEdit_2.setCurrentSection(QDateTimeEdit.Section.SecondSection)

        self.horizontalLayout_6.addWidget(self.timeEdit_2)

        self.pushButton_10 = QPushButton(self.groupBox_2)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_6.addWidget(self.pushButton_10)


        self.formLayout_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.timeEdit = QTimeEdit(self.groupBox_2)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setMaximumTime(QTime(0, 59, 59))
        self.timeEdit.setCurrentSection(QDateTimeEdit.Section.SecondSection)

        self.horizontalLayout_7.addWidget(self.timeEdit)

        self.pushButton_11 = QPushButton(self.groupBox_2)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_7.addWidget(self.pushButton_11)


        self.formLayout_2.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.timeEdit_3 = QTimeEdit(self.groupBox_2)
        self.timeEdit_3.setObjectName(u"timeEdit_3")
        self.timeEdit_3.setMaximumTime(QTime(0, 59, 59))
        self.timeEdit_3.setCurrentSection(QDateTimeEdit.Section.SecondSection)

        self.horizontalLayout_8.addWidget(self.timeEdit_3)

        self.pushButton_12 = QPushButton(self.groupBox_2)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.horizontalLayout_8.addWidget(self.pushButton_12)


        self.formLayout_2.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_13 = QPushButton(self.groupBox_2)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.horizontalLayout_9.addWidget(self.pushButton_13)


        self.formLayout_2.setLayout(5, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_9)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.retranslateUi(controlPanel)

        QMetaObject.connectSlotsByName(controlPanel)
    # setupUi

    def retranslateUi(self, controlPanel):
        controlPanel.setWindowTitle(QCoreApplication.translate("controlPanel", u"MEEGA - Control Panel", None))
        self.groupBox.setTitle(QCoreApplication.translate("controlPanel", u"Experiment Control", None))
        self.label.setText(QCoreApplication.translate("controlPanel", u"Valve", None))
        self.pushButton.setText(QCoreApplication.translate("controlPanel", u"Open", None))
        self.pushButton_2.setText(QCoreApplication.translate("controlPanel", u"Close", None))
        self.label_2.setText(QCoreApplication.translate("controlPanel", u"Servo", None))
        self.pushButton_3.setText(QCoreApplication.translate("controlPanel", u"Set", None))
        self.label_4.setText(QCoreApplication.translate("controlPanel", u"LEDs", None))
        self.pushButton_6.setText(QCoreApplication.translate("controlPanel", u"On", None))
        self.pushButton_7.setText(QCoreApplication.translate("controlPanel", u"Off", None))
        self.label_5.setText(QCoreApplication.translate("controlPanel", u"Camera", None))
        self.pushButton_8.setText(QCoreApplication.translate("controlPanel", u"On", None))
        self.pushButton_9.setText(QCoreApplication.translate("controlPanel", u"Off", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("controlPanel", u"Test Mode", None))
        self.label_3.setText(QCoreApplication.translate("controlPanel", u"Test Run", None))
        self.pushButton_4.setText(QCoreApplication.translate("controlPanel", u"Start", None))
        self.pushButton_5.setText(QCoreApplication.translate("controlPanel", u"Stop", None))
        self.label_7.setText(QCoreApplication.translate("controlPanel", u"Preparation Duration", None))
        self.timeEdit_2.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.pushButton_10.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_6.setText(QCoreApplication.translate("controlPanel", u"Experiment Duration", None))
        self.timeEdit.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.pushButton_11.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_8.setText(QCoreApplication.translate("controlPanel", u"Shutdown Duration", None))
        self.timeEdit_3.setDisplayFormat(QCoreApplication.translate("controlPanel", u"mm:ss", None))
        self.pushButton_12.setText(QCoreApplication.translate("controlPanel", u"Reset", None))
        self.label_9.setText(QCoreApplication.translate("controlPanel", u"Dry Run", None))
        self.pushButton_13.setText(QCoreApplication.translate("controlPanel", u"On", None))
    # retranslateUi

