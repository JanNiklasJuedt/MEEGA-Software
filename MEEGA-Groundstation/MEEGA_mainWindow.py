# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.resize(1315, 750)
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
        MainWindow.setAnimated(False)
        self.actionFileLoad = QAction(MainWindow)
        self.actionFileLoad.setObjectName(u"actionFileLoad")
        self.actionFileSave_as = QAction(MainWindow)
        self.actionFileSave_as.setObjectName(u"actionFileSave_as")
        self.actionFileNew = QAction(MainWindow)
        self.actionFileNew.setObjectName(u"actionFileNew")
        self.actionResults = QAction(MainWindow)
        self.actionResults.setObjectName(u"actionResults")
        self.actionRetry = QAction(MainWindow)
        self.actionRetry.setObjectName(u"actionRetry")
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
#if QT_CONFIG(shortcut)
        self.actionConnect.setShortcut(u"F8")
#endif // QT_CONFIG(shortcut)
        self.actionDisconnect = QAction(MainWindow)
        self.actionDisconnect.setObjectName(u"actionDisconnect")
        self.actionRestart = QAction(MainWindow)
        self.actionRestart.setObjectName(u"actionRestart")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionConnectionAutomatic = QAction(MainWindow)
        self.actionConnectionAutomatic.setObjectName(u"actionConnectionAutomatic")
        self.actionConnectionAutomatic.setCheckable(True)
        self.actionConnectionAutomatic.setChecked(True)
        self.actionConnectionAutomatic.setProperty(u"data", 10)
        self.actionConnectionManual = QAction(MainWindow)
        self.actionConnectionManual.setObjectName(u"actionConnectionManual")
        self.actionConnectionManual.setCheckable(True)
        self.actionConnectionManual.setProperty(u"data", 11)
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
        self.actionModeRecording = QAction(MainWindow)
        self.actionModeRecording.setObjectName(u"actionModeRecording")
        self.actionModeRecording.setCheckable(True)
        self.actionModeRecording.setChecked(True)
        self.actionModeRecording.setProperty(u"data", 2)
        self.actionModeReplaying = QAction(MainWindow)
        self.actionModeReplaying.setObjectName(u"actionModeReplaying")
        self.actionModeReplaying.setCheckable(True)
        self.actionModeReplaying.setProperty(u"data", 3)
        self.actionModeTesting = QAction(MainWindow)
        self.actionModeTesting.setObjectName(u"actionModeTesting")
        self.actionModeTesting.setCheckable(True)
        self.actionModeTesting.setProperty(u"data", 1)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionLog = QAction(MainWindow)
        self.actionLog.setObjectName(u"actionLog")
        self.actionaloha = QAction(MainWindow)
        self.actionaloha.setObjectName(u"actionaloha")
        self.actionTesting = QAction(MainWindow)
        self.actionTesting.setObjectName(u"actionTesting")
        self.actionFlying = QAction(MainWindow)
        self.actionFlying.setObjectName(u"actionFlying")
        self.actionReplaying = QAction(MainWindow)
        self.actionReplaying.setObjectName(u"actionReplaying")
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
        self.connectionFrame = QFrame(self.centralwidget)
        self.connectionFrame.setObjectName(u"connectionFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.connectionFrame.sizePolicy().hasHeightForWidth())
        self.connectionFrame.setSizePolicy(sizePolicy)
        self.connectionFrame.setMinimumSize(QSize(250, 70))
        self.connectionFrame.setBaseSize(QSize(0, 0))
        self.connectionFrame.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.connectionFrame.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.connectionFrame.setFrameShape(QFrame.Shape.Box)
        self.connectionFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.connectionFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.label_Connection = QLabel(self.connectionFrame)
        self.label_Connection.setObjectName(u"label_Connection")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.label_Connection.sizePolicy().hasHeightForWidth())
        self.label_Connection.setSizePolicy(sizePolicy1)
        self.label_Connection.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.label_Connection.setFont(font1)
        self.label_Connection.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_Connection.setScaledContents(False)
        self.label_Connection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_Connection.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.horizontalLayout_3.addWidget(self.label_Connection)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.frame_2 = QFrame(self.connectionFrame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setMinimumSize(QSize(50, 50))
        self.frame_2.setFrameShape(QFrame.Shape.Panel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.frame_2)


        self.horizontalLayout_6.addWidget(self.connectionFrame)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.frame_time = QFrame(self.centralwidget)
        self.frame_time.setObjectName(u"frame_time")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_time.sizePolicy().hasHeightForWidth())
        self.frame_time.setSizePolicy(sizePolicy3)
        self.frame_time.setMinimumSize(QSize(166, 0))
        self.frame_time.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.frame_time.setFrameShape(QFrame.Shape.Box)
        self.frame_time.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_time.setLineWidth(1)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_time)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, -1, 10, -1)
        self.label_time = QLabel(self.frame_time)
        self.label_time.setObjectName(u"label_time")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_time.sizePolicy().hasHeightForWidth())
        self.label_time.setSizePolicy(sizePolicy4)
        self.label_time.setMinimumSize(QSize(66, 0))
        self.label_time.setFont(font1)
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_time)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.time_counter = QLabel(self.frame_time)
        self.time_counter.setObjectName(u"time_counter")
        self.time_counter.setFont(font1)
        self.time_counter.setText(u"00:00")

        self.horizontalLayout_5.addWidget(self.time_counter)


        self.horizontalLayout_6.addWidget(self.frame_time)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.distancePlotFrame = QFrame(self.centralwidget)
        self.distancePlotFrame.setObjectName(u"distancePlotFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(10)
        sizePolicy5.setHeightForWidth(self.distancePlotFrame.sizePolicy().hasHeightForWidth())
        self.distancePlotFrame.setSizePolicy(sizePolicy5)
        self.distancePlotFrame.setMinimumSize(QSize(250, 0))
        self.distancePlotFrame.setMaximumSize(QSize(16777215, 16777215))
        self.distancePlotFrame.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.distancePlotFrame.setFrameShape(QFrame.Shape.Box)
        self.distancePlotFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.label_temp_1 = QLabel(self.distancePlotFrame)
        self.label_temp_1.setObjectName(u"label_temp_1")
        self.label_temp_1.setGeometry(QRect(40, 60, 121, 16))
        self.label_temp_1.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.verticalLayout.addWidget(self.distancePlotFrame)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_sensorstatus = QFrame(self.centralwidget)
        self.frame_sensorstatus.setObjectName(u"frame_sensorstatus")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_sensorstatus.sizePolicy().hasHeightForWidth())
        self.frame_sensorstatus.setSizePolicy(sizePolicy6)
        self.frame_sensorstatus.setMinimumSize(QSize(100, 0))
        self.frame_sensorstatus.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.frame_sensorstatus.setFrameShape(QFrame.Shape.Box)
        self.frame_sensorstatus.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_4 = QGridLayout(self.frame_sensorstatus)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_temp_4 = QLabel(self.frame_sensorstatus)
        self.label_temp_4.setObjectName(u"label_temp_4")
        self.label_temp_4.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.gridLayout_4.addWidget(self.label_temp_4, 2, 0, 1, 1)

        self.label_temp_2 = QLabel(self.frame_sensorstatus)
        self.label_temp_2.setObjectName(u"label_temp_2")
        self.label_temp_2.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.gridLayout_4.addWidget(self.label_temp_2, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 3, 0, 1, 1)

        self.frame_11 = QFrame(self.frame_sensorstatus)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy2.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy2)
        self.frame_11.setMinimumSize(QSize(20, 20))
        self.frame_11.setFrameShape(QFrame.Shape.Panel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.frame_11, 2, 1, 1, 1)

        self.label_temp_6 = QLabel(self.frame_sensorstatus)
        self.label_temp_6.setObjectName(u"label_temp_6")
        self.label_temp_6.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.gridLayout_4.addWidget(self.label_temp_6, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 3, 6, 1, 1)

        self.frame_9 = QFrame(self.frame_sensorstatus)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy2.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy2)
        self.frame_9.setMinimumSize(QSize(20, 20))
        self.frame_9.setFrameShape(QFrame.Shape.Panel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.frame_9, 0, 1, 1, 1)

        self.label_temp_7 = QLabel(self.frame_sensorstatus)
        self.label_temp_7.setObjectName(u"label_temp_7")
        self.label_temp_7.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.gridLayout_4.addWidget(self.label_temp_7, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_sensorstatus)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_sensorstatus)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy2.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy2)
        self.frame_10.setMinimumSize(QSize(20, 20))
        self.frame_10.setFrameShape(QFrame.Shape.Panel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.frame_10, 1, 1, 1, 1)

        self.frame_12 = QFrame(self.frame_sensorstatus)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy2.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy2)
        self.frame_12.setMinimumSize(QSize(20, 20))
        self.frame_12.setFrameShape(QFrame.Shape.Panel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.frame_12, 0, 3, 1, 1)

        self.frame_13 = QFrame(self.frame_sensorstatus)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy2.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy2)
        self.frame_13.setMinimumSize(QSize(20, 20))
        self.frame_13.setFrameShape(QFrame.Shape.Panel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.frame_13, 0, 5, 1, 1)


        self.horizontalLayout_2.addWidget(self.frame_sensorstatus)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 0, 0)
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy2.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy2)
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
        self.label_mode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_mode)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.treeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem.setCheckState(0, Qt.Checked);
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsAutoTristate);
        __qtreewidgetitem1.setCheckState(0, Qt.Checked);
        __qtreewidgetitem2 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem2.setCheckState(0, Qt.Checked);
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem3.setCheckState(0, Qt.Checked);
        __qtreewidgetitem4 = QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem4.setCheckState(0, Qt.Checked);
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem5.setCheckState(0, Qt.Checked);
        __qtreewidgetitem6 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem6.setCheckState(0, Qt.Checked);
        __qtreewidgetitem7 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem7.setCheckState(0, Qt.Checked);
        __qtreewidgetitem8 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem8.setCheckState(0, Qt.Checked);
        __qtreewidgetitem9 = QTreeWidgetItem(__qtreewidgetitem8)
        __qtreewidgetitem9.setCheckState(0, Qt.Checked);
        __qtreewidgetitem10 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem10.setCheckState(0, Qt.Checked);
        __qtreewidgetitem11 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem11.setCheckState(0, Qt.Checked);
        __qtreewidgetitem12 = QTreeWidgetItem(__qtreewidgetitem9)
        __qtreewidgetitem12.setCheckState(0, Qt.Checked);
        __qtreewidgetitem13 = QTreeWidgetItem(__qtreewidgetitem8)
        __qtreewidgetitem13.setCheckState(0, Qt.Checked);
        __qtreewidgetitem14 = QTreeWidgetItem(__qtreewidgetitem8)
        __qtreewidgetitem14.setCheckState(0, Qt.Checked);
        __qtreewidgetitem15 = QTreeWidgetItem(__qtreewidgetitem8)
        __qtreewidgetitem15.setCheckState(0, Qt.Checked);
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy8)
        self.treeWidget.setMinimumSize(QSize(0, 300))
        self.treeWidget.setFrameShape(QFrame.Shape.Box)
        self.treeWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeWidget.setProperty(u"showDropIndicator", True)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setProperty(u"showSortIndicator", False)

        self.verticalLayout_7.addWidget(self.treeWidget)

        self.frame_sensorselection = QFrame(self.centralwidget)
        self.frame_sensorselection.setObjectName(u"frame_sensorselection")
        self.frame_sensorselection.setEnabled(True)
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(1)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.frame_sensorselection.sizePolicy().hasHeightForWidth())
        self.frame_sensorselection.setSizePolicy(sizePolicy9)
        self.frame_sensorselection.setMinimumSize(QSize(0, 50))
        self.frame_sensorselection.setSizeIncrement(QSize(0, 0))
        self.frame_sensorselection.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.frame_sensorselection.setFrameShape(QFrame.Shape.Box)
        self.frame_sensorselection.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_sensorselection.setLineWidth(1)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_sensorselection)
        self.horizontalLayout_7.setSpacing(10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.button_All = QPushButton(self.frame_sensorselection)
        self.button_All.setObjectName(u"button_All")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(1)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.button_All.sizePolicy().hasHeightForWidth())
        self.button_All.setSizePolicy(sizePolicy10)
        self.button_All.setMinimumSize(QSize(50, 30))
        self.button_All.setSizeIncrement(QSize(0, 0))
        self.button_All.setBaseSize(QSize(0, 0))
        self.button_All.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.horizontalLayout_7.addWidget(self.button_All)

        self.button_default = QPushButton(self.frame_sensorselection)
        self.button_default.setObjectName(u"button_default")
        sizePolicy2.setHeightForWidth(self.button_default.sizePolicy().hasHeightForWidth())
        self.button_default.setSizePolicy(sizePolicy2)
        self.button_default.setMinimumSize(QSize(50, 30))

        self.horizontalLayout_7.addWidget(self.button_default)


        self.verticalLayout_7.addWidget(self.frame_sensorselection)

        self.verticalLayout_7.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy11.setHorizontalStretch(3)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy11)
        self.frame.setMinimumSize(QSize(600, 300))
        self.frame.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.label_temp_3 = QLabel(self.frame)
        self.label_temp_3.setObjectName(u"label_temp_3")
        self.label_temp_3.setGeometry(QRect(70, 50, 101, 16))
        self.label_temp_3.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.verticalLayout_4.addWidget(self.frame)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame_timescale = QFrame(self.centralwidget)
        self.frame_timescale.setObjectName(u"frame_timescale")
        sizePolicy10.setHeightForWidth(self.frame_timescale.sizePolicy().hasHeightForWidth())
        self.frame_timescale.setSizePolicy(sizePolicy10)
        self.frame_timescale.setMinimumSize(QSize(0, 50))
        self.frame_timescale.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.frame_timescale.setFrameShape(QFrame.Shape.Box)
        self.frame_timescale.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_timescale)
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 10, 10, 10)
        self.button_Total = QPushButton(self.frame_timescale)
        self.button_Total.setObjectName(u"button_Total")
        sizePolicy10.setHeightForWidth(self.button_Total.sizePolicy().hasHeightForWidth())
        self.button_Total.setSizePolicy(sizePolicy10)
        self.button_Total.setMinimumSize(QSize(50, 30))
        self.button_Total.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.horizontalLayout_8.addWidget(self.button_Total)

        self.button_Last = QPushButton(self.frame_timescale)
        self.button_Last.setObjectName(u"button_Last")
        sizePolicy10.setHeightForWidth(self.button_Last.sizePolicy().hasHeightForWidth())
        self.button_Last.setSizePolicy(sizePolicy10)
        self.button_Last.setMinimumSize(QSize(50, 30))
        self.button_Last.setLocale(QLocale(QLocale.English, QLocale.Germany))

        self.horizontalLayout_8.addWidget(self.button_Last)


        self.horizontalLayout_9.addWidget(self.frame_timescale)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.verticalLayout_4.setStretch(0, 10)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.horizontalLayout_4.setStretch(0, 1)
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
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.label_SODS.sizePolicy().hasHeightForWidth())
        self.label_SODS.setSizePolicy(sizePolicy12)
        self.label_SODS.setMinimumSize(QSize(127, 0))
        self.label_SODS.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_SODS.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_SODS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_SODS, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_progressbars.addItem(self.horizontalSpacer_4, 0, 7, 1, 1)

        self.label_SD = QLabel(self.centralwidget)
        self.label_SD.setObjectName(u"label_SD")
        sizePolicy4.setHeightForWidth(self.label_SD.sizePolicy().hasHeightForWidth())
        self.label_SD.setSizePolicy(sizePolicy4)
        self.label_SD.setMinimumSize(QSize(97, 0))
        self.label_SD.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.label_SD.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.label_SD, 1, 8, 1, 1)

        self.progressBar_SODS = QProgressBar(self.centralwidget)
        self.progressBar_SODS.setObjectName(u"progressBar_SODS")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy13.setHorizontalStretch(1)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.progressBar_SODS.sizePolicy().hasHeightForWidth())
        self.progressBar_SODS.setSizePolicy(sizePolicy13)
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
        sizePolicy13.setHeightForWidth(self.progressBar_PF.sizePolicy().hasHeightForWidth())
        self.progressBar_PF.setSizePolicy(sizePolicy13)
        self.progressBar_PF.setMinimumSize(QSize(50, 0))
        self.progressBar_PF.setFont(font2)
        self.progressBar_PF.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.progressBar_PF.setValue(0)
        self.progressBar_PF.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_progressbars.addWidget(self.progressBar_PF, 0, 0, 1, 1)

        self.progressBar_LO = QProgressBar(self.centralwidget)
        self.progressBar_LO.setObjectName(u"progressBar_LO")
        sizePolicy13.setHeightForWidth(self.progressBar_LO.sizePolicy().hasHeightForWidth())
        self.progressBar_LO.setSizePolicy(sizePolicy13)
        self.progressBar_LO.setMinimumSize(QSize(50, 0))
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
        sizePolicy2.setHeightForWidth(self.label_SOE.sizePolicy().hasHeightForWidth())
        self.label_SOE.setSizePolicy(sizePolicy2)
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
        self.progressBar_SD.setMinimumSize(QSize(97, 0))
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
        sizePolicy15.setHorizontalStretch(10)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 1315, 20))
        self.menubar.setFont(font)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName(u"menuExport")
        self.menuConnection = QMenu(self.menubar)
        self.menuConnection.setObjectName(u"menuConnection")
        self.menuConnectionMode = QMenu(self.menuConnection)
        self.menuConnectionMode.setObjectName(u"menuConnectionMode")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menuLanguage = QMenu(self.menuOptions)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        self.menuMode = QMenu(self.menuStart)
        self.menuMode.setObjectName(u"menuMode")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuFile.addAction(self.actionFileNew)
        self.menuFile.addAction(self.actionFileLoad)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFileSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionResults)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addSeparator()
        self.menuExport.addAction(self.actionExportHousholding)
        self.menuExport.addAction(self.actionExportMeasurements)
        self.menuExport.addAction(self.actionExportEverything)
        self.menuConnection.addAction(self.actionConnect)
        self.menuConnection.addSeparator()
        self.menuConnection.addAction(self.actionRetry)
        self.menuConnection.addSeparator()
        self.menuConnection.addAction(self.actionLog)
        self.menuConnection.addAction(self.menuConnectionMode.menuAction())
        self.menuConnection.addSeparator()
        self.menuConnection.addAction(self.actionDisconnect)
        self.menuConnectionMode.addAction(self.actionConnectionAutomatic)
        self.menuConnectionMode.addAction(self.actionConnectionManual)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionDocumentation)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionGerman)
        self.menuStart.addAction(self.menuMode.menuAction())
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionRestart)
        self.menuStart.addAction(self.actionQuit)
        self.menuMode.addAction(self.actionTesting)
        self.menuMode.addAction(self.actionFlying)

        self.retranslateUi(MainWindow)

        self.button_Last.setDefault(True)


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
        self.actionRetry.setText(QCoreApplication.translate("MainWindow", u"Reconnect", None))
