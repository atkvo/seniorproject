#!/usr/bin/env python3

import sys
# import curveTracerSerial as myserial
# import curveTracerProtocol as protocol
import time

# obj = myserial.CurveTracerSerial('/dev/ttyACM1', 9600)


# while True:
# 	raw = ""
# 	raw = raw_input('Enter command: ')
# 	command = protocol.createPacket(raw)
# 	obj.sendCommand(command)
# 	response = obj.read()
# 	print(response)


# def requestLoop(limit):
#     command = protocol.createPacket("VLT?")
#     obj.sendCommand(command)
#     response = obj.read()
#     # response = int(response)
#     print("response:", response)
#     time.sleep(.5)
#     # while response < limit:
#     # 	command = protocol.createPacket("VLT?")
#     # 	obj.sendCommand(command)
#     # 	response = obj.read()
#     # 	response = int(response)     # use int(response) to convert from ASCII to integer
#     # 	print("response and type: ", response, type(response))

# limit = input('Enter limit: ')	# use raw_input to get ASCII char
# while(True):
#     command = input('COMMAND: ')
#     protocol.createPacket(command)
#     # print("ECHO: ", command)
#     obj.sendCommand(command)
#     response = obj.read()
#     print("RESPONSE: ", response)
# obj.close()
# del obj


#CURVE TRACER PLOT PREVIOUS 

import matplotlib.pyplot as plt
from math import *
from numpy import *


# arSize = input("array size: ")
valMax = float(input("max value: "))
valMin = float(input("min value: "))

# newStep = int(input("start value: "))
arStep = input("array step: ")
realTime = int(input("Real time (1) or (0): "))
# arSize = int(arSize)

# arStep = int(4096/int(arStep)) ## take only integer steps
# arStep = int(arStep)
arStep = float(arStep)
arSize = int((valMax - valMin)/(arStep))

# arSize = int(arSize)

# print(arStep)
# print(arSize)
# arSize = int(arSize/arStep)

print("SIZE: ", arSize)

x = zeros((arSize))           # initialize array with zeroes
y = zeros((arSize))           # initialize array with zeroes
y2 = zeros((arSize))
xAxis = zeros((arSize))
xAxis[0] = valMin
plt.ion()
# plt.show()
# ivCurve = plt.plot(x, y)
# xyCurve = plt.plot(x, y2)
# plt.setp(ivCurve, color='r', linewidth=3.0)
# plt.setp(xyCurve, color='b', linewidth=7.0)
# newStep = 0

## REAL TIME PLOTTING IS SLOW. MAKE THIS AN OPTION
# i = 1

for i in range(1, arSize):
    xAxis[i] = xAxis[i-1] + .785

plt.xticks(xAxis)

for i in range(arSize):
    # x[i] = newStep
    # x[i] = newStep
    x[i] = valMin
    # y[i] = sin((x[i])/4)
    # y[i] = (x[i])*(x[i])*(x[i])
    y[i] = cos(x[i])
    y2[i] = sin(x[i])
    if realTime is 1:
            # plt.plot(x[0:i], y[0:i])
            # plt.draw()
            plt.plot(x[0:i], y[0:i])
            plt.plot(x[0:i], y2[0:i])
            plt.draw()
    print(i)
    valMin = valMin + arStep
    # newStep = newStep + arStep

## TURN OFF REAL TIME TO MAKE PLOTTING QUICKER
## Calculate arrays and then plot
if realTime is 0:
        plt.plot(x, y)
        plt.plot(x, y2)
        plt.draw()
print(x)
print(y)
# y = 2*y

input("Press Enter to quit: ")
# plt.plot(x, y)
# plt.show()


