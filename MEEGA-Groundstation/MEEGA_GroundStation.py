#imports
from __future__ import annotations
from math import floor
from math import sin, radians
import sys
import time

from PySide6.QtGui import (QAction, QActionGroup, QIcon, QImage, QPixmap, QPainter)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QMainWindow, QDialog, QWidget, QVBoxLayout)
from PySide6.QtCore import (Signal, Slot, QTranslator, QLocale, QThread, QPointF)
from PySide6.QtCharts import (QChart, QChartView, QLineSeries, QValueAxis)

from MEEGA_mainWindow import *
from MEEGA_calibration import *
from MEEGA_startup import *
from MEEGA_Connection import *
from MEEGA_time import *
from MEEGA_documentation import *
from MEEGA_error import *
from MEEGA_controlPanel import *
from MEEGA_results import *
from MEEGA_calibration import *
from MEEGA_diagramSettings import *

from MEEGA_PyDataHandling import *

#class to handle program settings
class Settings:
    AUTOMATIC = 0
    MANUAL = 1
    FLIGHT = 0
    TEST = 1
    SERIAL = 0
    TCP = 1
    #diagram flags
    SELFSCALING = 0
    FIXEDVALUE = 1
    SCROLLING = 0
    EXPANDING = 1
    ALL = 0
    LO = 1
    SOE = 2
    defaultFilePath = "Default.meega"
    defaultLaunchTime = QTime(12,0,0)

    def __init__(self, locale: QLocale = None):
        if locale == None:
            self.locale = QLocale()
        else:
            self.locale = QLocale(locale)
        self.mode = self.TEST
        self.connectionMode = self.AUTOMATIC
        self.connectionType = self.SERIAL
        self.connector = "COM4"
        self.filePath = self.defaultFilePath
        self.launchTime = self.defaultLaunchTime
        self.pressureAxeMode = self.SELFSCALING
        self.temperatureAxeMode = self.SELFSCALING
        self.timespanMode = self.EXPANDING
        self.pressureAxeValue = 300
        self.temperatureAxeValue = 300
        self.scrollingTimeSeconds = 10
        self.expandFrom = self.ALL
        self.liftOffIndex = -1
        self.startOfExperimentIndex = -1

#class to handle telecommands
class Telecommand:
    def __init__(self, collection):
        self.collection = collection
        self.tcframe = DataHandling.CreateTC()
        self.sendCounter = 0

    def newTCFrame(self):
        self.tcframe = DataHandling.CreateTC()
        DataHandling.WriteFrame(self.tcframe, 0, self.collection.settings.mode)

    def sendInit(self):
        self.sendCounter = 10

    def sendStep(self):
        if self.sendCounter > 0:
            DataHandling.AddFrame(self.tcframe)
            self.sendCounter -= 1

