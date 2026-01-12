# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_liveValuesWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_LiveValuesWidget(object):
    def setupUi(self, LiveValuesWidget):
        if not LiveValuesWidget.objectName():
            LiveValuesWidget.setObjectName(u"LiveValuesWidget")
        LiveValuesWidget.resize(480, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LiveValuesWidget.sizePolicy().hasHeightForWidth())
        LiveValuesWidget.setSizePolicy(sizePolicy)
        LiveValuesWidget.setMinimumSize(QSize(480, 720))
        LiveValuesWidget.setMaximumSize(QSize(480, 720))
        self.accumulatorTemperature = QLabel(LiveValuesWidget)
        self.accumulatorTemperature.setObjectName(u"accumulatorTemperature")
        self.accumulatorTemperature.setGeometry(QRect(40, 660, 51, 16))
        self.accumulatorTemperature.setFrameShape(QFrame.Shape.StyledPanel)
        self.accumulatorTemperature.setFrameShadow(QFrame.Shadow.Sunken)
        self.accumulatorTemperature.setLineWidth(5)
        self.accumulatorTemperature.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.coldJunctionTemperature = QLabel(LiveValuesWidget)
        self.coldJunctionTemperature.setObjectName(u"coldJunctionTemperature")
        self.coldJunctionTemperature.setGeometry(QRect(360, 660, 81, 20))
        self.coldJunctionTemperature.setFrameShape(QFrame.Shape.StyledPanel)
        self.coldJunctionTemperature.setFrameShadow(QFrame.Shadow.Sunken)
        self.coldJunctionTemperature.setLineWidth(5)
        self.coldJunctionTemperature.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.accumulatorPressure = QLabel(LiveValuesWidget)
        self.accumulatorPressure.setObjectName(u"accumulatorPressure")
        self.accumulatorPressure.setGeometry(QRect(320, 370, 71, 16))
        self.accumulatorPressure.setFrameShape(QFrame.Shape.StyledPanel)
        self.accumulatorPressure.setFrameShadow(QFrame.Shadow.Sunken)
        self.accumulatorPressure.setLineWidth(5)
        self.accumulatorPressure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzlePressure3 = QLabel(LiveValuesWidget)
        self.nozzlePressure3.setObjectName(u"nozzlePressure3")
        self.nozzlePressure3.setGeometry(QRect(10, 100, 71, 16))
        self.nozzlePressure3.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzlePressure3.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzlePressure3.setLineWidth(5)
        self.nozzlePressure3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzlePressure2 = QLabel(LiveValuesWidget)
        self.nozzlePressure2.setObjectName(u"nozzlePressure2")
        self.nozzlePressure2.setGeometry(QRect(10, 120, 71, 16))
        self.nozzlePressure2.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzlePressure2.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzlePressure2.setLineWidth(5)
        self.nozzlePressure2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzlePressure1 = QLabel(LiveValuesWidget)
        self.nozzlePressure1.setObjectName(u"nozzlePressure1")
        self.nozzlePressure1.setGeometry(QRect(10, 140, 71, 16))
        self.nozzlePressure1.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzlePressure1.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzlePressure1.setLineWidth(5)
        self.nozzlePressure1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzleTemperature3 = QLabel(LiveValuesWidget)
        self.nozzleTemperature3.setObjectName(u"nozzleTemperature3")
        self.nozzleTemperature3.setGeometry(QRect(420, 100, 51, 16))
        self.nozzleTemperature3.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzleTemperature3.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzleTemperature3.setLineWidth(5)
        self.nozzleTemperature3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzleTemperature2 = QLabel(LiveValuesWidget)
        self.nozzleTemperature2.setObjectName(u"nozzleTemperature2")
        self.nozzleTemperature2.setGeometry(QRect(420, 120, 51, 16))
        self.nozzleTemperature2.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzleTemperature2.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzleTemperature2.setLineWidth(5)
        self.nozzleTemperature2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.nozzleTemperature1 = QLabel(LiveValuesWidget)
        self.nozzleTemperature1.setObjectName(u"nozzleTemperature1")
        self.nozzleTemperature1.setGeometry(QRect(420, 140, 51, 16))
        self.nozzleTemperature1.setFrameShape(QFrame.Shape.StyledPanel)
        self.nozzleTemperature1.setFrameShadow(QFrame.Shadow.Sunken)
        self.nozzleTemperature1.setLineWidth(5)
        self.nozzleTemperature1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.chamberTemperature = QLabel(LiveValuesWidget)
        self.chamberTemperature.setObjectName(u"chamberTemperature")
        self.chamberTemperature.setGeometry(QRect(380, 270, 51, 16))
        self.chamberTemperature.setFrameShape(QFrame.Shape.StyledPanel)
        self.chamberTemperature.setFrameShadow(QFrame.Shadow.Sunken)
        self.chamberTemperature.setLineWidth(5)
        self.chamberTemperature.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.ambientPressure = QLabel(LiveValuesWidget)
        self.ambientPressure.setObjectName(u"ambientPressure")
        self.ambientPressure.setGeometry(QRect(360, 590, 81, 21))
        self.ambientPressure.setFrameShape(QFrame.Shape.StyledPanel)
        self.ambientPressure.setFrameShadow(QFrame.Shadow.Sunken)
        self.ambientPressure.setLineWidth(5)
        self.ambientPressure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.chamberPressure = QLabel(LiveValuesWidget)
        self.chamberPressure.setObjectName(u"chamberPressure")
        self.chamberPressure.setGeometry(QRect(70, 270, 71, 16))
        self.chamberPressure.setFrameShape(QFrame.Shape.StyledPanel)
        self.chamberPressure.setFrameShadow(QFrame.Shadow.Sunken)
        self.chamberPressure.setLineWidth(5)
        self.chamberPressure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.retranslateUi(LiveValuesWidget)

        QMetaObject.connectSlotsByName(LiveValuesWidget)
    # setupUi

    def retranslateUi(self, LiveValuesWidget):
        LiveValuesWidget.setWindowTitle(QCoreApplication.translate("LiveValuesWidget", u"Live Values Widget", None))
        self.accumulatorTemperature.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.coldJunctionTemperature.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.accumulatorPressure.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
        self.nozzlePressure3.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
        self.nozzlePressure2.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
        self.nozzlePressure1.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
        self.nozzleTemperature3.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.nozzleTemperature2.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.nozzleTemperature1.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.chamberTemperature.setText(QCoreApplication.translate("LiveValuesWidget", u"0 K", None))
        self.ambientPressure.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
        self.chamberPressure.setText(QCoreApplication.translate("LiveValuesWidget", u"0 Pa", None))
    # retranslateUi

