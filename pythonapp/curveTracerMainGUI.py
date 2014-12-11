#!/usr/bin/env python3
"""
Curve Tracer GUI
================

Embedded pyplot?
"""
import sys
import curveTracerSerial
import curveTracerSweeper as cts
import csv
import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        QtCore.pyqtRemoveInputHook()
        self.mutex = QtCore.QMutex()
        self.initUI()

    def initUI(self):

        #### MSP CONNECTION CONFIG #########################
        self.mspConfigPortBox = QtGui.QLineEdit(self)
        if sys.platform == "win32":
            self.mspConfigPortBox.setText("COM1")
        else:
            self.mspConfigPortBox.setText("/dev/ttyUSB0")
        self.mspConfigBaudBox = QtGui.QLineEdit(self)
        self.mspConfigBaudBox.setText("9600")

        #### MSP COMMAND STUFF #############################
        self.btnMspConnect = QtGui.QPushButton("CONNECT")
        self.btnMspConnect.clicked.connect(self.mspConnect)

        self.btnSendCommand = QtGui.QPushButton("SEND")
        self.btnSendCommand.clicked.connect(self.mspSend)

        self.commandBox = QtGui.QLineEdit(self)
        self.commandBox.setText("CMD?")

        #### CURVE TRACE APP MAIN LAYOUT ###################
        vbox = QtGui.QVBoxLayout()

        #### CURVE TRACE APP CONNECTION ####################
        self.mspConnectGroup = QtGui.QGroupBox("Connection")
        self.mspConnectGroup.setFlat(False)
        # btnTest = QtGui.QPushButton("TEST")
        # btnTest.clicked.connect(self.tester)
        # btnTest.clicked.connect(self.sweepVoltageAction)
        gridConnect = QtGui.QGridLayout()
        gridConnect.addWidget(self.mspConfigPortBox, 0, 0)
        gridConnect.addWidget(self.mspConfigBaudBox, 0, 1)
        gridConnect.addWidget(self.btnMspConnect, 0, 2)

        self.mspConnectGroup.setLayout(gridConnect)

        #### CURVE TRACE APP COMMANDS ######################
        mspCommandGroup = QtGui.QGroupBox("Send Manual Command")
        mspCommandGroup.setFlat(False)
        gridCommand = QtGui.QGridLayout()
        gridCommand.addWidget(self.commandBox, 0, 0, 0, 1)
        gridCommand.addWidget(self.btnSendCommand, 0, 2)
        mspCommandGroup.setLayout(gridCommand)

        #### SWEEPER GROUP #################################
        self.groupSweeper = QtGui.QGroupBox("Sweeper Settings")
        gridSweeper = QtGui.QGridLayout()

        sweepVoltageMinLabel = QtGui.QLabel("Min Voltage (mV)")
        self.sweepVoltageMin = QtGui.QLineEdit(self)
        self.sweepVoltageMin.setMinimumWidth(50)
        self.sweepVoltageMin.setText("-1000")
        # self.sweepVoltageMin.setAlignment(QtCore.Qt.AlignCenter)

        sweepVoltageMaxLabel = QtGui.QLabel("Max Voltage (mV)")
        self.sweepVoltageMax = QtGui.QLineEdit(self)
        self.sweepVoltageMax.setText("1000")
        self.sweepVoltageMax.setMinimumWidth(50)

        sweepVoltageIncrLabel = QtGui.QLabel("Step Size (mV)")
        self.sweepVoltageIncr = QtGui.QLineEdit(self)
        self.sweepVoltageIncr.setText("10")
        self.sweepVoltageIncr.setMinimumWidth(40)

        self.btnSweepCommand = QtGui.QPushButton("SWEEP")
        self.btnSweepCommand.clicked.connect(self.sweepVoltageAction)
        self.btnSweepCommand.setFixedWidth(60)

        self.sweepSampleRateLabel = QtGui.QLabel("Sample Rate (x_)")
        self.sweepSampleRate = QtGui.QLineEdit(self)
        self.sweepSampleRate.setText("2")
        self.sweepSampleRate.setFixedWidth(60)

        self.vcc5VoltageLabel = QtGui.QLabel("5V Value (V)")
        self.vcc5Voltage = QtGui.QLineEdit(self)
        self.vcc5Voltage.setText("5.00")
        self.vcc5Voltage.setFixedWidth(50)

        self.vcc3VoltageLabel = QtGui.QLabel("3.3V Value (V)")
        self.vcc3Voltage = QtGui.QLineEdit(self)
        self.vcc3Voltage.setText("3.30")
        self.vcc3Voltage.setFixedWidth(50)

        self.currentGainLabel = QtGui.QLabel("Shunt Resistor Gain")
        self.currentGain = QtGui.QLineEdit(self)
        self.currentGain.setText("-50")
        self.currentGain.setFixedWidth(50)

        self.btnExportLog = QtGui.QPushButton("Export")
        self.btnExportLog.clicked.connect(self.btnExportLogAction)
        self.btnExportLog.setFixedWidth(60)
        self.btnExportLog.setEnabled(False)  # Cannot export log without a run

        # self.tempCheck = QtGui.QCheckBox()
        # self.tempCheckLabel = QtGui.QLabel("Temperature?")
        gridSweeper.addWidget(sweepVoltageMaxLabel, 0, 0)
        gridSweeper.addWidget(self.sweepVoltageMax, 0, 1)
        gridSweeper.addWidget(sweepVoltageMinLabel, 1, 0)
        gridSweeper.addWidget(self.sweepVoltageMin, 1, 1)
        gridSweeper.addWidget(self.vcc5VoltageLabel, 2, 0)
        gridSweeper.addWidget(self.vcc5Voltage, 2, 1)
        gridSweeper.addWidget(self.vcc3VoltageLabel, 3, 0)
        gridSweeper.addWidget(self.vcc3Voltage, 3, 1)
        gridSweeper.addWidget(self.currentGainLabel, 4, 0)
        gridSweeper.addWidget(self.currentGain, 4, 1)
        gridSweeper.addWidget(sweepVoltageIncrLabel, 0, 4)
        gridSweeper.addWidget(self.sweepVoltageIncr, 0, 5)
        gridSweeper.addWidget(self.sweepSampleRateLabel, 1, 4)
        gridSweeper.addWidget(self.sweepSampleRate, 1, 5)
        gridSweeper.addWidget(self.btnSweepCommand, 3, 6)
        gridSweeper.addWidget(self.btnExportLog, 4, 6)
        self.groupSweeper.setLayout(gridSweeper)

        #### STATUS GROUP ###################################
        self.groupStatus = QtGui.QGroupBox("Sweep Status")
        gridStatus = QtGui.QGridLayout()

        measuredVoltageLabel = QtGui.QLabel("Voltage [mV]")
        self.measuredVoltage = QtGui.QLineEdit(self)
        self.measuredVoltage.setReadOnly(True)

        measuredCurrentLabel = QtGui.QLabel("Current [mA]")
        self.measuredCurrent = QtGui.QLineEdit(self)
        self.measuredCurrent.setReadOnly(True)

        gridStatus.addWidget(measuredVoltageLabel, 0, 0)
        gridStatus.addWidget(self.measuredVoltage, 0, 1)
        gridStatus.addWidget(measuredCurrentLabel, 1, 0)
        gridStatus.addWidget(self.measuredCurrent, 1, 1)
        self.groupStatus.setLayout(gridStatus)

        #### VBOX LAYOUT
        vbox.addWidget(self.mspConnectGroup)
        vbox.addWidget(mspCommandGroup)
        vbox.addWidget(self.groupSweeper)
        vbox.addWidget(self.groupStatus)
        self.setLayout(vbox)
        self.show()

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Curve Tracer Prototype')

        self.toggleCommandField("OFF")
        self.toggleConnectField("ON")
        self.show()

    def mspConnect(self):
        source = self.sender()
        if source.text() == "CONNECT":
            port = self.mspConfigPortBox.text()
            rate = self.mspConfigBaudBox.text()
            self.mspInst = curveTracerSerial.Connection(port, rate)
            self.btnMspConnect.setText("DISCONNECT")
            self.toggleConnectField("OFF")
        elif source.text() == "DISCONNECT":
            self.mspInst.close()
            del self.mspInst
            self.btnMspConnect.setText("CONNECT")
            self.toggleConnectField("ON")

    def sweepVoltageAction(self):
        sender = self.sender()
        senderName = sender.text()
        if senderName == "SWEEP":
            maxV = self.sweepVoltageMax.text()
            minV = self.sweepVoltageMin.text()
            incr = self.sweepVoltageIncr.text()
            sampleRate = self.sweepSampleRate.text()
            vcc5Voltage = self.vcc5Voltage.text()
            vcc3Voltage = self.vcc3Voltage.text()
            currentGain = self.currentGain.text()
            try:
                self.c = cts.SweepThread(self.mutex, self.mspInst,
                                         minV, maxV, incr, sampleRate,
                                         vcc5Voltage, vcc3Voltage, currentGain)
                self.c.signalSweepDone.connect(self.sweepDoneAction)
                self.c.signalUpdateStats.connect(self.updateStats)
                self.c.begin()
            except:
                print("unable to start")
        elif senderName == "STOP":
            try:
                self.c.stopSweep()
                # del self.c
                self.toggleSweepField("ON")
                self.btnSweepCommand.setText("SWEEP")
            except:
                print("Could not kill process")

    def sweepDoneAction(self, check):
        if check is False:
            self.btnSweepCommand.setText("STOP")
            self.toggleSweepField("OFF")
        elif check is True:
            print("voltage", self.voltageArray)
            print("current", self.currentArray)
            self.toggleSweepField("ON")
            self.btnExportLog.setEnabled(True)
            self.btnSweepCommand.setText("SWEEP")

    def btnExportLogAction(self):
        csvFile = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '.')
        print(csvFile)
        with open(csvFile, 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(('VOLTAGE [mV]', 'CURRENT [mA]'))
            for i in range(len(self.voltageArray)):
                a.writerow((self.voltageArray[i], self.currentArray[i]))

    def updateStats(self, type, value):
        valueRounded = round(value, 4)
        if type == "VOLTAGE":
            self.measuredVoltage.setText(str(valueRounded) + " mV")
            self.voltageArray.append(value)
        elif type == "CURRENT":
            self.measuredCurrent.setText(str(valueRounded) + " mA")
            self.currentArray.append(value)
            for i in range(len(self.currentArray)):
                ax = self.figure.add_subplot(111)
                ax.hold(False)
                ax.plot(self.voltageArray[0:i], self.currentArray[0:i])
                ax.set_title('SOLAR CELL IV CURVE')
                ax.set_xlabel('VOLTAGE [mV]')
                ax.set_ylabel('CURRENT [mA]')
                self.canvas.draw()
        elif type == "SIZE":
            self.voltageArray = array.array('f')
            self.currentArray = array.array('f')
            self.figure = plt.figure()
            self.canvas = FigCanvas(self.figure)
            self.canvas.show()

    def mspSend(self):
        command = self.commandBox.text()
        self.mspInst.sendCommand(command)
        print(self.mspInst.read())

    def toggleConnectField(self, value):
        if value == "ON":
            self.mspConfigBaudBox.setEnabled(True)
            self.mspConfigPortBox.setEnabled(True)
            self.toggleCommandField("OFF")
        elif value == "OFF":
            self.toggleCommandField("ON")
            self.mspConfigBaudBox.setEnabled(False)
            self.mspConfigPortBox.setEnabled(False)

    def toggleCommandField(self, value):
        if value == "ON":
            self.btnSendCommand.setEnabled(True)
            self.commandBox.setEnabled(True)
            self.groupSweeper.setEnabled(True)
        elif value == "OFF":
            self.btnSendCommand.setEnabled(False)
            self.commandBox.setEnabled(False)
            self.groupSweeper.setEnabled(False)

    def toggleSweepField(self, value):
        if value == "ON":
            self.sweepVoltageMin.setEnabled(True)
            self.sweepVoltageMax.setEnabled(True)
        elif value == "OFF":
            self.sweepVoltageMin.setEnabled(False)
            self.sweepVoltageMax.setEnabled(False)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