#class to define the Main Window
class GSMain(QMainWindow):
    def __init__(self, collection: ClassCollection):
        super().__init__()

        #importing visuals from the ui-file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #creating variables
        self.ACTIVE = 1
        self.ISSUES = 2
        self.INACTIVE = 0
        self.collection = collection

        #creating local status list
        self.statusDisplay = ["" for _ in range(20)]
        self.statusDisplay[0] = self.ui.statusLabelPAmbient
        self.statusDisplay[1] = self.ui.statusLabelTCompare
        self.statusDisplay[2] = self.ui.statusLabelPReservoir
        self.statusDisplay[3] = self.ui.statusLabelTReservoir
        self.statusDisplay[4] = self.ui.statusLabelPAccumulator
        self.statusDisplay[5] = self.ui.statusLabelTAccumulator
        self.statusDisplay[6] = self.ui.statusLabelPNozzle1
        self.statusDisplay[7] = self.ui.statusLabelTNozzle1
        self.statusDisplay[8] = self.ui.statusLabelPNozzle2
        self.statusDisplay[9] = self.ui.statusLabelTNozzle2
        self.statusDisplay[10] = self.ui.statusLabelPNozzle3
        self.statusDisplay[11] = self.ui.statusLabelTNozzle3
        self.statusDisplay[12] = self.ui.statusLabelServo
        self.statusDisplay[13] = self.ui.statusLabelValve
        self.statusDisplay[14] = self.ui.statusLabelLED
        self.statusDisplay[15] = self.ui.statusLabelPChip
        self.statusDisplay[16] = self.ui.statusLabelTChip
        self.statusDisplay[17] = self.ui.statusLabelMainboard
        self.statusDisplay[18] = self.ui.statusLabelLiftOff
        self.statusDisplay[19] = self.ui.statusLabelSOE

        #creating status pixmaps
        self.activepix = QPixmap("Ressources\\active.png")
        self.issuespix = QPixmap("Ressources\\issues.png")
        self.inactivepix = QPixmap("Ressources\\inactive.png")

        self.scalePixmaps()
        
        #standard display
        for statusLabel in self.statusDisplay:
            statusLabel.setPixmap(self.inactivepix_scaled)

        self.createPlots()

        self.setLocale(self.collection.settings.locale)

        self.ui.treeWidget.expandAll()

        #creating the big logo
        self.logo = QPixmap("Ressources\\meega_logo_small.png")
        self.ui.label_logo.setPixmap(self.logo)

        #creating menubar actiongroups (for exclusivity of selected options)
        self.languageGroup = QActionGroup(self.ui.menuLanguage)
        self.languageGroup.setExclusive(True)
        for i in self.ui.menuLanguage.actions():
            self.languageGroup.addAction(i)
        self.modeGroup = QActionGroup(self.ui.menuStart)
        self.modeGroup.setExclusive(True)
        self.modeGroup.addAction(self.ui.actionFlight_Mode)
        self.modeGroup.addAction(self.ui.actionTest_Mode)
        self.connectionModeGroup = QActionGroup(self.ui.menuConnection)
        self.connectionModeGroup.addAction(self.ui.actionAutomatic)
        self.connectionModeGroup.addAction(self.ui.actionManual)
        
        #reference to the application object
        self.app = QApplication.instance()
    #internal functions
    def connect(self):
        #connection of signals and slots
        self.languageGroup.triggered.connect(self.languageChanges)
        self.ui.actionManual.triggered.connect(self.fetchSettings)
        self.ui.actionAutomatic.triggered.connect(self.fetchSettings)
        self.ui.actionFlight_Mode.triggered.connect(self.modeSwitched)
        self.ui.actionTest_Mode.triggered.connect(self.modeSwitched)
        self.ui.actionQuit.triggered.connect(self.collection.shutdown)
        self.ui.treeWidget.itemChanged.connect(self.onItemChanged)
    #override closeEvent to ensure proper thread termination and application exit
    def closeEvent(self, event):
        self.collection.shutdown()
        event.accept()
        super().closeEvent(event)
    def scalePixmaps(self):
            #Pixmaps an die aktuelle Label-Groesse anpassen
            label_size = self.ui.statusLabelMainboard.size()
            circle_diameter = min(label_size.width(), label_size.height())
            self.activepix_scaled = self.activepix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.issuespix_scaled = self.issuespix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.inactivepix_scaled = self.inactivepix.scaled(circle_diameter, circle_diameter, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #scale for connection status
            #self.activepix_
    #override resizeEvent to rescale pixmaps when window size changes
    def resizeEvent(self, event):
            self.scalePixmaps()
            super().resizeEvent(event)
    def retranslateUi(self):
        self.ui.retranslateUi()
    def languageChanges(self):
        translator = QTranslator()
        locale = self.collection.settings.locale
        language = QLocale.languageToCode(locale.language())
        for i in self.languageGroup.actions():
            if i.property("data") == language:
                i.setChecked(True)
        #Baustelle:
        if translator.load(locale, "MEEGA_Language"):
            self.app.removeTranslator(translator)
            self.app.installTranslator(translator)
            self.retranslateUi(self)
    def connectionModeChanges(self):
        if self.collection.settings.connectionMode == Settings.AUTOMATIC:
            self.ui.actionConnect.setEnabled(False)
            self.ui.actionRetry.setEnabled(False)
            self.ui.actionDisconnect.setEnabled(False)
        else:
            self.ui.actionConnect.setEnabled(True)
            self.ui.actionRetry.setEnabled(True)
            self.ui.actionDisconnect.setEnabled(True)
            self.ui.menuSettings.popup(self.ui.menuSettings.pos())
            self.ui.menuSettings.setActiveAction(self.ui.menuConnection.menuAction())
    def filePathChanges(self):
        pass
    def displayStatus(self, index: int):
        #connection status


        #sensor / household status
        #check for invalid index
        if index is None or index < 0:
            return
        statusList = self.collection.dataAccumulation.household[index][0:12] + self.collection.dataAccumulation.household[index][14:20] + self.collection.dataAccumulation.household[index][21:23]
        for i in range(len(self.statusDisplay)):
            match statusList[i]:
                case self.ACTIVE:
                    self.statusDisplay[i].setPixmap(self.activepix_scaled)
                case self.ISSUES:
                    self.statusDisplay[i].setPixmap(self.issuespix_scaled)
                case self.INACTIVE:
                    self.statusDisplay[i].setPixmap(self.inactivepix_scaled)
    def createPlots(self):
        #time plot
        #create Line Series for each sensor
        #ambient pressure, compare temperature, accumulator pressure, accumulator temperature, chamber pressure, chamber temperature, nozzle 1 pressure, nozzle 1 temperature, nozzle 2 pressure, nozzle 2 temperature, nozzle 3 pressure, nozzle 3 temperature
        self.timeSeries = [QLineSeries() for _ in range(12)]

        self.timeHighestPres = 0
        self.timeHighestTemp = 0

        #create and add Series
        self.timeChart = QChart()
        for s in self.timeSeries:
            self.timeChart.addSeries(s)

        #create and configure Axes
        self.timeAxis = QValueAxis()
        self.timePressureAxis = QValueAxis()
        self.timeTemperatureAxis = QValueAxis()
        self.timeAxis.setTitleText("time in ms")
        self.timePressureAxis.setTitleText("pressure in Pa")
        self.timeTemperatureAxis.setTitleText("temperature in K")
        self.timePressureAxis.setRange(0, self.collection.settings.pressureAxeValue)
        self.timeTemperatureAxis.setRange(0, self.collection.settings.temperatureAxeValue)
        self.timeAxis.setRange(0, 1)
        self.timeChart.addAxis(self.timeAxis, Qt.AlignBottom)
        self.timeChart.addAxis(self.timePressureAxis, Qt.AlignLeft)
        self.timeChart.addAxis(self.timeTemperatureAxis, Qt.AlignRight)
        for s in self.timeSeries:
            s.attachAxis(self.timeAxis)
            s.attachAxis(self.timePressureAxis)
            s.attachAxis(self.timeTemperatureAxis)
        
        #create Layout
        self.timeLayout = QVBoxLayout(self.ui.timePlotGroupBox)
        self.timeLayout.setContentsMargins(0,0,0,0)

        #create ChartView and add to Layout
        self.timeChartView = QChartView(self.timeChart)
        self.timeChartView.setRenderHint(QPainter.Antialiasing)
        self.timeLayout.addWidget(self.timeChartView)

        #distance plot
        #create Line Series for pressure and temperature
        self.distancePSeries = QLineSeries()
        self.distanceTSeries = QLineSeries()

        #create Chart and add Series
        self.distanceChart = QChart()
        self.distanceChart.addSeries(self.distancePSeries)
        self.distanceChart.addSeries(self.distanceTSeries)

        #create and configure Axes
        self.distanceYAxis = QValueAxis()
        self.distancePressureAxis = QValueAxis()
        self.distanceTemperatureAxis = QValueAxis()
        self.distancePressureAxis.setTitleText("pressure in Pa")
        self.distanceTemperatureAxis.setTitleText("temperature in K")
        self.distanceYAxis.setRange(0, 4)
        self.distancePressureAxis.setRange(0, self.collection.settings.pressureAxeValue)
        self.distanceTemperatureAxis.setRange(0, self.collection.settings.temperatureAxeValue)
        self.distanceChart.addAxis(self.distancePressureAxis, Qt.AlignBottom)
        self.distanceChart.addAxis(self.distanceTemperatureAxis, Qt.AlignTop)
        self.distanceChart.addAxis(self.distanceYAxis, Qt.AlignLeft)
        self.distancePSeries.attachAxis(self.distancePressureAxis)
        self.distancePSeries.attachAxis(self.distanceTemperatureAxis)
        self.distancePSeries.attachAxis(self.distanceYAxis)
        self.distanceTSeries.attachAxis(self.distancePressureAxis)
        self.distanceTSeries.attachAxis(self.distanceTemperatureAxis)
        self.distanceTSeries.attachAxis(self.distanceYAxis)
        
        #create Layout
        self.distanceLayout = QVBoxLayout(self.ui.distancePlotGroupBox)
        self.distanceLayout.setContentsMargins(0,0,0,0)

        #add Chart to ChartView and Layout
        self.distanceChartView = QChartView(self.distanceChart)
        self.distanceChartView.setRenderHint(QPainter.Antialiasing)
        self.distanceLayout.addWidget(self.distanceChartView)

        self.connectItemsToSeries()

    def extendPlots(self, index: int):
        settings = self.collection.settings
        dataAccu = self.collection.dataAccumulation

        #check for invalid index
        if index is None or index < 0:
            return
        if index >= len(dataAccu.sensorData) or index >= len(dataAccu.household):
            return

        #distance plot
        self.distancePSeries.clear()
        self.distanceTSeries.clear()
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[index][2], 0)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[index][4], 1)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[index][6], 2)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[index][8], 3)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[index][10], 4)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[index][3], 0)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[index][5], 1)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[index][7], 2)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[index][9], 3)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[index][11], 4)

        #skip if expandng mode needs an event that hasnt happened yet
        if not (settings.timespanMode == Settings.EXPANDING and(
            (settings.expandFrom == Settings.LO and settings.liftOffIndex == -1) or 
            (settings.expandFrom == Settings.SOE and settings.startOfExperimentIndex == -1)
        )):
            #time plot
            for i in range(12):
                while settings.timespanMode == Settings.SCROLLING and (self.timeSeries[i].at(self.timeSeries[i].count()-1).x() - self.timeSeries[i].at(0).x()) >= settings.scrollingTimeSeconds*1000:
                    self.timeSeries[i].remove(0)
                self.timeSeries[i].append(dataAccu.household[index][20], dataAccu.sensorData[index][i])
                if i%2 == 0: #pressure Value
                    if dataAccu.sensorData[index][i] > self.timeHighestPres:
                        self.timeHighestPres = dataAccu.sensorData[index][i]
                else: #temperature Value
                    if dataAccu.sensorData[index][i] > self.timeHighestTemp:
                        self.timeHighestTemp = dataAccu.sensorData[index][i]
            self.timeAxis.setRange(self.timeSeries[0].at(0).x(), self.timeSeries[0].at(self.timeSeries[0].count()-1).x())

        if settings.temperatureAxeMode == Settings.SELFSCALING or settings.pressureAxeMode == Settings.SELFSCALING:
            self.updateAxes()

    def rebuildPlot(self):
        settings = self.collection.settings
        dataAcc = self.collection.dataAccumulation
        sensorData = dataAcc.sensorData
        household = dataAcc.household

        startIndex = 0
        endIndex = dataAcc.gatherIndex
        if settings.timespanMode == Settings.EXPANDING:
            match settings.expandFrom:
                case Settings.LO:
                    if settings.liftOffIndex != -1:
                        startIndex = settings.liftOffIndex
                case Settings.SOE:
                    if settings.startOfExperimentIndex != -1:
                        startIndex = self.collection.startOfExperimentIndex
        else:
            startIndex = max(0, len(sensorData) - self.collection.dataHandlingThread.frequency * settings.scrollingTimeSeconds - 1)

        xValues = [household[p][20] for p in range(startIndex, endIndex)]
        for i in range(12):
            yValues =  [sensorData[p][i] for p in range(startIndex, endIndex)]
            points = [QPointF(x, y) for x, y in zip(xValues, yValues)]
            self.timeSeries[i].replace(points)

    def updateAxes(self):
        settings = self.collection.settings
        if settings.pressureAxeMode == Settings.FIXEDVALUE:
            self.timePressureAxis.setRange(0, settings.pressureAxeValue)
            self.distancePressureAxis.setRange(0, settings.pressureAxeValue)
        else:
            self.timePressureAxis.setRange(0, self.timeHighestPres)
            self.distancePressureAxis.setRange(0, max(point.x() for point in self.distancePSeries.points()))
        if settings.temperatureAxeMode == Settings.FIXEDVALUE:
            self.timeTemperatureAxis.setRange(0, settings.temperatureAxeValue)
            self.distanceTemperatureAxis.setRange(0, settings.temperatureAxeValue)
        else:
            self.timeTemperatureAxis.setRange(0, self.timeHighestTemp)
            self.distanceTemperatureAxis.setRange(0, max(point.x() for point in self.distanceTSeries.points()))

    def connectItemsToSeries(self):
        tree = self.ui.treeWidget
        tree.topLevelItem(0).child(0).child(3).setData(0, Qt.UserRole, 0)  # Ambient Pressure
        tree.topLevelItem(0).child(1).child(3).setData(0, Qt.UserRole, 1)  # Compare Temperature
        tree.topLevelItem(0).child(0).child(2).setData(0, Qt.UserRole, 2)  # Accumulator Pressure
        tree.topLevelItem(0).child(1).child(2).setData(0, Qt.UserRole, 3)  # Accumulator Temperature
        tree.topLevelItem(0).child(0).child(1).setData(0, Qt.UserRole, 4)  # Chamber Pressure
        tree.topLevelItem(0).child(1).child(1).setData(0, Qt.UserRole, 5)  # Chamber Temperature
        tree.topLevelItem(0).child(0).child(0).child(0).setData(0, Qt.UserRole, 6)  # Nozzle 1 Pressure
        tree.topLevelItem(0).child(1).child(0).child(0).setData(0, Qt.UserRole, 7)  # Nozzle 1 Temperature
        tree.topLevelItem(0).child(0).child(0).child(1).setData(0, Qt.UserRole, 8)  # Nozzle 2 Pressure
        tree.topLevelItem(0).child(1).child(0).child(1).setData(0, Qt.UserRole, 9)  # Nozzle 2 Temperature
        tree.topLevelItem(0).child(0).child(0).child(2).setData(0, Qt.UserRole, 10)  # Nozzle 3 Pressure
        tree.topLevelItem(0).child(1).child(0).child(2).setData(0, Qt.UserRole, 11)  # Nozzle 3 Temperature

    #external functions (slots)
    @Slot(int)
    def onNewFrame(self, index: int):
        self.extendPlots(index)
        self.displayStatus(index)
    @Slot()
    def modeSwitched(self):
        if self.modeGroup.checkedAction() == self.ui.actionFlight_Mode:
            self.collection.settings.mode = Settings.FLIGHT
            self.ui.label_mode.setText("Flight Mode")
            self.ui.actionControl_Panel.setEnabled(False)
            self.collection.controlPanel.clearPanel()
            self.collection.controlPanel.hide()
        else:
            self.collection.settings.mode = Settings.TEST
            self.ui.label_mode.setText("Test Mode")
            self.ui.actionControl_Panel.setEnabled(True)
        self.collection.telecommand.newTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def fetchSettings(self):
        if self.connectionModeGroup.checkedAction() == self.ui.actionAutomatic:
            connectionMode = Settings.AUTOMATIC
        else:
            connectionMode = Settings.MANUAL
        self.collection.settings.connectionMode = connectionMode
        self.connectionModeChanges()
    @Slot()
    def applySettings(self):
        if self.collection.settings.connectionMode == Settings.AUTOMATIC:
            self.ui.actionAutomatic.setChecked(True)
        else:
            self.ui.actionManual.setChecked(True)
        if self.collection.settings.mode == Settings.FLIGHT:
            self.ui.actionFlight_Mode.setChecked(True)
        else:
            self.ui.actionTest_Mode.setChecked(True)
        self.setLocale(self.collection.settings.locale)
        self.languageChanges()
        self.modeSwitched()
        self.connectionModeChanges()
        self.filePathChanges()

    @Slot(QTreeWidgetItem, int)
    def onItemChanged(self, item, column):
        if item.data(0, Qt.UserRole) is None:
            return
        series = self.timeSeries[item.data(0, Qt.UserRole)]
        if item.checkState(0) == Qt.Checked:
            if series not in self.timeChart.series():
                self.timeChart.addSeries(series)
                series.attachAxis(self.timeAxis)
                series.attachAxis(self.timeTemperatureAxis)
                series.attachAxis(self.timePressureAxis)
        else:
            if series in self.timeChart.series():
                self.timeChart.removeSeries(series)

