#include <msp430.h> 
/*
 * main.c
 * This code is intended to understand the functionality
 * 	of the LTC1854 12-bit bipolar external ADC
 *
 */

#define ADC_SCK BIT1		// SPI Clock
#define ADC_SEND BIT2		// SDI (ADC control 8-bit)
#define ADC_CONVST BIT3		// CONVST (Start ADC conversion. Active High)
#define ADC_READ BIT4		// SDO (ADC converted data 16-bit (2LSB Don't care)
#define ADC_BUSY BIT0		// If LOW, then ADC is busy
#define PORT_ADC P6OUT


#define ADC_CH0 0x8000	// MUX CTRL: 0b1000 ---- ---- ----
#define ADC_CH2 0x9000  // MUX CTRL: 0b1001 ---- ---- ----
#define ADC_CH4 0xA000  // MUX CTRL: 0b1010 ---- ---- ----

#define ADC_ON	0x0000	// PWR CTRL: 0b---- --00 ---- ----
#define ADC_NAP	0x0200	// PWR CTRL: 0b---- --10 ---- ----
#define ADC_SLP	0x0100	// PWR CTRL: 0b---- --01 ---- ----

void shiftWordOut(unsigned int wordToShift);
unsigned int shiftWordIn();
void adcSend(unsigned int channel, unsigned int power);
void adcRead(unsigned int channel);
void initPorts();

volatile unsigned int g_adcValue;

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;	// Stop watchdog timer
	initPorts();
	while(1) {
		adcRead(0);
		__delay_cycles(10000);

	}
}


void initPorts() {
	P1DIR |= 0x00;
	P2DIR |= 0x00;
	P3DIR |= 0x00;
	P4DIR |= 0x00;
	P5DIR |= 0x00;
	P6DIR |= 0x00;
	P7DIR |= 0x00;
	P8DIR |= 0x00;

	P6DIR |= ADC_SCK + ADC_SEND + ADC_CONVST;
	P6DIR &= ~ADC_READ;
}

void shiftWordOut(unsigned int wordToShift) {				// shifts MSB first
	volatile unsigned int i;
	volatile unsigned int outBit;
	PORT_ADC &= ~ADC_SCK;
	// ADC SPECIFIC ----------------
	volatile unsigned int inBit;
	volatile unsigned int data = 0;
	// -----------------------------

	wordToShift = wordToShift;
	while(P6IN & ADC_BUSY){;} 				// wait until ADC is not busy

	for(i = 0; i < 16; i++) {
		outBit = wordToShift & (0x8000);
		outBit = outBit >> 15;

		switch(outBit) {
		case 0:
			PORT_ADC &= ~ADC_SEND;
			break;
		case 1:
			PORT_ADC |= ADC_SEND;
			break;
		default: break;
		}

		// ADC SPECIFIC ----------------
		if (i < 13) {
			inBit = (P6IN & ADC_READ) && ADC_READ;

			data = data | inBit;
			data = data << 1;
		}
		// -----------------------------

		PORT_ADC |= ADC_SCK;
		PORT_ADC &= ~ADC_SCK;

		wordToShift = (wordToShift << 1);		// drop out leftmost bit

	}
	g_adcValue = data;
}

unsigned int shiftWordIn() {
	volatile unsigned int i;
	volatile unsigned int inBit;
	volatile unsigned int data = 0;

	for(i = 0; i < 16; i++) {
		/* Implement logic for receiving 16 bits from pin ADC_READ
		 * Question: Should distinct ADC values be stored globally?
		 * Or a single global variable g_adcValue and have Python interpret it?
		 *
		 */
		PORT_ADC |= ADC_SCK;
		PORT_ADC &= ~ADC_SCK;

		inBit = (P6IN & ADC_READ);
		data = data + inBit;
		data = data << 1;
	}

	return data;
}

void adcSend(unsigned int channel, unsigned int power) {
	unsigned int command;
	switch(channel) {
	case 0:
		command = ADC_CH0;
		break;
	case 1:
		command = ADC_CH2;
		break;
	case 2:
		command = ADC_CH4;
		break;
	default:
		break;
	}

	switch(power) {
	case 0:
		command = command + ADC_ON;
		break;
	case 1:
		command = command + ADC_SLP;
		break;
	case 2:
		command = command + ADC_NAP;
		break;
	default:
		command = command + ADC_ON;
	}

	shiftWordOut(command);
}

void adcRead(unsigned int channel) {
	unsigned int power = 0;
	PORT_ADC |= ADC_CONVST;
	PORT_ADC &= ~ADC_CONVST;
	adcSend(channel, power);
}
