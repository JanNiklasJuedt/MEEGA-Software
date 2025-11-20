#imports
from __future__ import annotations
from math import floor
from math import sin, radians
import numpy as np
import sys
import time

from PySide6.QtGui import (QAction, QActionGroup, QIcon, QImage, QPixmap, QPainter)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QMainWindow, QDialog, QWidget, QVBoxLayout)
from PySide6.QtCore import (Signal, Slot, QTranslator, QLocale, QThread, QPointF, QObject)
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
    FLIGHT = 1
    TEST = 0
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
        self.sendCounter = 0
        self.expStartQueue = False

    def newTCFrame(self):
        self.tcframe = DataHandling.CreateTC()
        DataHandling.WriteFrame(self.tcframe, 0, self.collection.settings.mode)

    def sendInit(self):
        self.expStartQueue = False
        self.sendCounter = 10

    def sendStep(self):
        if self.sendCounter > 0:
            DataHandling.AddFrame(self.tcframe)
            self.sendCounter -= 1
        #sending another tc after experiment start to turn off experiment start and prevent multiple starts
        elif self.expStartQueue:
            self.newTCFrame()
            self.collection.controlPanel.updateTCFrame()
            self.sendInit()

#class to define the Main Window
class GSMain(QMainWindow):
    ACTIVE = 1
    ISSUES = 2
    INACTIVE = 0
    NOCONNECTION = 3
    def __init__(self, collection: ClassCollection):
        super().__init__()

        #importing visuals from the ui-file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #creating variables
        self.ACTIVE = 1
        self.ISSUES = 2
        self.INACTIVE = 0
        self.NOCONNECTION = 3
        self.connectionStatus = self.NOCONNECTION
        self.collection = collection

        #creating local status list
        self.statusDisplay = ["" for _ in range(21)]
        self.statusDisplay[0] = self.ui.statusLabelPAmbient
        self.statusDisplay[1] = self.ui.statusLabelTCompare
        self.statusDisplay[2] = self.ui.statusLabelPReservoir
        self.statusDisplay[3] = self.ui.statusLabelTReservoir
        self.statusDisplay[4] = self.ui.statusLabelPAccumulator
        self.statusDisplay[5] = self.ui.statusLabelTChamber1
        self.statusDisplay[6] = self.ui.statusLabelTChamber2
        self.statusDisplay[7] = self.ui.statusLabelPNozzle1
        self.statusDisplay[8] = self.ui.statusLabelTNozzle1
        self.statusDisplay[9] = self.ui.statusLabelPNozzle2
        self.statusDisplay[10] = self.ui.statusLabelTNozzle2
        self.statusDisplay[11] = self.ui.statusLabelPNozzle3
        self.statusDisplay[12] = self.ui.statusLabelTNozzle3
        self.statusDisplay[13] = self.ui.statusLabelServo
        self.statusDisplay[14] = self.ui.statusLabelValve
        self.statusDisplay[15] = self.ui.statusLabelLED
        self.statusDisplay[16] = self.ui.statusLabelPChip
        self.statusDisplay[17] = self.ui.statusLabelTChip
        self.statusDisplay[18] = self.ui.statusLabelMainboard
        self.statusDisplay[19] = self.ui.statusLabelLiftOff
        self.statusDisplay[20] = self.ui.statusLabelSOE

        #creating status pixmaps
        self.activepix = QPixmap("Ressources\\active.png")
        self.issuespix = QPixmap("Ressources\\issues.png")
        self.inactivepix = QPixmap("Ressources\\inactive.png")
        self.noconnectionpix = QPixmap("Ressources\\noconnection.png")

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
            connectionLabelSize = self.ui.connectionLabel.size()
            connectionCircle = min(connectionLabelSize.width(), connectionLabelSize.height())
            self.activepix_connection = self.activepix.scaled(connectionCircle, connectionCircle, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.issuespix_connection = self.issuespix.scaled(connectionCircle, connectionCircle, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.inactivepix_connection = self.inactivepix.scaled(connectionCircle, connectionCircle, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.noconnectionpix_connection = self.noconnectionpix.scaled(connectionCircle, connectionCircle, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        match self.connectionStatus:
            case self.ACTIVE:
                self.ui.connectionLabel.setPixmap(self.activepix_connection)
            case self.ISSUES:
                self.ui.connectionLabel.setPixmap(self.issuespix_connection)
            case self.INACTIVE:
                self.ui.connectionLabel.setPixmap(self.inactivepix_connection)
            case self.NOCONNECTION:
                self.ui.connectionLabel.setPixmap(self.noconnectionpix_connection)

        #sensor / household status
        gatherIndex = self.collection.dataAccumulation.gatherIndex
        statusList = np.concatenate((self.collection.dataAccumulation.household[gatherIndex][0:13], self.collection.dataAccumulation.household[gatherIndex][15:21], self.collection.dataAccumulation.household[gatherIndex][22:24]))
        for i in range(len(self.statusDisplay)):
            match statusList[i]:
                case self.ACTIVE:
                    self.statusDisplay[i].setPixmap(self.activepix_scaled)
                case self.ISSUES:
                    self.statusDisplay[i].setPixmap(self.issuespix_scaled)
                case self.INACTIVE:
                    self.statusDisplay[i].setPixmap(self.inactivepix_scaled)

            mbHealth = self.collection.dataAccumulation.household[gatherIndex][20]
            mbHealth -= 8
            if mbHealth <= 0:
                self.statusDisplay[18].setPixmap(self.inactivepix_scaled)
            elif mbHealth <= 2:
                self.statusDisplay[18].setPixmap(self.issuespix_scaled)
            else:
                self.statusDisplay[18].setPixmap(self.activepix_scaled)

    def createPlots(self):
        #time plot
        #create Line Series for each sensor
        #ambient pressure, compare temperature, accumulator pressure, accumulator temperature, chamber pressure, chamber temperature1, chamber temperature 2, nozzle 1 pressure, nozzle 1 temperature, nozzle 2 pressure, nozzle 2 temperature, nozzle 3 pressure, nozzle 3 temperature
        self.timeSeries = [QLineSeries() for _ in range(13)]

        self.pressureIndices = [0,2,4,7,9,11]
        self.temperatureIndices = [1,3,5,6,8,10,12]

        self.rebuildSignal = Signal()
        self.reducePointsSignal = Signal()

        #value tracking for time plots
        self.timeHighestPres = 0
        self.timeHighestTemp = 0
        self.currentIndex = -1

        #create chart and add Series
        self.timeChart = QChart()
        self.timeChart.legend().setVisible(False)
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
        for i, series in enumerate(self.timeSeries):
            if i in self.pressureIndices:
                series.attachAxis(self.timePressureAxis)
            else:
                series.attachAxis(self.timeTemperatureAxis)
            series.attachAxis(self.timeAxis)
            
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
        self.distanceAxis = QValueAxis()
        self.distancePressureAxis = QValueAxis()
        self.distanceTemperatureAxis = QValueAxis()
        self.distancePressureAxis.setTitleText("pressure in Pa")
        self.distanceTemperatureAxis.setTitleText("temperature in K")
        self.distanceAxis.setRange(0, 5)
        self.distancePressureAxis.setRange(0, self.collection.settings.pressureAxeValue)
        self.distanceTemperatureAxis.setRange(0, self.collection.settings.temperatureAxeValue)
        self.distanceChart.addAxis(self.distancePressureAxis, Qt.AlignBottom)
        self.distanceChart.addAxis(self.distanceTemperatureAxis, Qt.AlignTop)
        self.distanceChart.addAxis(self.distanceAxis, Qt.AlignLeft)
        self.distancePSeries.attachAxis(self.distancePressureAxis)
        self.distancePSeries.attachAxis(self.distanceAxis)
        self.distanceTSeries.attachAxis(self.distanceTemperatureAxis)
        self.distanceTSeries.attachAxis(self.distanceAxis)
        
        #create Layout
        self.distanceLayout = QVBoxLayout(self.ui.distancePlotGroupBox)
        self.distanceLayout.setContentsMargins(0,0,0,0)

        #add Chart to ChartView and Layout
        self.distanceChartView = QChartView(self.distanceChart)
        self.distanceChartView.setRenderHint(QPainter.Antialiasing)
        self.distanceLayout.addWidget(self.distanceChartView)

        self.connectItemsToSeries()
        #self.repaintPlots()

    def extendPlots(self, index: int):
        settings = self.collection.settings
        dataAccu = self.collection.dataAccumulation

        #distance plot
        self.distancePSeries.clear()
        self.distanceTSeries.clear()
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][2], 0)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][4], 1)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][7], 3)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][9], 4)
        self.distancePSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][11], 5)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][3], 0)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][5], 1)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][6], 2)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][8], 3)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][10], 4)
        self.distanceTSeries.append(self.collection.dataAccumulation.sensorData[dataAccu.gatherIndex][12], 5)

        #skip if expanding mode needs an event that hasnt happened yet
        if not (settings.timespanMode == Settings.EXPANDING and(
            (settings.expandFrom == Settings.LO and settings.liftOffIndex == -1) or 
            (settings.expandFrom == Settings.SOE and settings.startOfExperimentIndex == -1)
        )):
            #time plot
            while self.currentIndex < dataAccu.gatherIndex:
                self.currentIndex += 1
                for i, series in enumerate(self.timeSeries):
                    while settings.timespanMode == Settings.SCROLLING and (series.at(series.count()-1).x() - series.at(0).x()) > settings.scrollingTimeSeconds*1000:
                        series.remove(0)
                    if index == self.currentIndex:
                        series.append(dataAccu.household[index][21], dataAccu.sensorData[index][i])
                    else:
                        insertIndex = -1
                        if settings.timespanMode == Settings.EXPANDING and index > settings.liftOffIndex:
                            insertIndex = index - settings.liftOffIndex
                        elif settings.timespanMode == Settings.EXPANDING and index > settings.startOfExperimentIndex:
                            insertIndex = index - settings.startOfExperimentIndex
                        elif settings.timespandMode == Settings.SCROLLING:
                            insertIndex = index - (dataAccu.gatherIndex - series.count())
                        else:
                            insertIndex = index
                        if insertIndex >= 0:
                            series.insert(insertIndex, QPointF(dataAccu.household[index][21], dataAccu.sensorData[index][i]))
                    #save highest pressure for scaling of axes
                    if i in self.pressureIndices: #pressure Value
                        if dataAccu.sensorData[index][i] > self.timeHighestPres:
                            self.timeHighestPres = dataAccu.sensorData[index][i]
                    else: #temperature Value
                        if dataAccu.sensorData[index][i] > self.timeHighestTemp:
                            self.timeHighestTemp = dataAccu.sensorData[index][i]

                self.timeAxis.setRange(self.timeSeries[0].at(0).x(), self.timeSeries[0].at(self.timeSeries[0].count()-1).x())

        if settings.temperatureAxeMode == Settings.SELFSCALING or settings.pressureAxeMode == Settings.SELFSCALING:
            self.updateAxes()

        #self.repaintPlots()

    def repaintPlots(self):
        self.timeChartView.setUpdatesEnabled(True)
        self.timeChartView.blockSignals(False)
        self.distanceChartView.setUpdatesEnabled(True)
        self.distanceChartView.scene().blockSignals(False)
        self.distanceChartView.repaint()
        self.timeChartView.repaint()
        self.distanceChartView.setUpdatesEnabled(False)
        self.distanceChartView.scene().blockSignals(True)
        self.timeChartView.setUpdatesEnabled(False)
        self.timeChartView.blockSignals(True)

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
        tree.topLevelItem(0).child(1).child(1).child(0).setData(0, Qt.UserRole, 5)  # Chamber 1 Temperature
        tree.topLevelItem(0).child(1).child(1).child(1).setData(0,Qt.UserRole,6) #Chamber 2 Temperature
        tree.topLevelItem(0).child(0).child(0).child(0).setData(0, Qt.UserRole, 7)  # Nozzle 1 Pressure
        tree.topLevelItem(0).child(1).child(0).child(0).setData(0, Qt.UserRole, 8)  # Nozzle 1 Temperature
        tree.topLevelItem(0).child(0).child(0).child(1).setData(0, Qt.UserRole, 9)  # Nozzle 2 Pressure
        tree.topLevelItem(0).child(1).child(0).child(1).setData(0, Qt.UserRole, 10)  # Nozzle 2 Temperature
        tree.topLevelItem(0).child(0).child(0).child(2).setData(0, Qt.UserRole, 11)  # Nozzle 3 Pressure
        tree.topLevelItem(0).child(1).child(0).child(2).setData(0, Qt.UserRole, 12)  # Nozzle 3 Temperature

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
        seriesIndex = item.data(0, Qt.UserRole)
        series = self.timeSeries[seriesIndex]
        if item.checkState(0) == Qt.Checked:
            if series not in self.timeChart.series():
                self.timeChart.addSeries(series)
                series.attachAxis(self.timeAxis)
                if seriesIndex in self.pressureIndices:
                    series.attachAxis(self.timePressureAxis)
                else:
                    series.attachAxis(self.timeTemperatureAxis)
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
        self.ledState = 1
        self.collection.telecommand.newTCFrame()
        self.updateTCFrame()
        self.collection.telecommand.sendInit()
    @Slot()
    def offLED(self):
        self.ledState = 0
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
        self.collection.telecommand.expStartQueue = True
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
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Valve_Delay, (self.valveDelay.minute()*60 + self.valveDelay.second())*1000 + self.valveDelay.msec())
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Servo_Delay, (self.servoDelay.minute()*60 + self.servoDelay.second())*1000 + self.servoDelay.msec())
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.EoE_Delay, (self.EOEDelay.minute()*60 + self.EOEDelay.second())*1000 + self.EOEDelay.msec())
        #PowerOffDelay fehlt
        #NozzleOnDelay fehlt
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Dry_Run, self.dryRunActive)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.LED_Control, self.ledState)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Servo_Control, floor(self.servoAngle))
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Valve_Control, self.valveControl)
        #Camera control fehlt
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Test_Abort, self.testRunStop)
        DataHandling.WriteFrame(self.collection.telecommand.tcframe, TCID.Test_Run, self.testRunStart)
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
        self.calibrationPoints = [[0] * 3 for x in range(13)]

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
        mappedValue = self.collection.dataAccumulation.sensorData[self.collection.dataAccumulation.gatherIndex][self.selectedSensor]
        self.ui.label.setText(str(mappedValue) + " " + self.currentUnit)
    
    #select sensor and display already existing calibration points, according Units
    @Slot()
    def selectSensor(self):
        self.selectedSensor = self.ui.comboBox.currentIndex()
        self.ui.lineEdit.setText(str(self.calibrationPoints[self.selectedSensor][0]))
        self.ui.lineEdit_2.setText(str(self.calibrationPoints[self.selectedSensor][1]))
        self.ui.lineEdit_3.setText(str(self.calibrationPoints[self.selectedSensor][2]))
        if self.selectedSensor in self.collection.mainWindow.pressureIndices:
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
    rebuildSignal = Signal()

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
            self.rebuildSignal.emit()
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
        self.rebuildSignal.connect(self.collection.plotWorker.rebuildPlot)