#class to define the startup dialog window
class GSStart(QDialog):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
        self.collection = collection
        self.ui.languageComboBox.setItemData(0, "en")
        self.ui.languageComboBox.setItemData(1, "de")
        self.ui.connectionComboBox.setItemData(0,Settings.AUTOMATIC)
        self.ui.connectionComboBox.setItemData(1,Settings.MANUAL)
        self.ui.modeComboBox.setItemData(0, Settings.TEST)
        self.ui.modeComboBox.setItemData(1, Settings.FLIGHT)

        self.rejected.connect(self.collection.shutdown)
        self.accepted.connect(self.fetchSettings)

    #override closeEvent to ensure proper thread termination and application exit
    def closeEvent(self, event):
        self.collection.shutdown()
        event.accept()
        super().closeEvent(event)

    @Slot()
    def fetchSettings(self):
        self.collection.settings.language = self.ui.languageComboBox.currentData()
        self.collection.settings.connectionMode = self.ui.connectionComboBox.currentData()
        self.collection.settings.mode = self.ui.modeComboBox.currentData()
        self.collection.settings.filepath = self.ui.saveFileEdit.text()
        self.collection.settings.launchTime = self.ui.launchTimeTimeEdit.time()

class GSLaunchTime(QDialog):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_LaunchTimeDialog()
        self.ui.setupUi(self)
        self.collection = collection

        self.accepted.connect(self.fetchSettings)
    
    @Slot()
    def fetchSettings(self):
        self.collection.settings.launchTime = self.ui.launchTimeEdit.time()

