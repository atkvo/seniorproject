//--------------------------------------------
// EE198 Senior Project
// Group 6 - Fall 2014
// Members: Victoria Aman, Polar Halim
//			Jose Martinez, Andrew Vo
//
// 	Purpose: curveTracer_uart is simply a
// 		portion of the project code which is
// 		responsible for implementing the
//		communication lines between the msp
//		and the user through UART -> USB
//--------------------------------------------

#include <msp430.h>
#include <string.h>

void initPorts();
void initUART();
void initADC();

void UART_sendChar(char *c);
void analyze_cmd(char *c);
void UART_sendInt(unsigned int x);


// Global flags and constants
static volatile unsigned int flg_rx = 0;
unsigned int g_adc_value = 0;
static char const g_vlt[3]="VLT";
static char const g_cur[3]="CUR";
static char const g_sts[3]="STS";

#define REQUEST 0
#define COMMAND 1

int main(void)
{
	WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT

	initPorts();
	initADC();
	initUART();
	char rxBuffer[15];
	volatile int i = 0;
	__bis_SR_register(LPM0_bits + GIE);      // Enter LPM0, interrupts enabled
//	__bis_SR_register(GIE);

	while(1) {
		if (flg_rx) {
			if (UCA1RXBUF == '*') {
				analyze_cmd(rxBuffer);
		    	memset(rxBuffer, 0, i);
		    	i = 0;
		    }
			else if (UCA1RXBUF == 13) {		// compare to ascii {CR} d'13, 0x0D
				analyze_cmd(rxBuffer);
				memset(rxBuffer, 0, i);
				i = 0;
			}
		    else {
		    	rxBuffer[i] = UCA1RXBUF;
		    	i++;
		    }
			flg_rx = 0;
		}
		__bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
	}
}

#pragma vector=ADC12_VECTOR
__interrupt void ADC12_ISR (void) {

	ADC12CTL0 |= ADC12SC;
//	count = count + 1;							// used for debugging purposes
	g_adc_value = ADC12MEM0;

	ADC12CTL0 &= ~ADC12SC;
}

#pragma vector=USCI_A1_VECTOR
__interrupt void USCI_A1_ISR(void)
{
	LPM0_EXIT;									// exit LPM0
	switch(__even_in_range(UCA1IV,4))
	{
		case 0:break;                             // Vector 0 - no interrupt
		case 2:                                   // Vector 2 - RXIFG
		  flg_rx = 1;
		break;
		case 4:break;                             // Vector 4 - TXIFG
		default: break;
	}
}

void initPorts() {
	P1DIR |= 0x00;
	P2DIR |= 0x00;
	P3DIR |= 0x00;
	P4DIR |= 0x00;

	P1OUT |= 0x00;
	P2OUT |= 0x00;
	P3OUT |= 0x00;
	P4OUT |= 0x00;

	P1DIR |= 0x01;
	P1OUT |= 0x01;
}

void initUART() {

	P4SEL |= BIT4+BIT5;         				// Configure P4.4,5 as TXD/RXD

//	P3SEL |= BIT3+BIT4;         				// Configure P3.4,3 as TXD/RXD
	UCA1CTL1 |= UCSWRST;                    	// **Put state machine in reset**
	UCA1CTL1 |= UCSSEL_2;                     	// SMCLK
	UCA1BR0 = 6;                              	// 1MHz 9600 (see User's Guide)
	UCA1BR1 = 0;                              	// 1MHz 9600  UCA1MCTL = UCBRS_0 + UCBRF_4 + UCOS16;
	UCA1MCTL = UCBRS_0 + UCBRF_13 + UCOS16;		// Modln UCBRSx=0, UCBRFx=0,
												// over sampling
	UCA1CTL1 &= ~UCSWRST;                   	// **Initialize USCI state machine**
	UCA1IE |= UCRXIE;                         	// Enable USCI_A1 RX interrupt

}

void initADC() {
	P6SEL |= BIT0;								// Pin6.0 setup for ADC input
	ADC12CTL1 = ADC12DIV_3 + ADC12CONSEQ_0 + ADC12SSEL_3 + ADC12CSTARTADD_0;
	ADC12CTL0 |= ADC12SHT0_15 + ADC12ON + ADC12REFON;
	ADC12IE |= ADC12IE0;						// Enable ADC interrupts
	ADC12MCTL0 |= ADC12INCH_0 + ADC12SREF_0; 	// AN0 & Vref = VCC-VSS
	ADC12CTL0 |= ADC12ENC;						// Enable ADC Conversions
	ADC12CTL0 |= ADC12SC;						// Start Conversion

	ADC12CTL0 &= ~ADC12SC;						// required after every ADC12MEM0 read
}

void UART_sendChar(char *c) {
	unsigned int len = strlen(c);
	unsigned int i;
	for(i = 0; i<(len); i++) {
		while(!(UCA1IFG&UCTXIFG));
		UCA1TXBUF = c[i];
	}
}

// this function works, but is DUMB.
// make an INT -> ASCII function instead using this as a guide.
void UART_sendInt(unsigned int x) {
	volatile unsigned int number = x;

	int i = 3;
	char c[4];
	unsigned int digit;
	for(i = 3; i >= 0; i--) {
		digit = (number % 10);
		c[i] = digit + 0x30;

		number = (number/10);
	}

//	unsigned int len = strlen(c);

	for(i = 0; i <= 3; i++) {
		while(!(UCA1IFG&UCTXIFG));
		UCA1TXBUF = c[i];
	}
}



void analyze_cmd(char *c) {
	unsigned int len = strlen(c);
	unsigned int flg_match = 1;
	unsigned int flg_type; 	// 0 = request, 1 = command
	unsigned int i = 0;

//	may be unnecessary
	if (c[0]=='!') {
		if (c[4] == '?')
			flg_type = REQUEST;
		else if (c[4] == '=')
			flg_type = COMMAND;
		else
			flg_match = 0;
		if (flg_match != 0) {
			switch(c[1]) {
					case 'C':
						for(i = 1; i <= 3; i++) {
							if(!(c[i] == g_cur[i-1])) {
								flg_match = 0;
								break;
							}
						}
						UART_sendChar("Current Request\n");
						break;
					case 'V':
						for(i = 1; i <= 3; i++) {
							if((c[i] != g_vlt[i-1])) {
								flg_match = 0;
								break;
							}
						}
						if ((flg_type == REQUEST) & (flg_match = 1)) {
//							UART_sendChar("Voltage Request\n");
							UART_sendChar("!VLT=");
							UART_sendInt(g_adc_value);
						}
						else if ((flg_type == COMMAND) & (flg_match = 1))
							UART_sendChar("Voltage Command\n");
						break;
					case 'S':
						for(i = 1; i <= 3; i++) {
							if(!(c[i] == g_sts[i-1])) {
								flg_match = 0;
								break;
							}
						}
						UART_sendChar("Status Request\n");
						break;
					default: flg_match = 0;
					}
		}


	}
	else
		UART_sendChar("No '!' Detected\n");
	if (flg_match == 0) {
		UART_sendChar("Invalid command\n");
	}

}