#if QT_CONFIG(shortcut)
        self.actionRetry.setShortcut(QCoreApplication.translate("MainWindow", u"F9", None))
#endif // QT_CONFIG(shortcut)
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.actionDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.actionRestart.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.actionConnectionAutomatic.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.actionConnectionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionExportHousholding.setText(QCoreApplication.translate("MainWindow", u"Housholding", None))
        self.actionExportMeasurements.setText(QCoreApplication.translate("MainWindow", u"Measurements", None))
        self.actionExportEverything.setText(QCoreApplication.translate("MainWindow", u"Full Dataset", None))
        self.actionModeRecording.setText(QCoreApplication.translate("MainWindow", u"Recording", None))
        self.actionModeReplaying.setText(QCoreApplication.translate("MainWindow", u"Replaying", None))
        self.actionModeTesting.setText(QCoreApplication.translate("MainWindow", u"Testing", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
#if QT_CONFIG(shortcut)
        self.actionDocumentation.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionLog.setText(QCoreApplication.translate("MainWindow", u"Connection Log", None))
        self.actionaloha.setText(QCoreApplication.translate("MainWindow", u"aloha", None))
        self.actionTesting.setText(QCoreApplication.translate("MainWindow", u"Test Mode", None))
        self.actionFlying.setText(QCoreApplication.translate("MainWindow", u"Flight Mode", None))
        self.actionReplaying.setText(QCoreApplication.translate("MainWindow", u"Replaying", None))
        self.label_Connection.setText(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"T -", None))
        self.label_temp_1.setText(QCoreApplication.translate("MainWindow", u"Graph over Distance", None))
        self.label_temp_4.setText(QCoreApplication.translate("MainWindow", u"System Status 1", None))
        self.label_temp_2.setText(QCoreApplication.translate("MainWindow", u"System Status 1", None))
        self.label_temp_6.setText(QCoreApplication.translate("MainWindow", u"System Status 1", None))
        self.label_temp_7.setText(QCoreApplication.translate("MainWindow", u"System Status 1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"System Status 1", None))
        self.label_logo.setText("")
        self.label_mode.setText(QCoreApplication.translate("MainWindow", u"Flight Mode", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Sensoren", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Druck", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"D\u00fcse", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem2.child(1)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem2.child(2)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"Akkumulator", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"Speicher", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"Umgebung", None));
        ___qtreewidgetitem9 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"Temperatur", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem9.child(0)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"Neues untergeordnetes Element", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem10.child(0)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem10.child(1)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem10.child(2)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem9.child(1)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"Akkumulator", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem9.child(2)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"Speicher", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem9.child(3)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"Vergleichsstelle", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.button_All.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.button_default.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.label_temp_3.setText(QCoreApplication.translate("MainWindow", u"Graph over Time", None))
        self.button_Total.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.button_Last.setText(QCoreApplication.translate("MainWindow", u"Last", None))
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
        self.menuConnection.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.menuConnectionMode.setTitle(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuMode.setTitle(QCoreApplication.translate("MainWindow", u"Mode", None))
    # retranslateUi

