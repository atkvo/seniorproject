#!/usr/bin/env python3

####################################
#
# Packet Formats:
#
#	Voltage command = !V=xxxx*
#	Voltage request = !V?*
#	Current request = !C?*
#
####################################


def createPacket(base):
    command = "!" + base + "*"
    # print(type(command))
    return command

## This function might be unnecessary. MSP430 already returns correct value


# def readPacket(rawResponse):
