import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "CurveTracer",
        version = "0.1",
        description = "EE198 SolarCellCurveTracer",
        executables = [Executable("curveTracerMainGUI.py", base=base)])
