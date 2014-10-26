GENERAL OVERVIEW
================


    DUT Voltage (-V to +V)
    DUT Current (-V to +V)
    Temp sensor (0-3.3V)
    DAC output (0-4096)



USER OPTIONS
============

# Main Feature: Voltage Sweep
-----------------------------

    Options: 

        * when to start
        * when to end
        * voltage increment steps (1, 2, 3, 4.. 100% of Range)
        * Temp data OPTION
        * Live plot OPTION (may be really slow, better to log data then plot after)

## How does voltage sweep work
------------------------------

    Send DAC value (Get Vdut using this)
    Read ADC (Imonitor)

Other options:
    export data as .csv file
    data initially stored in 3d array [I][V][T], will dump to CSV when ready

## CSV STYLE
------------

Use python csv module (?)

    VOLTAGE (mV), CURRENT (mA), Temperature (K)
    x,x,x\n
    x,x,x\n
    x,x,x\n
    x,x,x\n


# TODO (Don't ignore above notes btw)
-------------------------------------

Add pyplot stuff into application.
    
    Plot window space always shown? Or only during plot?
    Real-time plotting?

Use CX_FREEZE to test it under Windows. Nvm, Must be built under Windows also. Installed required libraries on Windows to build already

** ADD CURRENT LIMIT **

# COMMAND LIST
--------------

+ -------------------------------------------------------- +
| COMMAND   | Description                                  |
+ --------- + -------------------------------------------- +
| !V=XXXX*  | Give DAC an output voltage. Must be 4 digits |
+ --------- + -------------------------------------------- +
| !C?*      | Read Imonitor                                |
+ --------- + -------------------------------------------- +
| ----      | Read Temp sensor ** REMOVE                   |
+ --------- + -------------------------------------------- +
| !V?*      | Read DUT Voltage                             |
+ --------- + -------------------------------------------- +

RANGE 0-8192
From 0-4095 = Positive
     0 => Vcc*2
From 4096-8192 = Negative
     -(Vcc*2) => 0V
