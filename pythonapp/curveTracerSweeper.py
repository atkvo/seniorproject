#!/usr/bin/env python3
from PyQt4 import QtCore, QtGui
import array


class SweepThread(QtCore.QThread):

    signalSweepDone = QtCore.pyqtSignal(bool)
    signalUpdateStats = QtCore.pyqtSignal(str, float)

    def __init__(self, mutex, mspInstance, minV, maxV, incr):
        super(SweepThread, self).__init__()
        self.exiting = False
        self.mutex = mutex
        self.minV = int(minV)
        self.maxV = int(maxV)
        self.incrStep = round(4096*(float(incr)/100))  # 4096 * incr%
        self.mspInst = mspInstance
        self.numberOfDataPoints = round(4096/self.incrStep)
        print("incr step is: ", self.incrStep)
        print("number of data points: ", self.numberOfDataPoints)

    def __del__(self):
        self.exiting = True
        self.signalSweepDone.emit(True)
        print("Exited")

    def run(self):  # NOTE: NEVER call this function directly, use start()
        self.signalUpdateStats.emit("SIZE", self.numberOfDataPoints)
        self.signalSweepDone.emit(False)
        measuredVoltage = 0
        measuredCurrent = 0
        currentArray = array.array('f')
        voltageArray = array.array('f')
        dacCommand = self.a2d(self.minV)
        self.stop = False
        i = 0
        while measuredVoltage < self.maxV \
                and i < self.numberOfDataPoints \
                and self.stop is False \
                and dacCommand < 4096:
            measuredVoltage = 0
            measuredCurrent = 0
            self.sendVoltage(dacCommand)
            self.msleep(10)
            QtGui.qApp.processEvents()
            # measuredVoltage = self.readVoltage()
            for n in range(4):
                # find outlier here
                voltageArray.insert(n, int(self.readVoltage()))
                print("READV: ", voltageArray[n])
                measuredVoltage = int(voltageArray[n]) + measuredVoltage
                self.msleep(10)
            measuredVoltage = measuredVoltage/4
            print("VOLTAGE1: ", measuredVoltage)
            measuredVoltage = self.convertRaw(measuredVoltage, "VOLTAGE")
            self.signalUpdateStats.emit("VOLTAGE", measuredVoltage)

            self.msleep(10)
            QtGui.qApp.processEvents()
            # measuredCurrent = self.readCurrent()
            for n in range(4):
                # find outlier here
                currentArray.insert(n, int(self.readCurrent()))
                print("READC: ", currentArray[n])
                measuredCurrent = int(currentArray[n]) + measuredCurrent
                self.msleep(10)
            measuredCurrent = measuredCurrent/4
            print("measuredCurrent: ", measuredCurrent)
            measuredCurrent = self.convertRaw(measuredCurrent, "CURRENT")
            self.signalUpdateStats.emit("CURRENT", measuredCurrent)
            i = i + 1
            dacCommand = dacCommand + self.incrStep
        self.signalSweepDone.emit(True)
        # When reading voltage, make sure to use int() or float()
        # to convert to integer to be able to do math
        # operations on it.

    def a2d(self, desiredVoltage):
        """ Convert the desiredVoltage to a digital value for the adc
            Will be used to get the STARTING voltage from minV
            Voltage unit: mV
            Equation: Y(+-Out) [mV] = 1.987(X_a) - 3.3
            X_a = analog voltage = (Y+3.3)/1.987 (if Vsupply = 3.3V)
            X_d = digital conversion = (3.3)/(4096*X_a)"""
        DAC_SUPPLY = 3300  # 3.6V supply for DAC
        #vAnalog = float((desiredVoltage + DAC_SUPPLY)/1.987)  # DAC 3.3V ideal
        vAnalog = float((desiredVoltage + DAC_SUPPLY)/1.999)  # DAC 3.6V test
        vDigital = round((4096*vAnalog)/DAC_SUPPLY)
        print("ANALOG: ", desiredVoltage, "DIGITAL: ", vDigital)
        return vDigital

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
        """This function will prepend 0's to raw.
            helps keep the format XXXX if value is smaller
            than 4 digits"""
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
        self.stop = True
        # Should cleanly kill sweep on mutex unlock

    def convertRaw(self, rawValue, type):
        VCC = 5.47  # terms of Volts
        ADC_FULLSCALE = 2000*VCC  # 2000 milli * VCC
        """ Convert raw adc voltage to real voltage"""
        rawValue = int(rawValue)
        ratio = 0
        if rawValue < 4096:
            # positive voltage (0-10V)
            ratio = int(rawValue)/4096
            # voltage = ratio * 10
            voltage = ratio * ADC_FULLSCALE  # get voltage in terms of mV
        elif rawValue >= 4096:
            rawValue = 8192 - rawValue
            # convert scaling (0->0V, 4096-> -10V)
            # be sure to multiply final value by (-1)
            ratio = int(rawValue)/4096
            voltage = -1 * (ratio * ADC_FULLSCALE)

        if type == "VOLTAGE":
            return voltage  # returns voltage in mV
        elif type == "CURRENT":
            # C:V ratio is 1:-1
            current = -1 * voltage
            return current  # returns current in mA