class GSResults(QWidget):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_ResultsWidget()
        self.ui.setupUi(self)
        self.collection = collection

        self.ui.buttonBox.clicked.connect(self.hide)

class GSDocumentation(QWidget):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_Documentation()
        self.ui.setupUi(self)
        self.collection = collection

class GSError(QDialog):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self)
        self.collection = collection
  
class GSControl(QWidget):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_controlPanel()
        self.ui.setupUi(self)
        self.collection = collection

        # Initialize control states
        self.valveControl = 0  # closed
        self.ledState = 0      # False (Off)
        self.servoAngle = 0 # in 1/10 °
        self.dryRunActive = 0
        self.testRunStart = 0
        self.testRunStop = 0
        # Initialize duration values
        self.valveDelay = QTime(0, 0, 0)
        self.servoDelay = QTime(0, 0, 0)
        self.EOEDelay = QTime(0, 0, 0)
        # Connect signals to slots
        self.connectSignals()
        
    def connectSignals(self):
        # Valve controls
        self.ui.openValveButton.clicked.connect(self.openValve)
        self.ui.closeValveButton.clicked.connect(self.closeValve)
        # Servo controls
        self.ui.setServoButton.clicked.connect(self.setServoAngle)
        # LED controls
        self.ui.ledOnButton.clicked.connect(self.onLED)
        self.ui.ledOffButton.clicked.connect(self.offLED)
        # Test run controls
        self.ui.startTestButton.clicked.connect(self.startTest)
        self.ui.stopTestButton.clicked.connect(self.stopTest)
        # Dry run control
        self.ui.dryRunOnButton.clicked.connect(self.dryRunSwitch)
        # Reset buttons
        self.ui.valveResetButton.clicked.connect(self.resetValveDelay)
        self.ui.servoResetButton.clicked.connect(self.resetServoDelay)
        self.ui.EOEResetButton.clicked.connect(self.resetEOEDelay)
    
    # external functions for ui controls
    # Valve control slots
    @Slot()
    def openValve(self):
        self.valveControl = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def closeValve(self):
        self.valveControl = 0
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # Servo control slot
    @Slot()
    def setServoAngle(self):
        self.servoAngle = self.ui.servoValueBox.value()
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # LED control slots
    @Slot()
    def onLED(self):
        self.ledState = 0
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def offLED(self):
        self.ledState = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    # Test run control slots
    @Slot()
    def startTest(self):
        self.setDelays()
        self.testRunStart = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
        self.testRunStart = 0
    @Slot()
    def stopTest(self):
        self.testRunStop = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
        self.testRunStop = 0
    # Dry run control slot
    @Slot()
    def dryRunSwitch(self):
        if self.ui.dryRunOnButton.isChecked():
            self.dryRunActive = 1
        else:
            self.dryRunActive = 0
    # Reset duration slots
    @Slot()
    def resetValveDelay(self):
        self.ui.valveTimeEdit.setTime(QTime(0, 0, 0))
        self.ui.valveMilliEdit.setText("000")
        self.valveDelay = QTime(0, 0, 0)
    @Slot()
    def resetServoDelay(self):
        self.ui.servoTimeEdit.setTime(QTime(0, 0, 0))
        self.ui.servoMilliEdit.setText("000")
        self.servoDelay = QTime(0, 0, 0)
    @Slot()
    def resetEOEDelay(self):
        self.ui.EOETimeEdit.setTime(QTime(0, 0, 0))
        self.ui.EOEMilliEdit.setText("000")
        self.EOEDelay = QTime(0, 0, 0)

    # internal functions
    # Duration changes
    def setDelays(self):
        self.valveDelay = self.ui.valveTimeEdit.time().addMSecs(int(self.ui.valveMilliEdit.text()))
        self.servoDelay = self.ui.servoTimeEdit.time().addMSecs(int(self.ui.servoMilliEdit.text()))
        self.EOEDelay = self.ui.EOETimeEdit.time().addMSecs(int(self.ui.EOEMilliEdit.text()))
    # Update the telecommand frame with current control states and durations
    def updateTCFrame(self):
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 1, (self.valveDelay.minute()*60 + self.valveDelay.second())*1000 + self.valveDelay.msec())
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 2, (self.servoDelay.minute()*60 + self.servoDelay.second())*1000 + self.servoDelay.msec())
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 3, (self.EOEDelay.minute()*60 + self.EOEDelay.second())*1000 + self.EOEDelay.msec())
        #PowerOffDelay fehlt
        #NozzleOnDelay fehlt
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 6, self.dryRunActive)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 7, self.ledState)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 8, floor(self.servoAngle*10))
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 9, self.valveControl)
        #Camera control fehlt
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 11, self.testRunStop)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, 12, self.testRunStart)
    def clearPanel(self):
        self.valveControl = 0
        self.ledState = 0
        self.servoAngle = 0
        self.ui.servoValueBox.setValue(0)
        self.dryRunActive = 0
        self.ui.dryRunOnButton.setChecked(False)
        self.testRunStart = 0
        self.testRunStop = 0
        self.resetValveDelay()
        self.resetServoDelay()
        self.resetEOEDelay()

