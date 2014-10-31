#!/usr/bin/env python3

import serial


class Connection:
    def __init__(self, port, rate):
        """ on Windows, port = number
            on Linux, port = '/dev/tty_'
        """
        self.ser = serial.Serial(port, rate, timeout=.2)

    def sendCommand(self, command):
        """ Sends command CMD_
        - Calls on function curveTracerProtocol.createPacket()
        to add the ! and * to the command
        """
        command = self.createPacket(command)
        # print("COMMAND: ", command)
        self.ser.write(command.encode())
        # print('encoded: ', command.encode())

    def read(self):
        x = ""
        x = self.ser.read(50)
        # print(x)
        # print("Raw adc: ", x)
        return x

    def close(self):
        self.ser.close()
        del self.ser

    def createPacket(self, base):
        command = "!" + base + "*"
        # print(type(command))
        return command


        # ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        # cmd = "!VLT?*"
        # print(type(cmd.encode()))
        # ser.write(cmd.encode())
        # x = ser.read(50)
        # print(x)
