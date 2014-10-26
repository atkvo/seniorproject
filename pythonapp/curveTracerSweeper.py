#!/usr/bin/env python3
from PyQt4 import QtCore, QtGui
import platform

if platform.system() == "Windows":
    SLEEP_CMD = ['python', '-c', 'import time\ntime.sleep(5)']
else:
    SLEEP_CMD = ['sleep', '5']


class SweeperThread(QtCore.QThread):

    def __init__(self, mutex, mspInstance, minV, maxV, incr):
    # def __init__(self, minV, maxV, incr):
    # Should also take sweep increment % also
        super(SweeperThread, self).__init__()
        self.mutex = mutex
        self.minV = int(minV)
        self.maxV = int(maxV)
        self.incrStep = round(4096*(int(incr)/100))
        self.mspInst = mspInstance
        print("incr step is: ", self.incrStep)

    def __del__(self):
        self.exiting = True
        self.wait()
        print("Exited")

    def run(self):  # NOTE: NEVER call this function directly
    # TODO: This therad is blocking the main GUI. Figure it out.
        measuredVoltage = 0
        measuredCurrent = 0
        dacCommand = 0          # from 0 - 4095

        while measuredVoltage < self.maxV:
            dacCommand = dacCommand + self.incrStep
            self.sendVoltage(dacCommand)
            self.msleep(10)
            QtGui.qApp.processEvents()
            measuredVoltage = self.readVoltage()
            measuredVoltage = self.convertRaw(measuredVoltage, "VOLTAGE")
            print("Measured voltage: ", measuredVoltage)

            self.msleep(10)
            QtGui.qApp.processEvents()
            measuredCurrent = self.readCurrent()
            measuredCurrent = self.convertRaw(measuredCurrent, "VOLTAGE")
            print("Measured current: ", measuredCurrent)

            # When reading voltage, make sure to use int()
            # to convert to integer to be able to do math
            # operations on it.

    def readVoltage(self):
        self.mutex.lock()
        self.mspInst.sendCommand("V?")
        self.mspInst.read()
        self.mspInst.sendCommand("V?")
        self.mutex.unlock()
        return(self.mspInst.read())

    def readCurrent(self):
        self.mutex.lock()
        self.mspInst.sendCommand("C?")
        self.mspInst.read()
        self.mspInst.sendCommand("C?")
        self.mutex.unlock()
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

    def killme(self):
        self.terminate()

    def sweepLoop(self):
        self.mspInst.sendCommand("V?")
        """ SWEEP LOOP & LOG HERE
            Loop is done whenever maxV is reached.
                Autokill thread
                Be able to signal to main app that sweep is done
        """

    def sweepStop(self):
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
        """ Return grabbed values"""

    def non_blocking(self):
        self.setMessage("Starting non blocking sleep")
        process = QtCore.QProcess(parent=self.win)
        process.setProcessChannelMode(process.ForwardedChannels)
        process.finished.connect(self.finished)
        # process.start('sleep', ['5'])
        process.start(SLEEP_CMD[0], SLEEP_CMD[1:])
