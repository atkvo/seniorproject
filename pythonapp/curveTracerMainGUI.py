#!/usr/bin/env python3
"""
Curve Tracer GUI
================

Embedded pyplot?
"""
import sys
import curveTracerSerial
import curveTracerSweeper as cts
from PyQt4 import QtGui


# If Menubar desired, use QtGui.QMainWindow
class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        #### MSP CONNECTION CONFIG #########################
        self.mspConfigPortBox = QtGui.QLineEdit(self)
        self.mspConfigPortBox.setText("/dev/ttyACM1")
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
        btnTest = QtGui.QPushButton("TEST")
        # btnTest.clicked.connect(self.tester)
        btnTest.clicked.connect(self.sweepVoltageAction)
        gridConnect = QtGui.QGridLayout()
        gridConnect.addWidget(self.mspConfigPortBox, 0, 0)
        gridConnect.addWidget(self.mspConfigBaudBox, 0, 1)
        gridConnect.addWidget(self.btnMspConnect, 0, 2)
        ############################################
        gridConnect.addWidget(btnTest, 0, 3) ##########
        ############################################
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
        # self.sweepVoltageMin.setFixedWidth(50)
        self.sweepVoltageMin.setMinimumWidth(50)
        self.sweepVoltageMin.setText("-1000")
        # self.sweepVoltageMin.setAlignment(QtCore.Qt.AlignCenter)

        sweepVoltageMaxLabel = QtGui.QLabel("Max Voltage (mV)")
        self.sweepVoltageMax = QtGui.QLineEdit(self)
        self.sweepVoltageMax.setMinimumWidth(50)

        # self.sweepVoltageMax.setFixedWidth(50)

        sweepVoltageIncrLabel = QtGui.QLabel("Increment %")
        self.sweepVoltageIncr = QtGui.QLineEdit(self)
        self.sweepVoltageIncr.setText("5")
        # self.sweepVoltageIncr.setFixedWidth(40)
        self.sweepVoltageIncr.setMinimumWidth(40)

        self.btnSweepCommand = QtGui.QPushButton("SWEEP")
        self.btnSweepCommand.clicked.connect(self.sweepVoltageAction)
        self.btnSweepCommand.setFixedWidth(60)

        # self.tempCheck = QtGui.QCheckBox()
        # self.tempCheckLabel = QtGui.QLabel("Temperature?")
        gridSweeper.addWidget(sweepVoltageMinLabel, 0, 0)
        gridSweeper.addWidget(self.sweepVoltageMin, 0, 1)
        gridSweeper.addWidget(sweepVoltageMaxLabel, 0, 2)
        gridSweeper.addWidget(self.sweepVoltageMax, 0, 3)
        gridSweeper.addWidget(sweepVoltageIncrLabel, 0, 4)
        gridSweeper.addWidget(self.sweepVoltageIncr, 0, 5)
        gridSweeper.addWidget(self.btnSweepCommand, 0, 6)
        # gridSweeper.addWidget(self.tempCheckLabel, 1, 1)
        # gridSweeper.addWidget(self.tempCheck, 1, 0, QtCore.Qt.AlignRight)
        self.groupSweeper.setLayout(gridSweeper)

        #### STATUS GROUP ###################################
        self.groupStatus = QtGui.QGroupBox("Statuses")
        gridStatus = QtGui.QGridLayout()

        measuredVoltageLabel = QtGui.QLabel("Voltage: ")
        self.measuredVoltage = QtGui.QLineEdit(self)
        self.measuredVoltage.setReadOnly(True)

        measuredCurrentLabel = QtGui.QLabel("Current: ")
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

    def tester(self):
        maxV = self.sweepVoltageMax.text()
        minV = self.sweepVoltageMin.text()
        incr = self.sweepVoltageIncr.text()
        #     tSweep = cts.SweeperThread(self.mspInst, minV, maxV)
        c = cts.SweeperThread(minV, maxV, incr)

        c.begin()
        # c.start()
        print("ok")

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
        self.tester()
        # sender = self.sender()
        # if sender.text() == "SWEEP":
        #     maxV = self.sweepVoltageMax.text()
        #     minV = self.sweepVoltageMin.text()
        #     tSweep = cts.SweeperThread(self.mspInst, minV, maxV)
        #     tSweep.initThread()     # START SWEEPER THREAD HERE
        #     self.btnSweepCommand.setText("STOP")
        #     self.toggleSweepField("OFF")
        # elif sender.text() == "STOP":
        #     self.toggleSweepField("ON")
        #     self.btnSweepCommand.setText("SWEEP")
        #     # KILL THREAD HERE tSweep.kill() ?

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
            self.tempCheck.setEnabled(True)
        elif value == "OFF":
            self.sweepVoltageMin.setEnabled(False)
            self.sweepVoltageMax.setEnabled(False)
            self.tempCheck.setEnabled(False)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
