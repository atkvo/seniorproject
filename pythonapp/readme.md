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
        * voltage increment steps (0.5, 1, 1.8, 2, 3, 4.. 99.9, 100% of Range)
        * Live plot - Simple visualization of IV curve. Use CSV export & Excel for more robust plotting

### How does voltage sweep work

    Send DAC value (Difference amplifier causes Vout swing to +- 3.3V)
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


## DEVELOPMENT NOTES

### TODO (Application still under development 10.25.14)

* (done) Utilize signals & slots (New QT4 style)
* (done) Fix GUI lockup during thread object. (Not behaving like a separate thread...
* (done, not tested) Change sweep start to start at MINIMUM voltage (Need dual power supply to begin testing properly)
* (done) Add CSV output ability
* (done) Add premature sweep stop
* (done) Fix Pyplot lockup
* **ADD CURRENT LIMIT **
* Use CX_FREEZE to test it under Windows. Nvm, Must be built under Windows also. Installed required libraries on Windows to build already


### Changelog
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
 


### COMMAND LIST

| COMMAND   | Description                                  |
| --------- | -------------------------------------------- |
| !V=XXXX\* | Give DAC an output voltage. Must be 4 digits |
| !C?\*     | Read Imonitor                                |
| !V?\*     | Read DUT Voltage                             |


### ADC CONVERSION TABLE

| ADC RAW       | Conversion           |
| ------------- | -------------------- |
| 0 -> 4095     | 0 -> +(Vcc\*2)       |
| 4096 -> 8192  | -(Vcc\*2) => 0V      |


