# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_diagramSettings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QLayout, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_diagramSettings(object):
    def setupUi(self, diagramSettings):
        if not diagramSettings.objectName():
            diagramSettings.setObjectName(u"diagramSettings")
        diagramSettings.resize(270, 430)
        diagramSettings.setMinimumSize(QSize(270, 430))
        diagramSettings.setMaximumSize(QSize(270, 430))
        self.verticalLayoutWidget = QWidget(diagramSettings)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 251, 411))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pressureAxes = QGroupBox(self.verticalLayoutWidget)
        self.pressureAxes.setObjectName(u"pressureAxes")
        self.pressureAxes.setMinimumSize(QSize(0, 100))
        self.pressureAxes.setMaximumSize(QSize(16777215, 100))
        self.gridLayoutWidget = QWidget(self.pressureAxes)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 19, 231, 71))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pressureSelfScaling = QRadioButton(self.gridLayoutWidget)
        self.pressureSelfScaling.setObjectName(u"pressureSelfScaling")
        self.pressureSelfScaling.setChecked(True)

        self.gridLayout.addWidget(self.pressureSelfScaling, 0, 0, 1, 1)

        self.pressureFixedValue = QRadioButton(self.gridLayoutWidget)
        self.pressureFixedValue.setObjectName(u"pressureFixedValue")

        self.gridLayout.addWidget(self.pressureFixedValue, 1, 0, 1, 1)

        self.pressureLineEdit = QLineEdit(self.gridLayoutWidget)
        self.pressureLineEdit.setObjectName(u"pressureLineEdit")
        self.pressureLineEdit.setEnabled(False)
        self.pressureLineEdit.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout.addWidget(self.pressureLineEdit, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.pressureAxes)

        self.temperatureAxes = QGroupBox(self.verticalLayoutWidget)
        self.temperatureAxes.setObjectName(u"temperatureAxes")
        self.temperatureAxes.setMinimumSize(QSize(0, 100))
        self.temperatureAxes.setMaximumSize(QSize(16777215, 100))
        self.gridLayoutWidget_2 = QWidget(self.temperatureAxes)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(9, 19, 231, 71))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.temperatureFixedValue = QRadioButton(self.gridLayoutWidget_2)
        self.temperatureFixedValue.setObjectName(u"temperatureFixedValue")

        self.gridLayout_2.addWidget(self.temperatureFixedValue, 1, 0, 1, 1)

        self.temperatureSelfScaling = QRadioButton(self.gridLayoutWidget_2)
        self.temperatureSelfScaling.setObjectName(u"temperatureSelfScaling")
        self.temperatureSelfScaling.setChecked(True)

        self.gridLayout_2.addWidget(self.temperatureSelfScaling, 0, 0, 1, 1)

        self.temperatureLineEdit = QLineEdit(self.gridLayoutWidget_2)
        self.temperatureLineEdit.setObjectName(u"temperatureLineEdit")
        self.temperatureLineEdit.setEnabled(False)
        self.temperatureLineEdit.setInputMethodHints(Qt.InputMethodHint.ImhFormattedNumbersOnly)

        self.gridLayout_2.addWidget(self.temperatureLineEdit, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.temperatureAxes)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.shownTimespan = QGroupBox(self.verticalLayoutWidget)
        self.shownTimespan.setObjectName(u"shownTimespan")
        self.shownTimespan.setMinimumSize(QSize(0, 140))
        self.shownTimespan.setMaximumSize(QSize(16777215, 140))
        self.shownTimespan.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.gridLayoutWidget_3 = QWidget(self.shownTimespan)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(9, 19, 231, 111))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.expandingRadioButton = QRadioButton(self.gridLayoutWidget_3)
        self.expandingRadioButton.setObjectName(u"expandingRadioButton")
        self.expandingRadioButton.setChecked(True)

        self.gridLayout_3.addWidget(self.expandingRadioButton, 3, 0, 1, 1)

        self.scrollingTimeEdit = QTimeEdit(self.gridLayoutWidget_3)
        self.scrollingTimeEdit.setObjectName(u"scrollingTimeEdit")
        self.scrollingTimeEdit.setEnabled(False)
        self.scrollingTimeEdit.setTime(QTime(0, 0, 10))

        self.gridLayout_3.addWidget(self.scrollingTimeEdit, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 4, 0, 1, 1)

        self.firstShownComboBox = QComboBox(self.gridLayoutWidget_3)
        self.firstShownComboBox.addItem("")
        self.firstShownComboBox.addItem("")
        self.firstShownComboBox.addItem("")
        self.firstShownComboBox.setObjectName(u"firstShownComboBox")

        self.gridLayout_3.addWidget(self.firstShownComboBox, 4, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget_3)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)

        self.scrollingRadioButton = QRadioButton(self.gridLayoutWidget_3)
        self.scrollingRadioButton.setObjectName(u"scrollingRadioButton")
        self.scrollingRadioButton.setChecked(False)

        self.gridLayout_3.addWidget(self.scrollingRadioButton, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 5, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.shownTimespan)

        self.applyDiagramSettings = QPushButton(self.verticalLayoutWidget)
        self.applyDiagramSettings.setObjectName(u"applyDiagramSettings")

        self.verticalLayout_2.addWidget(self.applyDiagramSettings)


        self.retranslateUi(diagramSettings)

        QMetaObject.connectSlotsByName(diagramSettings)
    # setupUi

    def retranslateUi(self, diagramSettings):
        diagramSettings.setWindowTitle(QCoreApplication.translate("diagramSettings", u"Diagram Settings", None))
        self.pressureAxes.setTitle(QCoreApplication.translate("diagramSettings", u"Pressure Axes", None))
        self.pressureSelfScaling.setText(QCoreApplication.translate("diagramSettings", u"Self-Scaling", None))
        self.pressureFixedValue.setText(QCoreApplication.translate("diagramSettings", u"Fixed-Value", None))
        self.pressureLineEdit.setText(QCoreApplication.translate("diagramSettings", u"300", None))
        self.temperatureAxes.setTitle(QCoreApplication.translate("diagramSettings", u"Temperature Axes", None))
        self.temperatureFixedValue.setText(QCoreApplication.translate("diagramSettings", u"Fixed-Value", None))
        self.temperatureSelfScaling.setText(QCoreApplication.translate("diagramSettings", u"Self-Scaling", None))
        self.temperatureLineEdit.setText(QCoreApplication.translate("diagramSettings", u"300", None))
        self.shownTimespan.setTitle(QCoreApplication.translate("diagramSettings", u"Timespan Shown", None))
        self.expandingRadioButton.setText(QCoreApplication.translate("diagramSettings", u"Expanding", None))
        self.scrollingTimeEdit.setDisplayFormat(QCoreApplication.translate("diagramSettings", u"mm:ss", None))
        self.label_2.setText(QCoreApplication.translate("diagramSettings", u"Starting with:", None))
        self.firstShownComboBox.setItemText(0, QCoreApplication.translate("diagramSettings", u"All", None))
        self.firstShownComboBox.setItemText(1, QCoreApplication.translate("diagramSettings", u"Lift-Off", None))
        self.firstShownComboBox.setItemText(2, QCoreApplication.translate("diagramSettings", u"SOE", None))

        self.label.setText(QCoreApplication.translate("diagramSettings", u"Timespan:", None))
        self.scrollingRadioButton.setText(QCoreApplication.translate("diagramSettings", u"Scrolling", None))
        self.applyDiagramSettings.setText(QCoreApplication.translate("diagramSettings", u"Apply", None))
    # retranslateUi