class GSConnection(QDialog):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)
        self.collection = collection
        self.ui.ConnectorBox.setCurrentIndex(int(self.collection.settings.connector[-1])-1)

        self.connect()

    def applySettings(self):
        if self.ui.RS_Button.isChecked():
            self.collection.settings.connectionType = Settings.SERIAL
            self.collection.settings.connector = self.ui.ConnectorBox.currentText().encode("utf-8")
            DataHandling.SetPort(self.collection.settings.connector)
        else:
            self.collection.settings.connectionType = Settings.TCP

    def connect(self):
        self.ui.TCP_Button.clicked.connect(self.ui.PortEdit.setEnabled)
        self.ui.TCP_Button.clicked.connect(self.ui.IPEdit.setEnabled)
        self.ui.TCP_Button.clicked.connect(self.ui.ConnectorBox.setDisabled)
        self.ui.RS_Button.clicked.connect(self.ui.PortEdit.setDisabled)
        self.ui.RS_Button.clicked.connect(self.ui.IPEdit.setDisabled)
        self.ui.RS_Button.clicked.connect(self.ui.ConnectorBox.setEnabled)
        self.ui.buttonBox.accepted.connect(self.applySettings)

class GSCalibration(QDialog):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_Sensor_Calibration()
        self.ui.setupUi(self)
        self.collection = collection

        #initialize variables
        self.selectedSensor = 0
        self.selectedEntry = 0
        self.currentUnit = ""
        self.calibrationPoints = [[0] * 3 for x in range(12)]

        #create exclusive button group for radio buttons and add automatic disabling/enabling of lineEdits
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.ui.radioButton)
        self.buttonGroup.addButton(self.ui.radioButton_2)
        self.buttonGroup.addButton(self.ui.radioButton_3)
        self.buttonGroup.setExclusive(True)
        self.ui.radioButton.clicked.connect(self.selectEntry)
        self.ui.radioButton_2.clicked.connect(self.selectEntry)
        self.ui.radioButton_3.clicked.connect(self.selectEntry)
        self.ui.radioButton.click()

        self.selectSensor()
        self.ui.comboBox.currentIndexChanged.connect(self.selectSensor)
        self.ui.pushButton.clicked.connect(self.newCalibrationPoint)
    

    #update the displayed sensor value
    def updateValue(self, index: int):
        digitalValue = self.collection.dataAccumulation.sensorData[index][self.selectedSensor]
        mappedValue = str(DataHandling.MapSensorValue(self.selectedSensor, int(digitalValue)))
        self.ui.label.setText(mappedValue + " " + self.currentUnit)
    
    #select sensor and display already existing calibration points, according Units
    @Slot()
    def selectSensor(self):
        self.selectedSensor = self.ui.comboBox.currentIndex()
        self.ui.lineEdit.setText(str(self.calibrationPoints[self.selectedSensor][0]))
        self.ui.lineEdit_2.setText(str(self.calibrationPoints[self.selectedSensor][1]))
        self.ui.lineEdit_3.setText(str(self.calibrationPoints[self.selectedSensor][2]))
        if self.selectedSensor in [0,2,4,6,8,10]:
            self.currentUnit = "Pa"
        else:
            self.currentUnit = "K"
        self.ui.label_2.setText(self.currentUnit)
        self.ui.label_3.setText(self.currentUnit)
        self.ui.label_4.setText(self.currentUnit)

    #enable lineEdit corresponding to selected radioButton, disable the others
    @Slot()
    def selectEntry(self):
        match self.buttonGroup.checkedButton():
            case self.ui.radioButton:
                self.ui.lineEdit.setEnabled(True)
                self.ui.lineEdit_2.setDisabled(True)
                self.ui.lineEdit_3.setDisabled(True)
                self.selectedEntry = 0
            case self.ui.radioButton_2:
                self.ui.lineEdit.setDisabled(True)
                self.ui.lineEdit_2.setEnabled(True)
                self.ui.lineEdit_3.setDisabled(True)
                self.selectedEntry = 1
            case self.ui.radioButton_3:
                self.ui.lineEdit.setDisabled(True)
                self.ui.lineEdit_2.setDisabled(True)
                self.ui.lineEdit_3.setEnabled(True)
                self.selectedEntry = 2
    
    #save the currently selected calibration point
    @Slot()
    def newCalibrationPoint(self):
        currentEntry = ""
        match self.selectedEntry:
            case 0:
                currentEntry = self.ui.lineEdit.text()
            case 1:
                currentEntry = self.ui.lineEdit_2.text()
            case 2:
                currentEntry = self.ui.lineEdit_3.text()
        digitalValue = self.collection.dataAccumulation.sensorData[self.collection.dataAccumulation.gatherIndex][self.selectedSensor]
        DataHandling.WritePoint(self.selectedSensor, self.selectedEntry, digitalValue, float(currentEntry))
        self.calibrationPoints[self.selectedSensor][self.selectedEntry] = float(currentEntry)

    @Slot(int)
    def onNewFrame(self, index:int):
        self.updateValue(index)