class DataAccumulation(QObject):
    newFrameSignal = Signal(int)

    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.collection = collection
        self.gatherIndex = -1
        self.newIndex = -1
        self.allocationSize = 5000
        self.sensorData = np.ones((self.allocationSize, 13))
        self.household = np.ones((self.allocationSize, 27))

    def accumulate(self):
        testData = False

        #Get Frame and check connection status
        if not testData:
            if DataHandling.PortIsOpen():
                self.collection.mainWindow.connectionStatus = GSMain.INACTIVE
            else:
                self.collection.mainWindow.connectionStatus = GSMain.NOCONNECTION
        while True:
            if not testData:
                frame = DataHandling.GetNextFrame()
                if DataHandling.FrameIsEmpty(frame):
                    self.newFrameSignal.emit(int(self.newIndex))
                    break
                if DataHandling.FrameHasFlag(frame, Flag.OK):
                    self.collection.mainWindow.connectionStatus = GSMain.ACTIVE
                    self.gatherIndex += 1
                else:
                    self.collection.mainWindow.connectionStatus = GSMain.ISSUES
                    self.newFrameSignal.emit(int(self.newIndex))
                    break
            else:
                ###
                self.gatherIndex += 1 ###only for testing purposes###
                ###
            #extend arrays if necessary
            if self.gatherIndex%self.allocationSize == 0:
                dataExtension = np.ones((self.allocationSize, 13))
                householdExtension = np.ones((self.allocationSize, 27))
                self.sensorData = np.concatenate((self.sensorData, dataExtension))
                self.household = np.concatenate((self.household, householdExtension))
            if not testData:
                if self.gatherIndex <= 0 or DataHandling.ReadFrame(frame, TMID.System_Time) > self.household[self.gatherIndex][21]:
                    self.newIndex = self.gatherIndex
                else:
                    self.newIndex = np.searchsorted(self.household[:self.gatherIndex, 21], DataHandling.ReadFrame(frame, TMID.System_Time))
            else:
                ###
                self.newIndex = self.gatherIndex ###only for testing purposes###
                ###
            for i in range(13):
                if testData:
                    ###
                    self.sensorData[self.newIndex][i] = int(150*sin(radians((10*self.gatherIndex)%360 + 10*i))+150) ###only for testing purposes###
                    ###
                else:
                    self.sensorData[self.newIndex][i] = DataHandling.MapSensorValue(i, DataHandling.ReadFrame(frame, i))
            if testData:
                ###
                self.household[self.newIndex][21] = 1000/self.collection.dataHandlingThread.frequency*self.gatherIndex  ###only for testing purposes###
                ###
            else:
                for i in range(13):
                    self.household[self.newIndex][i] = DataHandling.ReadFrame(frame, 13+i)
                self.household[self.newIndex][13] = DataHandling.ReadFrame(frame, TMID.Nozzle_Open)
                self.household[self.newIndex][14] = DataHandling.ReadFrame(frame, TMID.Nozzle_Closed)
                self.household[self.newIndex][15] = DataHandling.ReadFrame(frame, TMID.Nozzle_Servo)
                self.household[self.newIndex][16] = DataHandling.ReadFrame(frame, TMID.Reservoir_Valve)
                self.household[self.newIndex][17] = DataHandling.ReadFrame(frame, TMID.LEDs)
                self.household[self.newIndex][18] = DataHandling.ReadFrame(frame, TMID.Sensorboard_P)
                self.household[self.newIndex][19] = DataHandling.ReadFrame(frame, TMID.Sensorboard_T)
                self.household[self.newIndex][20] = DataHandling.ReadFrame(frame, TMID.Mainboard)
                self.household[self.newIndex][21] = DataHandling.ReadFrame(frame, TMID.System_Time)
                self.household[self.newIndex][22] = DataHandling.ReadFrame(frame, TMID.Lift_Off)
                self.household[self.newIndex][23] = DataHandling.ReadFrame(frame, TMID.Start_Experiment)
                self.household[self.newIndex][24] = DataHandling.ReadFrame(frame, TMID.End_Experiment)
                self.household[self.newIndex][25] = DataHandling.ReadFrame(frame, TMID.Mode)
                self.household[self.newIndex][26] = DataHandling.ReadFrame(frame, TMID.Experiment_State)

                if self.gatherIndex > 0:
                    if self.household[self.gatherIndex - 1][22] == 0 and self.household[self.gatherIndex][22] == 1:
                        self.collection.settings.liftOffIndex = self.gatherIndex
                    if self.household[self.gatherIndex -1][23] == 0 and self.household[self.gatherIndex][23] == 1:
                        self.collection.settings.startOfExperimentIndex = self.gatherIndex
            self.newFrameSignal.emit(int(self.newIndex))
            if testData:
                ###
                break ###only for testing purposes###
                ###

