#!/usr/bin/env python3

# import curveTracerSweeper

# c = curveTracerSweeper.SweeperThread()

# c.start()


# print("DONE")
raw = 100
command = "V="
digits = len(str(raw))
zeroes = 4 - digits
for i in range(zeroes):
    command = command + "0"
command = command + str(raw)
print(command)

# rawVoltage = "4005"
# ratio = int(rawVoltage)/4096
# ratio = -1*(ratio * 10)
# print(ratio)