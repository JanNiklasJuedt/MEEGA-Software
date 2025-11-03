# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.resize(1366, 817)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.Germany))
        MainWindow.setIconSize(QSize(50, 50))
        MainWindow.setAnimated(False)
        self.actionFileLoad = QAction(MainWindow)
        self.actionFileLoad.setObjectName(u"actionFileLoad")
        self.actionFileSave_as = QAction(MainWindow)
        self.actionFileSave_as.setObjectName(u"actionFileSave_as")
        self.actionFileNew = QAction(MainWindow)
        self.actionFileNew.setObjectName(u"actionFileNew")
        self.actionResults = QAction(MainWindow)
        self.actionResults.setObjectName(u"actionResults")
        self.actionRestart = QAction(MainWindow)
        self.actionRestart.setObjectName(u"actionRestart")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionEnglish.setCheckable(True)
        self.actionEnglish.setChecked(True)
        self.actionEnglish.setText(u"English")
        self.actionEnglish.setIconText(u"English")
#if QT_CONFIG(tooltip)
        self.actionEnglish.setToolTip(u"English")
#endif // QT_CONFIG(tooltip)
        self.actionEnglish.setProperty(u"data", u"en")
        self.actionGerman = QAction(MainWindow)
        self.actionGerman.setObjectName(u"actionGerman")
        self.actionGerman.setCheckable(True)
        self.actionGerman.setText(u"Deutsch")
        self.actionGerman.setIconText(u"Deutsch")
#if QT_CONFIG(tooltip)
        self.actionGerman.setToolTip(u"Deutsch")