class GSDiagramSettings(QWidget):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.ui = Ui_diagramSettings()
        self.ui.setupUi(self)
        self.collection = collection
        self.connect()
    
    @Slot()
    def applySettings(self):
        plotRebuildNecessary = False

        if self.ui.pressureSelfScaling.isChecked():
            self.collection.settings.pressureAxeMode = Settings.SELFSCALING
        else:
            self.collection.settings.pressureAxeMode = Settings.FIXEDVALUE
            self.collection.settings.pressureAxeValue = float(self.ui.pressureLineEdit.text())
        if self.ui.temperatureSelfScaling.isChecked():
            self.collection.settings.temperatureAxeMode = Settings.SELFSCALING
        else:
            self.collection.settings.temperatureAxeMode = Settings.FIXEDVALUE
            self.collection.settings.temperatureAxeValue = float(self.ui.temperatureLineEdit.text())

        if self.ui.scrollingRadioButton.isChecked():
            if self.collection.settings.timespanMode != Settings.SCROLLING:
                plotRebuildNecessary = True
                self.collection.settings.timespanMode = Settings.SCROLLING
            if self.collection.settings.scrollingTimeSeconds != int(self.ui.scrollingTimeEdit.time().minute()*60 + self.ui.scrollingTimeEdit.time().second()):
                plotRebuildNecessary = True
                self.collection.settings.scrollingTimeSeconds = int(self.ui.scrollingTimeEdit.time().minute()*60 + self.ui.scrollingTimeEdit.time().second())
        else:
            if self.collection.settings.timespanMode != Settings.EXPANDING:
                plotRebuildNecessary = True
                self.collection.settings.timespanMode = Settings.EXPANDING
            if self.collection.settings.expandFrom != self.ui.firstShownComboBox.currentIndex():
                plotRebuildNecessary = True
                self.collection.settings.expandFrom = self.ui.firstShownComboBox.currentIndex()

        if plotRebuildNecessary:
            self.collection.mainWindow.rebuildPlot()
        self.collection.mainWindow.updateAxes()

    def radioButtonClicked(self):
        if self.ui.pressureSelfScaling.isChecked():
            self.ui.pressureLineEdit.setDisabled(True)
        else:
            self.ui.pressureLineEdit.setEnabled(True)
        if self.ui.temperatureSelfScaling.isChecked():
            self.ui.temperatureLineEdit.setDisabled(True)
        else:
            self.ui.temperatureLineEdit.setEnabled(True)
        if self.ui.scrollingRadioButton.isChecked():
            self.ui.scrollingTimeEdit.setEnabled(True)
            self.ui.firstShownComboBox.setDisabled(True)
        else:
            self.ui.scrollingTimeEdit.setDisabled(True)
            self.ui.firstShownComboBox.setEnabled(True)

    def connect(self):
        self.ui.pressureSelfScaling.clicked.connect(self.radioButtonClicked)
        self.ui.pressureFixedValue.clicked.connect(self.radioButtonClicked)
        self.ui.temperatureSelfScaling.clicked.connect(self.radioButtonClicked)
        self.ui.temperatureFixedValue.clicked.connect(self.radioButtonClicked)
        self.ui.scrollingRadioButton.clicked.connect(self.radioButtonClicked)
        self.ui.scrollingRadioButton.clicked.connect(self.radioButtonClicked)
        self.ui.expandingRadioButton.clicked.connect(self.radioButtonClicked)
        self.ui.expandingRadioButton.clicked.connect(self.radioButtonClicked)
        self.ui.applyDiagramSettings.clicked.connect(self.applySettings)

