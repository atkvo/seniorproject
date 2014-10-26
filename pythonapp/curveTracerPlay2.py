#!/usr/bin/env python3

# import curveTracerSweeper

# c = curveTracerSweeper.SweeperThread()

# c.start()


# print("DONE")

rawVoltage = "4005"
ratio = int(rawVoltage)/4096
ratio = -1*(ratio * 10)
print(ratio)