#endif // QT_CONFIG(tooltip)
        self.actionGerman.setProperty(u"data", u"de")
        self.actionExportHousholding = QAction(MainWindow)
        self.actionExportHousholding.setObjectName(u"actionExportHousholding")
        self.actionExportMeasurements = QAction(MainWindow)
        self.actionExportMeasurements.setObjectName(u"actionExportMeasurements")
        self.actionExportEverything = QAction(MainWindow)
        self.actionExportEverything.setObjectName(u"actionExportEverything")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionEstimated_Launch_Time = QAction(MainWindow)
        self.actionEstimated_Launch_Time.setObjectName(u"actionEstimated_Launch_Time")
        self.actionFlight_Mode = QAction(MainWindow)
        self.actionFlight_Mode.setObjectName(u"actionFlight_Mode")
        self.actionFlight_Mode.setCheckable(True)
        self.actionFlight_Mode.setChecked(True)
        self.actionTest_Mode = QAction(MainWindow)
        self.actionTest_Mode.setObjectName(u"actionTest_Mode")
        self.actionTest_Mode.setCheckable(True)
        self.actionControl_Panel = QAction(MainWindow)
        self.actionControl_Panel.setObjectName(u"actionControl_Panel")
        self.actionCalibration = QAction(MainWindow)
        self.actionCalibration.setObjectName(u"actionCalibration")
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionRetry = QAction(MainWindow)
        self.actionRetry.setObjectName(u"actionRetry")
        self.actionAutomatic = QAction(MainWindow)
        self.actionAutomatic.setObjectName(u"actionAutomatic")
        self.actionAutomatic.setCheckable(True)
        self.actionManual = QAction(MainWindow)
        self.actionManual.setObjectName(u"actionManual")
        self.actionManual.setCheckable(True)
        self.actionDisconnect = QAction(MainWindow)
        self.actionDisconnect.setObjectName(u"actionDisconnect")
        self.actionSelf_Scaling_Axes = QAction(MainWindow)
        self.actionSelf_Scaling_Axes.setObjectName(u"actionSelf_Scaling_Axes")
        self.actionDiagrams = QAction(MainWindow)
        self.actionDiagrams.setObjectName(u"actionDiagrams")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(30, 10, 30, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frame_time = QFrame(self.centralwidget)
        self.frame_time.setObjectName(u"frame_time")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_time.sizePolicy().hasHeightForWidth())
        self.frame_time.setSizePolicy(sizePolicy)
        self.frame_time.setMinimumSize(QSize(166, 0))
        self.frame_time.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.frame_time.setFrameShape(QFrame.Shape.Box)
        self.frame_time.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame_time.setLineWidth(1)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_time)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, -1, 10, -1)
        self.label_time = QLabel(self.frame_time)
        self.label_time.setObjectName(u"label_time")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_time.sizePolicy().hasHeightForWidth())
        self.label_time.setSizePolicy(sizePolicy1)
        self.label_time.setMinimumSize(QSize(66, 0))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.label_time.setFont(font1)
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_time)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.time_counter = QLabel(self.frame_time)
        self.time_counter.setObjectName(u"time_counter")
        sizePolicy1.setHeightForWidth(self.time_counter.sizePolicy().hasHeightForWidth())
        self.time_counter.setSizePolicy(sizePolicy1)
        self.time_counter.setMinimumSize(QSize(70, 0))
        self.time_counter.setFont(font1)
        self.time_counter.setText(u"00:00")

        self.horizontalLayout_5.addWidget(self.time_counter)


        self.horizontalLayout_6.addWidget(self.frame_time)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.connectionFrame = QFrame(self.centralwidget)
        self.connectionFrame.setObjectName(u"connectionFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.connectionFrame.sizePolicy().hasHeightForWidth())
        self.connectionFrame.setSizePolicy(sizePolicy2)
        self.connectionFrame.setMinimumSize(QSize(250, 70))
        self.connectionFrame.setBaseSize(QSize(0, 0))
        self.connectionFrame.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.connectionFrame.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.connectionFrame.setFrameShape(QFrame.Shape.Box)
        self.connectionFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_3 = QHBoxLayout(self.connectionFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.label_Connection = QLabel(self.connectionFrame)
        self.label_Connection.setObjectName(u"label_Connection")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.label_Connection.sizePolicy().hasHeightForWidth())
        self.label_Connection.setSizePolicy(sizePolicy3)
        self.label_Connection.setMinimumSize(QSize(0, 0))
        self.label_Connection.setFont(font1)
        self.label_Connection.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_Connection.setScaledContents(False)
        self.label_Connection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_Connection.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.horizontalLayout_3.addWidget(self.label_Connection)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.connectionLabel = QLabel(self.connectionFrame)
        self.connectionLabel.setObjectName(u"connectionLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.connectionLabel.sizePolicy().hasHeightForWidth())
        self.connectionLabel.setSizePolicy(sizePolicy4)
        self.connectionLabel.setMinimumSize(QSize(50, 50))
        self.connectionLabel.setFrameShape(QFrame.Shape.Panel)
        self.connectionLabel.setFrameShadow(QFrame.Shadow.Sunken)
        self.connectionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.connectionLabel)


        self.horizontalLayout_6.addWidget(self.connectionFrame)

        self.horizontalLayout_6.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.distancePlotGroupBox = QGroupBox(self.centralwidget)
        self.distancePlotGroupBox.setObjectName(u"distancePlotGroupBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(10)
        sizePolicy5.setHeightForWidth(self.distancePlotGroupBox.sizePolicy().hasHeightForWidth())
        self.distancePlotGroupBox.setSizePolicy(sizePolicy5)
        self.distancePlotGroupBox.setMinimumSize(QSize(250, 0))
        self.distancePlotGroupBox.setMaximumSize(QSize(16777215, 16777215))
        self.distancePlotGroupBox.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.verticalLayout.addWidget(self.distancePlotGroupBox)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_sensorstatus = QGroupBox(self.centralwidget)
        self.groupBox_sensorstatus.setObjectName(u"groupBox_sensorstatus")
        sizePolicy1.setHeightForWidth(self.groupBox_sensorstatus.sizePolicy().hasHeightForWidth())
        self.groupBox_sensorstatus.setSizePolicy(sizePolicy1)
        self.groupBox_sensorstatus.setMinimumSize(QSize(600, 0))
        self.groupBox_sensorstatus.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.groupBox_sensorstatus.setFlat(False)
        self.gridLayout_4 = QGridLayout(self.groupBox_sensorstatus)
        self.gridLayout_4.setSpacing(10)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_18 = QLabel(self.groupBox_sensorstatus)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_18, 5, 2, 1, 1)

        self.statusLabelTNozzle2 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTNozzle2.setObjectName(u"statusLabelTNozzle2")
        sizePolicy4.setHeightForWidth(self.statusLabelTNozzle2.sizePolicy().hasHeightForWidth())
        self.statusLabelTNozzle2.setSizePolicy(sizePolicy4)
        self.statusLabelTNozzle2.setMinimumSize(QSize(25, 25))
        self.statusLabelTNozzle2.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTNozzle2.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTNozzle2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTNozzle2, 4, 6, 1, 1)

        self.label_31 = QLabel(self.groupBox_sensorstatus)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_31, 3, 5, 1, 1)

        self.statusLabelTNozzle3 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTNozzle3.setObjectName(u"statusLabelTNozzle3")
        sizePolicy4.setHeightForWidth(self.statusLabelTNozzle3.sizePolicy().hasHeightForWidth())
        self.statusLabelTNozzle3.setSizePolicy(sizePolicy4)
        self.statusLabelTNozzle3.setMinimumSize(QSize(25, 25))
        self.statusLabelTNozzle3.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTNozzle3.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTNozzle3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTNozzle3, 5, 6, 1, 1)

        self.label_2 = QLabel(self.groupBox_sensorstatus)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)

        self.statusLabelTCompare = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTCompare.setObjectName(u"statusLabelTCompare")
        sizePolicy4.setHeightForWidth(self.statusLabelTCompare.sizePolicy().hasHeightForWidth())
        self.statusLabelTCompare.setSizePolicy(sizePolicy4)
        self.statusLabelTCompare.setMinimumSize(QSize(25, 25))
        self.statusLabelTCompare.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTCompare.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTCompare.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTCompare, 0, 6, 1, 1)

        self.label_11 = QLabel(self.groupBox_sensorstatus)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox_sensorstatus)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_30, 2, 5, 1, 1)

        self.label_temp_6 = QLabel(self.groupBox_sensorstatus)
        self.label_temp_6.setObjectName(u"label_temp_6")
        self.label_temp_6.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_temp_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_temp_6, 1, 2, 1, 1)

        self.label_29 = QLabel(self.groupBox_sensorstatus)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_29, 1, 5, 1, 1)

        self.statusLabelTChip = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTChip.setObjectName(u"statusLabelTChip")
        sizePolicy4.setHeightForWidth(self.statusLabelTChip.sizePolicy().hasHeightForWidth())
        self.statusLabelTChip.setSizePolicy(sizePolicy4)
        self.statusLabelTChip.setMinimumSize(QSize(25, 25))
        self.statusLabelTChip.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTChip.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTChip.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTChip, 2, 1, 1, 1)

        self.statusLabelMainboard = QLabel(self.groupBox_sensorstatus)
        self.statusLabelMainboard.setObjectName(u"statusLabelMainboard")
        sizePolicy4.setHeightForWidth(self.statusLabelMainboard.sizePolicy().hasHeightForWidth())
        self.statusLabelMainboard.setSizePolicy(sizePolicy4)
        self.statusLabelMainboard.setMinimumSize(QSize(25, 25))
        self.statusLabelMainboard.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelMainboard.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelMainboard.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelMainboard, 0, 1, 1, 1)

        self.statusLabelSOE = QLabel(self.groupBox_sensorstatus)
        self.statusLabelSOE.setObjectName(u"statusLabelSOE")
        sizePolicy4.setHeightForWidth(self.statusLabelSOE.sizePolicy().hasHeightForWidth())
        self.statusLabelSOE.setSizePolicy(sizePolicy4)
        self.statusLabelSOE.setMinimumSize(QSize(25, 25))
        self.statusLabelSOE.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelSOE.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelSOE.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelSOE, 1, 8, 1, 1)

        self.label_temp_2 = QLabel(self.groupBox_sensorstatus)
        self.label_temp_2.setObjectName(u"label_temp_2")
        self.label_temp_2.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_temp_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_temp_2, 0, 0, 1, 1)

        self.label_temp_7 = QLabel(self.groupBox_sensorstatus)
        self.label_temp_7.setObjectName(u"label_temp_7")
        self.label_temp_7.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_temp_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_temp_7, 0, 5, 1, 1)

        self.label_13 = QLabel(self.groupBox_sensorstatus)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_13, 5, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_sensorstatus)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_16, 3, 2, 1, 1)

        self.statusLabelPNozzle3 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPNozzle3.setObjectName(u"statusLabelPNozzle3")
        sizePolicy4.setHeightForWidth(self.statusLabelPNozzle3.sizePolicy().hasHeightForWidth())
        self.statusLabelPNozzle3.setSizePolicy(sizePolicy4)
        self.statusLabelPNozzle3.setMinimumSize(QSize(25, 25))
        self.statusLabelPNozzle3.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPNozzle3.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPNozzle3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPNozzle3, 5, 4, 1, 1)

        self.statusLabelPAccumulator = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPAccumulator.setObjectName(u"statusLabelPAccumulator")
        sizePolicy4.setHeightForWidth(self.statusLabelPAccumulator.sizePolicy().hasHeightForWidth())
        self.statusLabelPAccumulator.setSizePolicy(sizePolicy4)
        self.statusLabelPAccumulator.setMinimumSize(QSize(25, 25))
        self.statusLabelPAccumulator.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPAccumulator.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPAccumulator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPAccumulator, 2, 4, 1, 1)

        self.statusLabelTAccumulator = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTAccumulator.setObjectName(u"statusLabelTAccumulator")
        sizePolicy4.setHeightForWidth(self.statusLabelTAccumulator.sizePolicy().hasHeightForWidth())
        self.statusLabelTAccumulator.setSizePolicy(sizePolicy4)
        self.statusLabelTAccumulator.setMinimumSize(QSize(25, 25))
        self.statusLabelTAccumulator.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTAccumulator.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTAccumulator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTAccumulator, 2, 6, 1, 1)

        self.statusLabelLiftOff = QLabel(self.groupBox_sensorstatus)
        self.statusLabelLiftOff.setObjectName(u"statusLabelLiftOff")
        sizePolicy4.setHeightForWidth(self.statusLabelLiftOff.sizePolicy().hasHeightForWidth())
        self.statusLabelLiftOff.setSizePolicy(sizePolicy4)
        self.statusLabelLiftOff.setMinimumSize(QSize(25, 25))
        self.statusLabelLiftOff.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelLiftOff.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelLiftOff.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelLiftOff, 0, 8, 1, 1)

        self.statusLabelPNozzle1 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPNozzle1.setObjectName(u"statusLabelPNozzle1")
        sizePolicy4.setHeightForWidth(self.statusLabelPNozzle1.sizePolicy().hasHeightForWidth())
        self.statusLabelPNozzle1.setSizePolicy(sizePolicy4)
        self.statusLabelPNozzle1.setMinimumSize(QSize(25, 25))
        self.statusLabelPNozzle1.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPNozzle1.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPNozzle1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPNozzle1, 3, 4, 1, 1)

        self.line = QFrame(self.groupBox_sensorstatus)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line, 3, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_sensorstatus)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_12, 4, 0, 1, 1)

        self.statusLabelPChip = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPChip.setObjectName(u"statusLabelPChip")
        sizePolicy4.setHeightForWidth(self.statusLabelPChip.sizePolicy().hasHeightForWidth())
        self.statusLabelPChip.setSizePolicy(sizePolicy4)
        self.statusLabelPChip.setMinimumSize(QSize(25, 25))
        self.statusLabelPChip.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPChip.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPChip.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPChip, 1, 1, 1, 1)

        self.label_32 = QLabel(self.groupBox_sensorstatus)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_32, 4, 5, 1, 1)

        self.label_33 = QLabel(self.groupBox_sensorstatus)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_33, 5, 5, 1, 1)

        self.label_9 = QLabel(self.groupBox_sensorstatus)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_9, 1, 7, 1, 1)

        self.label_14 = QLabel(self.groupBox_sensorstatus)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_14, 2, 2, 1, 1)

        self.statusLabelTNozzle1 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTNozzle1.setObjectName(u"statusLabelTNozzle1")
        sizePolicy4.setHeightForWidth(self.statusLabelTNozzle1.sizePolicy().hasHeightForWidth())
        self.statusLabelTNozzle1.setSizePolicy(sizePolicy4)
        self.statusLabelTNozzle1.setMinimumSize(QSize(25, 25))
        self.statusLabelTNozzle1.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTNozzle1.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTNozzle1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTNozzle1, 3, 6, 1, 1)

        self.statusLabelTReservoir = QLabel(self.groupBox_sensorstatus)
        self.statusLabelTReservoir.setObjectName(u"statusLabelTReservoir")
        sizePolicy4.setHeightForWidth(self.statusLabelTReservoir.sizePolicy().hasHeightForWidth())
        self.statusLabelTReservoir.setSizePolicy(sizePolicy4)
        self.statusLabelTReservoir.setMinimumSize(QSize(25, 25))
        self.statusLabelTReservoir.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelTReservoir.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelTReservoir.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelTReservoir, 1, 6, 1, 1)

        self.label_15 = QLabel(self.groupBox_sensorstatus)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_15, 0, 2, 1, 1)

        self.statusLabelValve = QLabel(self.groupBox_sensorstatus)
        self.statusLabelValve.setObjectName(u"statusLabelValve")
        sizePolicy4.setHeightForWidth(self.statusLabelValve.sizePolicy().hasHeightForWidth())
        self.statusLabelValve.setSizePolicy(sizePolicy4)
        self.statusLabelValve.setMinimumSize(QSize(25, 25))
        self.statusLabelValve.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelValve.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelValve.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelValve, 5, 1, 1, 1)

        self.statusLabelPAmbient = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPAmbient.setObjectName(u"statusLabelPAmbient")
        sizePolicy4.setHeightForWidth(self.statusLabelPAmbient.sizePolicy().hasHeightForWidth())
        self.statusLabelPAmbient.setSizePolicy(sizePolicy4)
        self.statusLabelPAmbient.setMinimumSize(QSize(25, 25))
        self.statusLabelPAmbient.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPAmbient.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPAmbient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPAmbient, 0, 4, 1, 1)

        self.statusLabelServo = QLabel(self.groupBox_sensorstatus)
        self.statusLabelServo.setObjectName(u"statusLabelServo")
        sizePolicy4.setHeightForWidth(self.statusLabelServo.sizePolicy().hasHeightForWidth())
        self.statusLabelServo.setSizePolicy(sizePolicy4)
        self.statusLabelServo.setMinimumSize(QSize(25, 25))
        self.statusLabelServo.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelServo.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelServo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelServo, 4, 1, 1, 1)

        self.label_17 = QLabel(self.groupBox_sensorstatus)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_17, 4, 2, 1, 1)

        self.statusLabelPReservoir = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPReservoir.setObjectName(u"statusLabelPReservoir")
        sizePolicy4.setHeightForWidth(self.statusLabelPReservoir.sizePolicy().hasHeightForWidth())
        self.statusLabelPReservoir.setSizePolicy(sizePolicy4)
        self.statusLabelPReservoir.setMinimumSize(QSize(25, 25))
        self.statusLabelPReservoir.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPReservoir.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPReservoir.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPReservoir, 1, 4, 1, 1)

        self.statusLabelLED = QLabel(self.groupBox_sensorstatus)
        self.statusLabelLED.setObjectName(u"statusLabelLED")
        sizePolicy4.setHeightForWidth(self.statusLabelLED.sizePolicy().hasHeightForWidth())
        self.statusLabelLED.setSizePolicy(sizePolicy4)
        self.statusLabelLED.setMinimumSize(QSize(25, 25))
        self.statusLabelLED.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelLED.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelLED.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelLED, 2, 8, 1, 1)

        self.label_37 = QLabel(self.groupBox_sensorstatus)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_37, 0, 7, 1, 1)

        self.label_10 = QLabel(self.groupBox_sensorstatus)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_10, 2, 7, 1, 1)

        self.statusLabelPNozzle2 = QLabel(self.groupBox_sensorstatus)
        self.statusLabelPNozzle2.setObjectName(u"statusLabelPNozzle2")
        sizePolicy4.setHeightForWidth(self.statusLabelPNozzle2.sizePolicy().hasHeightForWidth())
        self.statusLabelPNozzle2.setSizePolicy(sizePolicy4)
        self.statusLabelPNozzle2.setMinimumSize(QSize(25, 25))
        self.statusLabelPNozzle2.setFrameShape(QFrame.Shape.NoFrame)
        self.statusLabelPNozzle2.setFrameShadow(QFrame.Shadow.Sunken)
        self.statusLabelPNozzle2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.statusLabelPNozzle2, 4, 4, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_sensorstatus)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_8)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 0, 0)
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(1)
        sizePolicy6.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy6)
        self.label_logo.setMinimumSize(QSize(200, 200))
        self.label_logo.setMaximumSize(QSize(200, 200))
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_logo.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_3.addWidget(self.label_logo)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.label_mode = QLabel(self.centralwidget)
        self.label_mode.setObjectName(u"label_mode")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_mode.sizePolicy().hasHeightForWidth())
        self.label_mode.setSizePolicy(sizePolicy7)
        self.label_mode.setFont(font1)
        self.label_mode.setScaledContents(True)
        self.label_mode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_mode)

        self.verticalLayout_3.setStretch(0, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy8)
        self.groupBox_2.setMinimumSize(QSize(200, 0))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 10, 0, 0)
        self.treeWidget = QTreeWidget(self.groupBox_2)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem.setCheckState(0, Qt.Checked);
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem1.setCheckState(0, Qt.Checked);
        __qtreewidgetitem2 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem2.setCheckState(0, Qt.Checked);
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem3.setCheckState(0, Qt.Checked);
        __qtreewidgetitem4 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem4.setCheckState(0, Qt.Checked);
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem5.setCheckState(0, Qt.Checked);
        __qtreewidgetitem6 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem6.setCheckState(0, Qt.Checked);
        __qtreewidgetitem7 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem7.setCheckState(0, Qt.Checked);
        __qtreewidgetitem8 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem8.setCheckState(0, Qt.Checked);
        __qtreewidgetitem9 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem9.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem9.setCheckState(0, Qt.Checked);
        __qtreewidgetitem10 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem10.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem10.setCheckState(0, Qt.Checked);
        __qtreewidgetitem11 = QTreeWidgetItem(__qtreewidgetitem10)
        __qtreewidgetitem11.setCheckState(0, Qt.Checked);
        __qtreewidgetitem12 = QTreeWidgetItem(__qtreewidgetitem10)
        __qtreewidgetitem12.setCheckState(0, Qt.Checked);
        __qtreewidgetitem13 = QTreeWidgetItem(__qtreewidgetitem10)
        __qtreewidgetitem13.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem13.setCheckState(0, Qt.Checked);
        __qtreewidgetitem14 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem14.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem14.setCheckState(0, Qt.Checked);
        __qtreewidgetitem15 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem15.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem15.setCheckState(0, Qt.Checked);
        __qtreewidgetitem16 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem16.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem16.setCheckState(0, Qt.Checked);
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy9)
        self.treeWidget.setMinimumSize(QSize(180, 300))
        self.treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.treeWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeWidget.setProperty(u"showDropIndicator", True)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setProperty(u"showSortIndicator", False)

        self.verticalLayout_5.addWidget(self.treeWidget)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.timePlotGroupBox = QGroupBox(self.centralwidget)
        self.timePlotGroupBox.setObjectName(u"timePlotGroupBox")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy10.setHorizontalStretch(3)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.timePlotGroupBox.sizePolicy().hasHeightForWidth())
        self.timePlotGroupBox.setSizePolicy(sizePolicy10)
        self.timePlotGroupBox.setMinimumSize(QSize(600, 300))
        self.timePlotGroupBox.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.verticalLayout_4.addWidget(self.timePlotGroupBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.horizontalLayout_4.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)

        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.layout_progressbars = QGridLayout()
        self.layout_progressbars.setObjectName(u"layout_progressbars")
        self.layout_progressbars.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.layout_progressbars.setHorizontalSpacing(0)
        self.layout_progressbars.setVerticalSpacing(10)
        self.layout_progressbars.setContentsMargins(0, -1, 0, -1)
        self.label_SODS = QLabel(self.centralwidget)
        self.label_SODS.setObjectName(u"label_SODS")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.label_SODS.sizePolicy().hasHeightForWidth())
        self.label_SODS.setSizePolicy(sizePolicy11)
        self.label_SODS.setMinimumSize(QSize(127, 0))
        self.label_SODS.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_SODS.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_SODS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_SODS, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_progressbars.addItem(self.horizontalSpacer_4, 0, 7, 1, 1)

        self.label_SD = QLabel(self.centralwidget)
        self.label_SD.setObjectName(u"label_SD")
        sizePolicy1.setHeightForWidth(self.label_SD.sizePolicy().hasHeightForWidth())
        self.label_SD.setSizePolicy(sizePolicy1)
        self.label_SD.setMinimumSize(QSize(97, 0))
        self.label_SD.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_SD.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_SD, 1, 8, 1, 1)

        self.progressBar_SODS = QProgressBar(self.centralwidget)
        self.progressBar_SODS.setObjectName(u"progressBar_SODS")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy12.setHorizontalStretch(5)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.progressBar_SODS.sizePolicy().hasHeightForWidth())
        self.progressBar_SODS.setSizePolicy(sizePolicy12)
        self.progressBar_SODS.setMinimumSize(QSize(50, 0))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        font2.setKerning(True)
        self.progressBar_SODS.setFont(font2)
        self.progressBar_SODS.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_SODS.setMinimum(0)
        self.progressBar_SODS.setValue(100)
        self.progressBar_SODS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.progressBar_SODS, 0, 4, 1, 1)

        self.progressBar_PF = QProgressBar(self.centralwidget)
        self.progressBar_PF.setObjectName(u"progressBar_PF")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy13.setHorizontalStretch(1)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.progressBar_PF.sizePolicy().hasHeightForWidth())
        self.progressBar_PF.setSizePolicy(sizePolicy13)
        self.progressBar_PF.setMinimumSize(QSize(75, 0))
        self.progressBar_PF.setFont(font2)
        self.progressBar_PF.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_PF.setValue(0)
        self.progressBar_PF.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.progressBar_PF, 0, 0, 1, 1)

        self.progressBar_LO = QProgressBar(self.centralwidget)
        self.progressBar_LO.setObjectName(u"progressBar_LO")
        sizePolicy13.setHeightForWidth(self.progressBar_LO.sizePolicy().hasHeightForWidth())
        self.progressBar_LO.setSizePolicy(sizePolicy13)
        self.progressBar_LO.setMinimumSize(QSize(75, 0))
        self.progressBar_LO.setFont(font2)
        self.progressBar_LO.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_LO.setValue(100)
        self.progressBar_LO.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar_LO.setTextVisible(True)

        self.layout_progressbars.addWidget(self.progressBar_LO, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.layout_progressbars.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.layout_progressbars.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.label_LO = QLabel(self.centralwidget)
        self.label_LO.setObjectName(u"label_LO")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.label_LO.sizePolicy().hasHeightForWidth())
        self.label_LO.setSizePolicy(sizePolicy14)
        self.label_LO.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_LO.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_LO, 1, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_SOE = QLabel(self.centralwidget)
        self.label_SOE.setObjectName(u"label_SOE")
        sizePolicy4.setHeightForWidth(self.label_SOE.sizePolicy().hasHeightForWidth())
        self.label_SOE.setSizePolicy(sizePolicy4)
        self.label_SOE.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.horizontalLayout.addWidget(self.label_SOE)

        self.label_EOE = QLabel(self.centralwidget)
        self.label_EOE.setObjectName(u"label_EOE")
        sizePolicy14.setHeightForWidth(self.label_EOE.sizePolicy().hasHeightForWidth())
        self.label_EOE.setSizePolicy(sizePolicy14)
        self.label_EOE.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_EOE.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_EOE)


        self.layout_progressbars.addLayout(self.horizontalLayout, 1, 6, 1, 1)

        self.progressBar_SD = QProgressBar(self.centralwidget)
        self.progressBar_SD.setObjectName(u"progressBar_SD")
        sizePolicy13.setHeightForWidth(self.progressBar_SD.sizePolicy().hasHeightForWidth())
        self.progressBar_SD.setSizePolicy(sizePolicy13)
        self.progressBar_SD.setMinimumSize(QSize(75, 0))
        self.progressBar_SD.setBaseSize(QSize(97, 0))
        self.progressBar_SD.setFont(font2)
        self.progressBar_SD.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_SD.setValue(100)
        self.progressBar_SD.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar_SD.setTextVisible(False)

        self.layout_progressbars.addWidget(self.progressBar_SD, 0, 8, 1, 1)

        self.progressBar_SOE = QProgressBar(self.centralwidget)
        self.progressBar_SOE.setObjectName(u"progressBar_SOE")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy15.setHorizontalStretch(20)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.progressBar_SOE.sizePolicy().hasHeightForWidth())
        self.progressBar_SOE.setSizePolicy(sizePolicy15)
        self.progressBar_SOE.setMinimumSize(QSize(100, 0))
        self.progressBar_SOE.setFont(font2)
        self.progressBar_SOE.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_SOE.setValue(24)
        self.progressBar_SOE.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.progressBar_SOE, 0, 6, 1, 1)

        self.label_PF = QLabel(self.centralwidget)
        self.label_PF.setObjectName(u"label_PF")
        sizePolicy14.setHeightForWidth(self.label_PF.sizePolicy().hasHeightForWidth())
        self.label_PF.setSizePolicy(sizePolicy14)
        self.label_PF.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_PF.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_PF, 1, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.layout_progressbars.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.layout_progressbars, 1, 0, 1, 2)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 1366, 23))
        self.menubar.setFont(font)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName(u"menuExport")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuLanguage = QMenu(self.menuSettings)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuConnection = QMenu(self.menuSettings)
        self.menuConnection.setObjectName(u"menuConnection")
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        self.menuSetup = QMenu(self.menubar)
        self.menuSetup.setObjectName(u"menuSetup")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetup.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionFileNew)
        self.menuFile.addAction(self.actionFileLoad)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFileSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionResults)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuExport.addAction(self.actionExportHousholding)
        self.menuExport.addAction(self.actionExportMeasurements)
        self.menuExport.addAction(self.actionExportEverything)
        self.menuSettings.addAction(self.menuLanguage.menuAction())
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.menuConnection.menuAction())
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionDiagrams)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionGerman)
        self.menuConnection.addAction(self.actionConnect)
        self.menuConnection.addAction(self.actionRetry)
        self.menuConnection.addSeparator()
        self.menuConnection.addAction(self.actionAutomatic)
        self.menuConnection.addAction(self.actionManual)
        self.menuConnection.addSeparator()
        self.menuConnection.addAction(self.actionDisconnect)
        self.menuStart.addAction(self.actionTest_Mode)
        self.menuStart.addAction(self.actionFlight_Mode)
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionControl_Panel)
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionDocumentation)
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionRestart)
        self.menuStart.addAction(self.actionQuit)
        self.menuSetup.addAction(self.actionCalibration)
        self.menuSetup.addSeparator()
        self.menuSetup.addAction(self.actionEstimated_Launch_Time)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MEEGA - Ground Station", None))
        self.actionFileLoad.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionFileSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionFileNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionResults.setText(QCoreApplication.translate("MainWindow", u"Results", None))
