#!/usr/bin/env python3
from PyQt4 import QtCore


class SweeperThread(QtCore.QThread):

    # def __init__(self, mspInstance, minV, maxV, incr):
    def __init__(self, minV, maxV, incr):
    # Should also take sweep increment % also
        super(SweeperThread, self).__init__()

        self.minV = int(minV)
        self.maxV = int(maxV)
        self.incrStep = round(4096*(int(incr)/100))
        print("incr step is: ", self.incrStep)

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self): #NOTE: NEVER call this function directly
    # Don't use SLEEP either?
        measuredVoltage = 0
        measuredCurrent = 0

        while measuredVoltage < self.maxV:
            measuredVoltage = measuredVoltage + self.incrStep
            print(measuredVoltage)
            # When reading voltage, make sure to use int() to convert to integer
            # to be able to do math operations on it
        mutex = QtCore.QMutex()
        mutex.unlock()

        # self.terminate()
        
        """ Initialize thread here. Be sure to kill thread also! """

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
        """ Convert raw adc voltage to real voltage"""
        ratio = 0
        if type == "VOLTAGE":
            if rawValue < 4096:
                # positive voltage (0-10V)
                ratio = int(rawValue)/4096
                voltage = ratio * 10
            elif rawValue >= 4096:
                rawValue = 8192 - rawValue      # convert scaling (0->0V, 4096-> -10V)
                # be sure to multiply final value by (-1)
                ratio = int(rawValue)/4096
                voltage = -1 * (ratio * 10)

    def getResults(self):
        """ Return grabbed values"""
