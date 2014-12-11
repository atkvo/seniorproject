Python Curve Tracer GUI Application
===================================

Curve Tracer Python Gui Application

Purpose:    Controls the MSP430 and interprets data to/from it
            Sweeps the solar cell and logs the current/voltage


## Features

### Main Feature: Voltage Sweep

    Options: 

        * when to start
        * when to end
        * voltage increment steps 
        * Live plot - Simple visualization of IV curve. Use CSV export & Excel for more robust plotting
            * Note, live plots will seem very unstable during initial samples since the scaling for the plot is very small until more data is sampled + plotted.

### How does voltage sweep work

    Send DAC value (Difference amplifier causes Vout swing from +- 3.3V)
    Read voltage across Solar Cell and from Imonitor pin and do necessary conversions

Other options:
    export data as .csv file
    data initially stored in 2d array [V][I], will dump to CSV on request

### CSV STYLE

Use python csv module (?)

    VOLTAGE (mV), CURRENT (mA)
    x,x\n
    x,x\n
    x,x\n
    x,x\n


### Required Libraries & Links

            USB to UART Driver (CP210x from Silicon Labs)
            http://www.silabs.com/products/mcu/pages/usbtouartbridgevcpdrivers.aspx
            
            Python 3.4.0
            https://www.python.org/downloads/release/python-340/

            PyQt4
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

            Matplotlib
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib

            pySerial
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyserial
            
            six
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#six
            
            pyParsing
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyparsing
            
            numpy
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

### Usage

    0. Install all drivers and code components
    1. Select COM port
    2. Setup desired sweep range
    3. Check sweep calibration parameters
    4. Click "sweep"
    5. Wait for sweep to finish
        5.1. Note: If taking large amount of data points, application may "hang" for a bit when data is compiled up, but all is well
    6. Export data
        6.1. Name the file with a **.csv** extension so Excel will automatically open when double clicking the file


### COMMAND LIST

| COMMAND   | Description                                  |
| --------- | -------------------------------------------- |
| !V=XXXX\* | Give DAC an output voltage. Must be 4 digits |
| !C?\*     | Read Imonitor                                |
| !V?\*     | Read DUT Voltage                             |




## DEVELOPMENT NOTES

Notes related to the development of the code. Should be important to those who edit the code for themselves.


    curveTracerMainGUI.py - Main GUI code. Does all the interface with the user and hardware. Calls on curveTracerSerial & curveTracerSweeper as "components"

    curveTracerSerial.py - Responsible for establishing connection with the MSP430 and formatting commands

    curveTracerSweeper.py - Responsible for the automatic sweeping thread. Contains all the math and conversion algorithms as well.


### Important Equations & Notes

#### Bipolar DAC voltage 
    
    OUTPUT = 1.987 * X_a - 3300 mV
    
    X_a = analog voltage
          (OUTPUT + Vsupply)    |
        = ------------------    |
            1.987               | Vsupply = 3300 mV

    X_d = digital conversion
           4096 * X_a   |
        =  ----------   |
            Vsupply     | Vsupply = 3300mV

#### Desired voltage step to digital step

                    (desiredStepSize * 4096)
    digitalStep =   -------------------------------
                            2 * VCC3

#### ADC CONVERSION TABLE

| ADC RAW       | Conversion           |
| ------------- | -------------------- |
| 0 -> 4095     | 0 -> +(Vcc\*2)       |
| 4096 -> 8192  | -(Vcc\*2) => 0V      |
### TODO

* (done) Utilize signals & slots (New QT4 style)
* (done) Fix GUI lockup during thread object. (Not behaving like a separate thread...
* (done, not tested) Change sweep start to start at MINIMUM voltage (Need dual power supply to begin testing properly)
* (done) Add CSV output ability
* (done) Add premature sweep stop
* (done) Fix Pyplot lockup
* (done) Add user-settable averaging (how many samples per point)


### Changelog
#### 12.11.14
* Fixed increment voltage formula
* Added user settable VCC3 and current gain 
* Clean out some comments
* Added safety check to make sure step size is > 2 mV

#### 12.06.14 06:00 PM
* Added adjustable 5V Calibration for ADC 
* Change increment % -> Step size (mV)
    * Added functions to support user adjustable sweep steps in mV rather than % of full range

#### 11.28.14 10:30 PM
* Added user-settable sample rate (samples per voltage step)

#### 11.22.14 01:40 PM
* Added averaging for voltage and current measurements
    * TODO: user-settable averaging
* Added another "stop check" for sweeping loop
    * if dacCmd > 4095, end sweep

#### 11.10.14 05:00 PM
* Fixed plot. From (voltage, voltage) to (current, current)

#### 11.09.14 09:00 PM
* Added current conversion to curveTracerSweeper
* Cleaned up code (removed obsolete comments)
* Changed constant variables to all CAPS to easily distinguish them

#### 11.07.14 12:06 AM
* Fixed plot lockup (use PYQT4 backend from matplotlib)
* Added plot axis labels and title
* 

#### 11.06.14 11:26 PM
* Code cleanup (still WIP)
* Confirmed +- voltage sweep logic (Equation works fine)


#### 11.04.14
* Added sweep to start at Minimum voltage
    * Extra function in sweeper to convert min voltage -> dac digital value

#### 10.31.14
* Added CVS logging/export
* Added real-time plotting (should make this optional)
* Added premature sweep stop (needs work, slow to respond sometimes)
* Moved data logging from sweepthread to main application. Measured values relayed through signals/slots


#### 10.26.14
* Fixed GUI lockup. Solution: Call thread object as self.thread
* Added initial signal & slot work (Signals: when sweep starts, stopped, and updating voltage/current stats)
 