#if QT_CONFIG(shortcut)
        self.actionResults.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionRestart.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.actionExportHousholding.setText(QCoreApplication.translate("MainWindow", u"Housholding", None))
        self.actionExportMeasurements.setText(QCoreApplication.translate("MainWindow", u"Measurements", None))
        self.actionExportEverything.setText(QCoreApplication.translate("MainWindow", u"Full Dataset", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionEstimated_Launch_Time.setText(QCoreApplication.translate("MainWindow", u"Estimated Launch Time", None))
        self.actionFlight_Mode.setText(QCoreApplication.translate("MainWindow", u"Flight Mode", None))
#if QT_CONFIG(shortcut)
        self.actionFlight_Mode.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.actionTest_Mode.setText(QCoreApplication.translate("MainWindow", u"Test Mode", None))
#if QT_CONFIG(shortcut)
        self.actionTest_Mode.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionControl_Panel.setText(QCoreApplication.translate("MainWindow", u"Control Panel", None))
        self.actionCalibration.setText(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.actionRetry.setText(QCoreApplication.translate("MainWindow", u"Reconnect", None))
        self.actionAutomatic.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.actionSelf_Scaling_Axes.setText(QCoreApplication.translate("MainWindow", u"Self-Scaling Axes", None))
        self.actionDiagrams.setText(QCoreApplication.translate("MainWindow", u"Diagrams", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"T -", None))
        self.label_Connection.setText(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.connectionLabel.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.distancePlotGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Graph over Distance", None))
        self.groupBox_sensorstatus.setTitle(QCoreApplication.translate("MainWindow", u"System Status", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"P Nozzle 3", None))
        self.statusLabelTNozzle2.setText("")
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"T Nozzle 1", None))
        self.statusLabelTNozzle3.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"P Chip", None))
        self.statusLabelTCompare.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"T Chip", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"T Chamber", None))
        self.label_temp_6.setText(QCoreApplication.translate("MainWindow", u"P Accumulator", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"T Accumulator", None))
        self.statusLabelTChip.setText("")
        self.statusLabelMainboard.setText("")
        self.statusLabelSOE.setText("")
        self.label_temp_2.setText(QCoreApplication.translate("MainWindow", u"Mainboard", None))
        self.label_temp_7.setText(QCoreApplication.translate("MainWindow", u"T Compare", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Valve", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"P Nozzle 1", None))
        self.statusLabelPNozzle3.setText("")
        self.statusLabelPAccumulator.setText("")
        self.statusLabelTAccumulator.setText("")
        self.statusLabelLiftOff.setText("")
        self.statusLabelPNozzle1.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Servo", None))
        self.statusLabelPChip.setText("")
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"T Nozzle 2", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"T Nozzle 3", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Start of Experiment", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"P Chamber", None))
        self.statusLabelTNozzle1.setText("")
        self.statusLabelTReservoir.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"P Ambient", None))
        self.statusLabelValve.setText("")
        self.statusLabelPAmbient.setText("")
        self.statusLabelServo.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"P Nozzle 2", None))
        self.statusLabelPReservoir.setText("")
        self.statusLabelLED.setText("")
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Lift-Off", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"LEDs", None))
        self.statusLabelPNozzle2.setText("")
        self.label_logo.setText("")
        self.label_mode.setText(QCoreApplication.translate("MainWindow", u"Flight Mode", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Sensor Selection", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Sensors", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"All", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Pressure", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Nozzle", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem3.child(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem3.child(2)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem2.child(1)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"Chamber", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem2.child(2)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"Accumulator", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem2.child(3)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"Ambient", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"Temperature", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem10.child(0)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"Nozzle", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem11.child(0)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem11.child(1)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem11.child(2)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem10.child(1)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"Chamber", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem10.child(2)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"Accumulator", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem10.child(3)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("MainWindow", u"Compare", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.timePlotGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Graph over Time", None))
        self.label_SODS.setText(QCoreApplication.translate("MainWindow", u"Experiment Preparation", None))
        self.label_SD.setText(QCoreApplication.translate("MainWindow", u"Shutdown", None))
        self.progressBar_SODS.setFormat(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.progressBar_PF.setFormat(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.progressBar_LO.setFormat(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label_LO.setText(QCoreApplication.translate("MainWindow", u"Lift Off", None))
        self.label_SOE.setText(QCoreApplication.translate("MainWindow", u"Start of Experiment", None))
        self.label_EOE.setText(QCoreApplication.translate("MainWindow", u"End of Experiment", None))
        self.progressBar_SD.setFormat(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.progressBar_SOE.setFormat(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label_PF.setText(QCoreApplication.translate("MainWindow", u"Pre-Flight", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.menuConnection.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuSetup.setTitle(QCoreApplication.translate("MainWindow", u"Setup", None))
    # retranslateUi