class PlotWorker(QThread):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.collection = collection

    def rebuildPlot(self):
        settings = self.collection.settings
        dataAcc = self.collection.dataAccumulation
        sensorData = dataAcc.sensorData
        household = dataAcc.household
        clear = False
        mainWindow = self.collection.mainWindow

        startIndex = 0
        endIndex = dataAcc.gatherIndex
        if settings.timespanMode == Settings.EXPANDING:
            match settings.expandFrom:
                case Settings.LO:
                    if settings.liftOffIndex != -1:
                        startIndex = settings.liftOffIndex
                    else:
                        clear = True
                case Settings.SOE:
                    if settings.startOfExperimentIndex != -1:
                        startIndex = settings.startOfExperimentIndex
                    else:
                        clear = True
        else:
            startIndex = max(0, dataAcc.gatherIndex - (self.collection.dataHandlingThread.frequency * settings.scrollingTimeSeconds))

        if endIndex <= startIndex:
            clear = True

        if clear:
            for s in mainWindow.timeSeries:
                s.clear()
            return
        
        if startIndex == 0:
            xValues = household[:endIndex, 21]
            yMatrix = sensorData[:endIndex, :13]
        else:
            xValues = np.ascontiguousarray(household[startIndex:endIndex, 21])
            yMatrix = np.ascontiguousarray(sensorData[startIndex:endIndex, :13])

        for i in range(13):
            yValues =  yMatrix[:, i]
            points = [QPointF(x, y) for x, y in zip(xValues, yValues)]
            mainWindow.timeSeries[i].replace(points)
        self.collection.mainWindow.currentIndex = dataAcc.gatherIndex
        self.collection.mainWindow.timeHighestPres = np.max(yMatrix[startIndex:endIndex, self.collection.mainWindow.pressureIndices])
        self.collection.mainWindow.timeHighestTemp = np.max(yMatrix[startIndex:endIndex, self.collection.mainWindow.temperatureIndices])
        #self.collection.mainWindow.repaintPlots()

