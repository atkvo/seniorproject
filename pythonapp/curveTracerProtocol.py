#!/usr/bin/env python3

####################################
#
# Packet Formats:
#
#	Voltage command = !VLT=xxxx*
#	Voltage request = !VLT?DUT*
#       Voltage request = !VLT?TMP*
#	Current request = !CUR?*
#
####################################

# ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
# cmd = "!VLT?*"
# print(type(cmd.encode()))
# ser.write(cmd.encode())
# x = ser.read(50)
# print(x)


def createPacket(base):
    command = "!" + base + "*"
    # print(type(command))
    return command

## This function might be unnecessary. MSP430 already returns correct value


# def readPacket(rawResponse):
