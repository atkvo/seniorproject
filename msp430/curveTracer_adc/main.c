#include <msp430.h> 

/*
 * main.c
 */

volatile unsigned int g_adcValue = 0;
// unsigned int count = 0;			// ** Used for debugging purposes

void init_adc();
void init_timer();
void adc_sample();

int main(void) {

    WDTCTL = WDTPW | WDTHOLD;	// Stop watchdog timer

	init_adc();
	__bis_SR_register(LPM3_bits + GIE);

	while(1) {
	}
}

#pragma vector=ADC12_VECTOR
__interrupt void ADC12_ISR (void) {

	ADC12CTL0 |= ADC12SC;
//	count = count + 1;				// used for debugging purposes
	g_adcValue = ADC12MEM0;			// store ADC12MEM0 to g_adcValue
	ADC12CTL0 &= ~ADC12SC; 			// stop conversion
}

void init_adc() {
	P6SEL |= BIT0;
//	ADC12CTL1 = ADC12DIV_3 + ADC12ISSH + ADC12CONSEQ_0 + ADC12SSEL_3 + ADC12CSTARTADD_0;
	ADC12CTL1 = ADC12DIV_3 + ADC12CONSEQ_0 + ADC12SSEL_3 + ADC12CSTARTADD_0;
	ADC12CTL0 |= ADC12SHT0_15 + ADC12ON + ADC12REFON;
	ADC12IE |= ADC12IE0;						// Enable ADC interrupts
	ADC12MCTL0 |= ADC12INCH_0 + ADC12SREF_0; 	// AN0 & Vref = VCC-VSS
	ADC12CTL0 |= ADC12ENC;						// Enable ADC Conversions

	ADC12CTL0 |= ADC12SC;						// Start Conversion
	g_adcValue = ADC12MEM0;						// read converted value in ADC12MEM
	ADC12CTL0 &= ~ADC12SC;						// required after every ADC12MEM0 read
	// count = 1;								// ** Used for debugging purposes

	// use P6.0 for ADC0 input

	// read ADC value through ADC12MEM0 register
}

//
//void adc_sample() {
////	ADC12CTL0 &= ~ADC12ENC;
//	ADC12CTL0 |= ADC12SC;
////	while(ADC12CTL0 & BUSY);		// wrong. should be ADC12CTL1
//	g_adcValue = ADC12MEM0;
////	ADC12CTL0 &= ~ADC12ENC;
////	__bis_SR_register(LPM3_bits + GIE);
//}