class DataAccumulation:
    def __init__(self, collection: ClassCollection):
        self.collection = collection
        self.gatherIndex = -1
        self.allocationSize = 5000
        self.sensorData = [[0 for _ in range(12)] for __ in range(self.allocationSize)]
        self.household = [[0 for _ in range(27)] for __ in range(self.allocationSize)]

    def accumulate(self):
        # while True:
            # frame = DataHandling.getnextframe()
            # if DataHandling.frameisempty(frame):
            #    break
            # else:
            #     self.gatherIndex += 1
        ###
        self.gatherIndex += 1 ###only for testing purposes###
        ###
        if self.gatherIndex%self.allocationSize == 0:
            dataExtension = [[0 for _ in range(12)] for __ in range(self.allocationSize)]
            householdExtension = [[0 for _ in range(27)] for __ in range(self.allocationSize)]
            self.sensorData.extend(dataExtension)
            self.household.extend(householdExtension)
        for i in range(12):
            ###
            self.sensorData[self.gatherIndex][i] = int(150*sin(radians(10*self.gatherIndex + 10*i))+150) ###only for testing purposes###
            ###
            # self.sensorData[self.gatherIndex][i] = DataHandling.MapSensorValue(i, DataHandling.ReadFrame(frame, i))
        ###
        self.household[self.gatherIndex][20] = 500*self.gatherIndex  ###only for testing purposes###
        ###
        # for i in range(12):
        #    self.household[self.gatherIndex][i] = DataHandling.ReadFrame(frame, 12+i)
        # self.household[self.gatherIndex][12] = DataHandling.ReadFrame(frame, TMID.Nozzle_Open)
        # self.household[self.gatherIndex][13] = DataHandling.ReadFrame(frame, TMID.Nozzle_Closed)
        # self.household[self.gatherIndex][14] = DataHandling.ReadFrame(frame, TMID.Nozzle_Servo)
        # self.household[self.gatherIndex][15] = DataHandling.ReadFrame(frame, TMID.Reservoir_Valve)
        # self.household[self.gatherIndex][16] = DataHandling.ReadFrame(frame, TMID.LEDs)
        # self.household[self.gatherIndex][17] = DataHandling.ReadFrame(frame, TMID.Sensorboard_P)
        # self.household[self.gatherIndex][18] = DataHandling.ReadFrame(frame, TMID.Sensorboard_T)
        # self.household[self.gatherIndex][19] = DataHandling.ReadFrame(frame, TMID.Mainboard)
        # self.household[self.gatherIndex][20] = DataHandling.ReadFrame(frame, TMID.System_Time)
        # self.household[self.gatherIndex][21] = DataHandling.ReadFrame(frame, TMID.Lift_Off)
        # self.household[self.gatherIndex][22] = DataHandling.ReadFrame(frame, TMID.Start_Experiment)
        # self.household[self.gatherIndex][23] = DataHandling.ReadFrame(frame, TMID.End_Experiment)
        # self.household[self.gatherIndex][24] = DataHandling.ReadFrame(frame, TMID.Mode)
        # self.household[self.gatherIndex][25] = DataHandling.ReadFrame(frame, TMID.Experiment_State)
        
        if self.household[self.gatherIndex - 1][21] == 0 and self.household[self.gatherIndex][21] == 1:
            self.collection.settings.liftOffIndex = self.gatherIndex
        if self.household[self.gatherIndex -1][22] == 0 and self.household[self.gatherIndex][22] == 1:
            self.collection.settings.startOfExperimentIndex = self.gatherIndex

