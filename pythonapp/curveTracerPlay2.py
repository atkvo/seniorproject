#!/usr/bin/env python3

# import curveTracerSweeper

# c = curveTracerSweeper.SweeperThread()

# c.start()


# print("DONE")
#***********************
# raw = 100
# command = "V="
# digits = len(str(raw))
# zeroes = 4 - digits
# for i in range(zeroes):
#     command = command + "0"
# command = command + str(raw)
# print(command)
#************************

# rawVoltage = "4005"
# ratio = int(rawVoltage)/4096
# ratio = -1*(ratio * 10)
# print(ratio)

dacSupply = 3300


def a2d(desiredVoltage):
    """ Convert the desiredVoltage to a digital value for the adc
        Will be used to get the STARTING voltage from minV

        Equation: Y(+-Out) = 1.987(X_a) - 3.3
        X_a = analog voltage = (Y+3.3)/1.987
        X_d = digital conversion = (4096*X_a)/Vsupply"""
    voltA = float((desiredVoltage + dacSupply)/1.987)
    voltD = round((4096*voltA)/dacSupply)
    return voltD

valueTest = -3200
test = a2d(valueTest)
print(test)
