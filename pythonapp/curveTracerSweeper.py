#!/usr/bin/env python3
from PyQt4 import QtCore, QtGui
import platform
import array

if platform.system() == "Windows":
    SLEEP_CMD = ['python', '-c', 'import time\ntime.sleep(5)']
else:
    SLEEP_CMD = ['sleep', '5']


class SweepThread(QtCore.QThread):
# class SweeperThread(QtCore.QObject):

    signalSweepDone = QtCore.pyqtSignal(bool)
    signalUpdateStats = QtCore.pyqtSignal(str, float)

    def __init__(self, mutex, mspInstance, minV, maxV, incr):
    # def __init__(self, minV, maxV, incr):
    # Should also take sweep increment % also
        super(SweepThread, self).__init__()
        self.exiting = False
        self.mutex = mutex
        self.minV = int(minV)
        self.maxV = int(maxV)
        self.incrStep = round(4096*(int(incr)/100))  # 4096 * inc%
        self.mspInst = mspInstance
        self.numberOfDataPoints = round(4096/self.incrStep)
        self.voltageArray = array.array('f')
        self.currentArray = array.array('f')
        print("incr step is: ", self.incrStep)
        print("number of data points: ", self.numberOfDataPoints)

    def __del__(self):
        self.exiting = True
        # self.wait()
        # self.emit.finished("DONE")
        self.signalSweepDone.emit(True)
        print("Exited")

    def run(self):  # NOTE: NEVER call this function directly
    # TODO: This therad is blocking the main GUI. Figure it out.
        self.signalSweepDone.emit(False)
        measuredVoltage = 0
        measuredCurrent = 0
        dacCommand = 0          # from 0 - 4095
        i = 0
        while measuredVoltage < self.maxV and i < self.numberOfDataPoints:
            dacCommand = dacCommand + self.incrStep
            self.sendVoltage(dacCommand)
            self.msleep(10)
            QtGui.qApp.processEvents()
            measuredVoltage = self.readVoltage()
            measuredVoltage = self.convertRaw(measuredVoltage, "VOLTAGE")
            print("Measured voltage: ", measuredVoltage)
            self.signalUpdateStats.emit("VOLTAGE", measuredVoltage)
            self.voltageArray.append(measuredVoltage)

            self.msleep(10)
            QtGui.qApp.processEvents()
            measuredCurrent = self.readCurrent()
            measuredCurrent = self.convertRaw(measuredCurrent, "VOLTAGE")
            print("Measured current: ", measuredCurrent)
            self.signalUpdateStats.emit("CURRENT", measuredCurrent)
            self.currentArray.append(measuredCurrent)

            i = i + 1
        self.signalSweepDone.emit(True)
        # When reading voltage, make sure to use int()
        # to convert to integer to be able to do math
        # operations on it.

    def readVoltage(self):
        self.mspInst.sendCommand("V?")
        self.mspInst.read()
        self.mspInst.sendCommand("V?")
        return(self.mspInst.read())

    def readCurrent(self):
        self.mspInst.sendCommand("C?")
        self.mspInst.read()
        self.mspInst.sendCommand("C?")
        return(self.mspInst.read())

    def sendVoltage(self, raw):
        command = "V="
        digits = len(str(raw))
        zeroes = 4 - digits
        for i in range(zeroes):     # prepends 0's to make value 4 digits
            command = command + "0"
        command = command + str(raw)
        self.mspInst.sendCommand(command)

    def begin(self):
        self.start()

    def stopSweep(self):
        print("Attempting to kill thread")
        """ Should cleanly kill sweep on mutex unlock"""

    def convertRaw(self, rawValue, type):
        VCC = 5.47
        """ Convert raw adc voltage to real voltage"""
        rawValue = int(rawValue)
        ratio = 0
        if type == "VOLTAGE":
            if rawValue < 4096:
                # positive voltage (0-10V)
                ratio = int(rawValue)/4096
                # voltage = ratio * 10
                voltage = ratio * VCC*2000     # get voltage in terms of mV
            elif rawValue >= 4096:
                rawValue = 8192 - rawValue
                # convert scaling (0->0V, 4096-> -10V)
                # be sure to multiply final value by (-1)
                ratio = int(rawValue)/4096
                # voltage = -1 * (ratio * 10)
                voltage = -1 * (ratio * VCC*2000)
            return voltage

    def getResults(self):
        return self.voltageArray, self.currentArray