class DataHandlingThread(QThread):
    newFrameSignal = Signal(int)

    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.collection = collection
        self.frequency = 2
    def run(self):
        period_ms = 1000 / self.frequency
        while True:
            clock = time.monotonic_ns()
            self.collection.dataAccumulation.accumulate()
            self.collection.telecommand.sendStep()
            self.newFrameSignal.emit(int(self.collection.dataAccumulation.gatherIndex))
            DataHandling.UpdateAll()
            if self.isInterruptionRequested():
                DataHandling.CloseAll()
                break
            endTime = time.monotonic_ns()
            if (endTime - clock)/1000000 < period_ms:
                self.msleep(period_ms - (endTime - clock) / 1000000)

class ClassCollection:
    def __init__(self):
        self.settings = Settings()
        self.telecommand = Telecommand(self)
        self.dataAccumulation = DataAccumulation(self)
        self.mainWindow = GSMain(self)
        self.startWindow = GSStart(self)
        self.controlPanel = GSControl(self)
        self.timeWindow = GSLaunchTime(self)
        self.documentationWindow = GSDocumentation(self)
        self.errorWindow = GSError(self)
        self.resultsWindow = GSResults(self)
        self.connectionWindow = GSConnection(self)
        self.calibrationWindow = GSCalibration(self)
        self.diagramSettingsWindow = GSDiagramSettings(self)
        #DataHandling setup
        DataHandling.Initialize(b"")
        self.dataHandlingThread = DataHandlingThread(self)
        self.dataHandlingThread.newFrameSignal.connect(self.mainWindow.onNewFrame)
        self.dataHandlingThread.newFrameSignal.connect(self.calibrationWindow.onNewFrame)
        self.dataHandlingThread.start()
        #lateInit
        self.mainWindow.connect()
    def interWindowConnection(self):
        self.mainWindow.ui.actionRestart.triggered.connect(self.startWindow.show)
        self.mainWindow.ui.actionRestart.triggered.connect(self.mainWindow.hide)
        self.mainWindow.ui.actionControl_Panel.triggered.connect(self.controlPanel.show)
        self.mainWindow.ui.actionDocumentation.triggered.connect(self.documentationWindow.show)
        self.mainWindow.ui.actionConnect.triggered.connect(self.connectionWindow.show)
        self.mainWindow.ui.actionResults.triggered.connect(self.resultsWindow.show)
        self.mainWindow.ui.actionEstimated_Launch_Time.triggered.connect(self.timeWindow.show)
        self.startWindow.accepted.connect(self.mainWindow.applySettings)
        self.startWindow.accepted.connect(self.mainWindow.show)
        self.timeWindow.accepted.connect(self.mainWindow.applySettings)
        self.mainWindow.ui.actionCalibration.triggered.connect(self.calibrationWindow.show)
        self.mainWindow.ui.actionDiagrams.triggered.connect(self.diagramSettingsWindow.show)
    def shutdown(self):
        thread = self.dataHandlingThread
        thread.requestInterruption()
        app = QApplication.instance()
        timeout_ms = 5000
        interval_ms = 50
        waited = 0
        while thread.isRunning() and waited < timeout_ms:
            app.processEvents()
            time.sleep(interval_ms/1000)
            waited += interval_ms
        app.quit()

#Main
if __name__ == "__main__":
    GS = QApplication()
    icon = QIcon("Ressources\\meega_logo_small.ico")
    GS.setWindowIcon(icon)
    translator = QTranslator()
    QLocale.setDefault(QLocale.C)
    collection = ClassCollection()

    #Hier Datahandling (Data Storage Variable)
    if translator.load(collection.settings.locale, "MEEGA_Language"):
        GS.installTranslator(translator)

    #inter-window connections
    collection.interWindowConnection()
    
    #showing the startup screen
    collection.startWindow.show()

    #starting the PyQt Application Loop (everything has to be defined prior to this)
    sys.exit(GS.exec())
#End