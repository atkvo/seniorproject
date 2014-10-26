//--------------------------------------------
// EE198 Senior Project
// Group 6 - Fall 2014
// Members: Victoria Aman, Polar Halim
//			Joe Martinez, Andrew Vo
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
void UART_sendChar(char *c);
void analyze_cmd(char *c);
void test_func();

// Global flags and constants
volatile unsigned int flg_rx = 0;
static char const g_vlt[3]="VLT";
static char const g_cur[3]="CUR";
static char const g_sts[3]="STS";


int main(void)
{
	WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT

	initPorts();
	initUART();
	char g_x[15];
	volatile int i = 0;
	__bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
//	__bis_SR_register(GIE);
	while(1) {
		test_func();
		if (flg_rx) {

			if (UCA1RXBUF == '*') {
				analyze_cmd(g_x);
//		    	UART_sendChar(g_x);
		    	memset(g_x, 0, i);
		    	i = 0;
		    }
			else if (UCA1RXBUF == 13) {		// compare to ascii {CR} d'13, 0x0D
				analyze_cmd(g_x);
				memset(g_x, 0, i);
				i = 0;
			}
		    else {
		    	g_x[i] = UCA1RXBUF;
		    	i++;
		    }
			flg_rx = 0;
		}
		if (flg_rx == 0)
			__bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
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

	P4DIR |= BIT7;
//	P4OUT |= BIT7;
}

void initUART() {
	UCA1CTL1 |= UCSWRST;                    	// **Put state machine in reset**
	P4SEL |= BIT4+BIT5;         				// Configure P4.4,5 as TXD/RXD
//	P3SEL |= BIT3+BIT4;         				// Configure P3.4,3 as TXD/RXD
	UCA1CTL1 |= UCSSEL_2;                     	// SMCLK
	UCA1BR0 = 6;                              	// 1MHz 9600 (see User's Guide)
	UCA1BR1 = 0;                              	// 1MHz 9600  UCA1MCTL = UCBRS_0 + UCBRF_4 + UCOS16;
	UCA1MCTL = UCBRS_0 + UCBRF_13 + UCOS16;		// Modln UCBRSx=0, UCBRFx=0,
												// over sampling
	UCA1CTL1 &= ~UCSWRST;                   	// **Initialize USCI state machine**
	UCA1IE |= UCRXIE;                         	// Enable USCI_A1 RX interrupt
}

void UART_sendChar(char *c) {
	volatile unsigned int len = strlen(c);
	volatile unsigned int i;
	P4OUT |= BIT7;
	for(i = 0; i<(len); i++) {
		while(!(UCA1IFG&UCTXIFG));
		UCA1TXBUF = c[i];
	}
	P4OUT &= ~BIT7;
}

void test_func() {
	P1OUT ^= BIT0;
}
void analyze_cmd(char *c) {
	volatile unsigned int len = strlen(c);
	volatile unsigned int flg_match = 1;
	volatile unsigned int flg_type; 	// 0 = request, 1 = command
	volatile unsigned int i = 0;

//	may be unnecessary
	if (c[0]=='!') {
		if (c[4] == '?')
			flg_type = 0;
		else if (c[4] == '=')
			flg_type = 1;

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
				if(!(c[i] == g_vlt[i-1])) {
					flg_match = 0;
					break;
				}
			}
			if (flg_type == 0)
				UART_sendChar("Voltage Request\n");
			else if (flg_type == 1)
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
	else
		UART_sendChar("No '!' Detected\n");
	if (flg_match == 0) {
		UART_sendChar("Invalid command\n");
	}

}
// Echo back RXed character, confirm TX buffer is ready first
#pragma vector=USCI_A1_VECTOR
__interrupt void USCI_A1_ISR(void)
{
//	P1OUT ^= BIT0;
	LPM0_EXIT;
//	__bis_SR_register_on_exit(LPM3_bits);
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
