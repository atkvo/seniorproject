SENIOR PROJECT
=============

EE198 - 2014 SPRING-FALL

Group Members: 

	Victoria Aman
	Polar Halim
	Jose Martinez
	Andrew Vo

Advisor: 

	Dr. David Parent


# General Overview

The MSP430 microcontroller contains the direct means of controlling/communicating with the various hardware of the curve tracer. It reacts solely on the USB UART connection with a computer through a python application. Without the application sending commands to the MSP430, it will sit in low power mode waiting for a UART interrupt. 


# COMMANDS

| COMMAND   | Description                                  |
| --------- | -------------------------------------------- |
| !V=XXXX\* | Give DAC an output voltage. Must be 4 digits |
| !C?\*     | Read Imonitor                                |
| !V?\*     | Read DUT Voltage                             |

# HARDWARE 
The hardware portion (digital components) of the Curve Tracer consists of the following components:

    * MSP430G2553 - 16-bit low power TI microcontroller
    * LTC1854CG - 12-bit bipolar ADC
    * MCP4921 - 12-bit Microchip DAC

# CHANGELOG 
## 11.28.14 10:30PM
* Changed ADC mode for shunt resistor voltage
    * From single ended mode to differential mode (-CH2, +CH3)
    * Due to differential mode connections (+Vcurrent connected to -CH2), voltage from inverting amplifier will automatically flip to a positive voltage. There isn't a need to multiply the voltage by -1 in the python app anymore

## 11.22.14 1:40PM
* Changed ADC modes
    * CH0 changed from Single ended mode to Differential mode

