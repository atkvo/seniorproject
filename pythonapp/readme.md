Python Curve Tracer GUI Application
===================================

Curve Tracer Python Gui Application

Purpose: Controls the MSP430 and interprets data to/from it


## Features
-----------

### Main Feature: Voltage Sweep
-------------------------------

    Options: 

        * when to start
        * when to end
        * voltage increment steps (1, 2, 3, 4.. 100% of Range)
        * (If time allows) Live plot OPTION (may be really slow, better to log data then plot after)

### How does voltage sweep work
-------------------------------

    Send DAC value (Get Vdut using this)
    Read ADC (Imonitor)

Other options:
    export data as .csv file
    data initially stored in 2d array [I][V], will dump to CSV when ready

### CSV STYLE
-------------

Use python csv module (?)

    VOLTAGE (mV), CURRENT (mA)
    x,x\n
    x,x\n
    x,x\n
    x,x\n


## DEVELOPMENT NOTES
--------------------

### TODO (Application still under development 10.25.14)
-------------------------------------------------------

* (in progress) Utilize signals & slots (New QT4 style)
* (done) Fix GUI lockup during thread object. (Not behaving like a separate thread...
* Change sweep start to start at MINIMUM voltage (Need dual power supply to begin testing properly)
* Add CSV output ability
* Add premature sweep stop
* Use CX_FREEZE to test it under Windows. Nvm, Must be built under Windows also. Installed required libraries on Windows to build already
* **ADD CURRENT LIMIT **

### Changelog (Started 10.26.14)
--------------------------------

* Fixed GUI lockup. Solution: Call thread object as self.thread
* Added initial signal & slot work (Signals: when sweep starts, stopped, and updating voltage/current stats)
 


### COMMAND LIST
----------------

| COMMAND   | Description                                  |
| --------- | -------------------------------------------- |
| !V=XXXX\* | Give DAC an output voltage. Must be 4 digits |
| !C?\*     | Read Imonitor                                |
| ----      | Read Temp sensor ** REMOVE                   |
| !V?\*     | Read DUT Voltage                             |


### ADC CONVERSION TABLE
------------------------
| ADC RAW       | Conversion           |
| ------------- | -------------------- |
| 0 -> 4095     | 0 -> +(Vcc\*2)       |
| 4096 -> 8192  | -(Vcc\*2) => 0V      |


