#include <msp430.h> 

/*
 * main.c
 */
void dacSend(unsigned int dacValue);
void shiftWord(unsigned int wordToShift);
void initPorts();

#define DAC_SCK BIT2		//
#define DAC_SDI BIT3		// 
#define DAC_LATCH BIT4		//
#define DAC_CS BIT5
#define DAC_MODE 0x0000
#define DAC_CFG 0x3000			//0b0011/XXXX/XXXX/XXXX
//#define DAC_CFG 0x1000			//0b0001/XXXX/XXXX/XXXX
//#define SHDN

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;	// Stop watchdog timer
	initPorts();
	dacSend(0x0000);
	__delay_cycles(100000);
    while(1) {
    	dacSend(2048);
    	__delay_cycles(1000000);
    	dacSend(0x400);
    	__delay_cycles(1000000);
    	dacSend(300);
    	__delay_cycles(1000000);

    }
}

void initPorts () {
	P1DIR |= 0x00;
	P2DIR |= 0x00;
	P3DIR |= 0x00;
	P4DIR |= 0x00;

//	P1OUT &= 0x00;
//	P2OUT &= 0x00;
//	P3OUT &= 0x00;
//	P4OUT &= 0x00;

	P1DIR |= DAC_SCK + DAC_SDI + DAC_LATCH + DAC_CS;
	P1OUT |= DAC_LATCH + DAC_CS;
	P1OUT &= ~(DAC_SCK + DAC_SDI);
}

void dacSend(unsigned int dacValue) {			// dacValue = 12-bit digit, 0-4096
	unsigned volatile int dacWord;
	P1OUT |= DAC_LATCH;
	dacWord = dacValue + DAC_CFG;		// add setup bits (MS4Bits)
	shiftWord(dacWord);
}

void shiftWord(unsigned int wordToShift) {				// shifts MSB first
	volatile unsigned int i;
	volatile unsigned int outBit;

	wordToShift = wordToShift;
	P1OUT |= DAC_LATCH;
	P1OUT &= ~DAC_CS;
	__delay_cycles(1000);
	for(i = 0; i < 16; i++) {
		outBit = wordToShift & (0x8000);
		outBit = outBit >> 15;

		switch(outBit) {
		case 0:
			P1OUT &= ~DAC_SDI;
			break;
		case 1:
			P1OUT |= DAC_SDI;
			break;
		default: break;
		}
		if(i == 3) {
			__delay_cycles(1000);
		}
		P1OUT |= DAC_SCK;
//		__delay_cycles(1000);					// slowed down for debugging purposes
		P1OUT &= ~DAC_SCK;
//		__delay_cycles(1000);					// slowed down for debugging purposes
		wordToShift = (wordToShift << 1);		// drop out leftmost bit

	}
	P1OUT |= DAC_CS;		// Bring CS pin HIGH to enable Vout
	// done shifting **
	P1OUT &= ~DAC_LATCH;	// Bring low to latch Din to DAC registers
//	__delay_cycles(1000);
	P1OUT |= DAC_LATCH;
}