class DataHandlingThread(QThread):
    def __init__(self, collection: ClassCollection):
        super().__init__()
        self.collection = collection
        self.frequency = 20
    def run(self):
        period_ms = 1000 / self.frequency
        i = 0
        times = [0]*50
        DataHandling.Initialize()
        while True:
            clock = time.monotonic_ns()
            DataHandling.DebugLastFrame()
            DataHandling.UpdateAll()
            # clock2 = time.monotonic_ns()
            # print("DataHandlingUpdate-time: " + str((clock2-clock)/1000000))
            self.collection.dataAccumulation.accumulate()
            # clock3 = time.monotonic_ns()
            # print("dataAcc-time: " + str((clock3-clock2)/1000000))
            self.collection.telecommand.sendStep()
            # clock4 = time.monotonic_ns()
            # print("tc-time: " + str((clock4-clock3)/1000000))
            # clock5 = time.monotonic_ns()
            # print("signal-emit-time: " + str((clock5-clock4)/1000000))
            if self.isInterruptionRequested():
                DataHandling.CloseAll()
                break
            endTime = time.monotonic_ns()
            # print(period_ms-(endTime - clock)/1000000)
            if (endTime - clock)/1000000 < period_ms:
                time.sleep((period_ms - (endTime - clock) / 1000000)/1000)
            clock6 = time.monotonic_ns()
            # print("rest-time: " + str((clock6-clock5)/1000000))
            times[i] = (clock6-clock)/1000000
            i += 1
            if i == 50:
                average = 0
                for timeVal in times:
                    average += timeVal
                average = average/50
                print("DataHandling Loop-time average: " + str(average) + " with " + str(self.collection.dataAccumulation.gatherIndex + 1) + " points\n")
                i = 0

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
        self.plotWorker = PlotWorker(self)
        self.diagramSettingsWindow = GSDiagramSettings(self)
        #connect onNewFrame signals
        self.dataAccumulation.newFrameSignal.connect(self.mainWindow.onNewFrame)
        self.dataAccumulation.newFrameSignal.connect(self.calibrationWindow.onNewFrame)
        #DataHandling setup
        self.dataHandlingThread = DataHandlingThread(self)
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