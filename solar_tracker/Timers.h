/*
* Timers.h
*
* Created: 2/7/2018 15:37:12
*  Author: lauta
*/
#include "mi_2560_UART0.h"




#ifndef TIMERS_H_
#define TIMERS_H_

#define ACTIVAR_T3	TCCR3B|=(1<<CS31)
#define DESACT_T3	TCCR3B &=~ (1<<CS31)
#define ACTIVAR_T4	TCCR5B|=(1<<CS51)
#define DESACT_T4	TCCR5B &=~ (1<<CS51)
//#define DESACT_T4	TCCR5A &=~ (1<<COM5B1)
#define ACT_INT_T3	TIMSK3 |=(1<<OCIE3A)
#define DESACT_INT_T3	TIMSK3 &=~ (1<<OCIE3A)
#define ACT_INT_T4	TIMSK5 |=(1<<OCIE5A)
#define DESACT_INT_T4	TIMSK5 &=~ (1<<OCIE5A)
#define TIMER3_TOP	TCNT3=OCR3A-1
#define TIMER4_TOP	TCNT5=OCR5A-1

void inicializarTimer1(){
	//Timer1 16-bits en modo CTC con frecuencia de 1Hz, Prescaler:1024
	TCCR1B = 1<<WGM12 | 1<<CS10 | 1<<CS12;
	OCR1A = (1*F_CPU/1024)-1;
	TIMSK1 = 1<<OCIE1A;
}

void inicializarTimer2(){
	//Timer2 8-bits en modo CTC con frecuencia de 100Hz(10ms)
	OCR2A = F_CPU/((long)1024*100)-1;
	TCCR2A |= (1<<WGM21);
	TCCR2B |= (1<<CS22) | (1<<CS21) | (1<<CS20);
	TIMSK2 |= (1<<OCIE2A);
}

void inicializarTimer3(){
	//Timer3
	OCR3A = 5000;
	OCR3B =  (OCR3A>>1) & 0x7fff;						//Como hago un corrimiento a la derecha, me aseguro con 0x7fff que se rellene con 0
	TCCR3A = (1<<COM3B1) | (1<<WGM30) | (1<<WGM31);		//Configuro Timer
	TCCR3B = (1<<WGM32) | (1<<WGM33) | (1<<CS31);		//Configuro Timer fast PWM prescaler 8
	TIMSK3 &=~ (1<<OCIE3A);
	DDRE= (1<<DDE3)|(1<<DDE4);
}
/*
void inicializarTimer4(){
	//Timer4
	OCR4A = 5000;
	OCR4B =  (OCR4A>>1) & 0x7fff;						//Como hago un corrimiento a la derecha, me aseguro con 0x7fff que se rellene con 0
	TCCR4A = (1<<COM4B1) | (1<<WGM40) | (1<<WGM41);		//Configuro Timer
	TCCR4B = (1<<WGM42) | (1<<WGM43) | (1<<CS41);		//Configuro Timer fast PWM prescaler 8
	TIMSK4 &=~ (1<<OCIE4A);
	DDRH= (1<<DDH3)|(1<<DDH4);
}
*/
void inicializarTimer5(){
	//Timer5
	OCR5A = 5000;
	OCR5B =  (OCR5A>>1) & 0x7fff;						//Como hago un corrimiento a la derecha, me aseguro con 0x7fff que se rellene con 0
	TCCR5A = (1<<COM5B1) | (1<<WGM50) | (1<<WGM51);		//Configuro Timer
	TCCR5B = (1<<WGM52) | (1<<WGM53) | (1<<CS51);		//Configuro Timer fast PWM prescaler 8
	TIMSK5 &=~ (1<<OCIE5A);
	DDRH= (1<<DDH3);
	DDRL= (1<<DDL4); // Pin 45
}
ISR(TIMER1_COMPA_vect)
{
	contador++;
	if (contador==PASO_SEG)
	{
		contador=0;
		RTC_GetTime(&rtc);
		if(rtc.hora.Hour>=HORA_INF && rtc.hora.Hour<HORA_SUP){
			uint32_t Totalsegundos=rtc.hora.Hour*SEG_HORA+rtc.hora.Minute*SEG_MIN+rtc.hora.Second;
			if(rtc.fecha.Day==dia && rtc.fecha.Month==mes && (Totalsegundos-segundos)<(PASO_SEG+1)){
				segundos=Totalsegundos;
				nuevaConsigna=1;
				nuevaFecha=0;
				nuevaHora=0;
			}
			
			if(rtc.fecha.Day!=dia || rtc.fecha.Month!=mes){
				dia=rtc.fecha.Day;
				mes=rtc.fecha.Month;
				nuevaFecha=1;
			}
			if ((Totalsegundos-segundos)>(PASO_SEG+1)){
				segundos=Totalsegundos;
				nuevaHora=1;
			}
		}
		else{
			printf("Fecha: %d|%d|%d --- Hora: %d:%d:%d\r\n",rtc.fecha.Day,rtc.fecha.Month,rtc.fecha.Year,rtc.hora.Hour,rtc.hora.Minute,rtc.hora.Second);
		}
	}
}

ISR(TIMER2_COMPA_vect) {
	disk_timerproc();
}

ISR(TIMER3_COMPA_vect){
	ATOMIC_BLOCK(ATOMIC_FORCEON) {
		pA++;
		printf("pa:%d\r\n", pA);
		if(pA==pasosA)
		{
			posA=consignaA;
			printf("Llegue consignaA\r\n");
			pA=0;
			pasosA=0;
			DESACT_T3;
			DESACT_INT_T3;
			TIMER3_TOP;
		}
		if(pA > pasosA){
			pA = 0;
			DESACT_T3;
			DESACT_INT_T3;
			TIMER3_TOP;
		}
	}
}

ISR(TIMER5_COMPA_vect){
	ATOMIC_BLOCK(ATOMIC_FORCEON) {
		pE++;
		printf("pe:%d\r\n", pE);
		if(pE==pasosE)
		{
			posE=consignaE;
			pE=0;
			pasosE=0;
			DESACT_T4;
			DESACT_INT_T4;
			TIMER4_TOP;
			printf("Llegue consignaE\r\n");
		}
		if(pE > pasosE)
		{
			pE = 0;
			DESACT_T4;
			DESACT_INT_T4;
			TIMER4_TOP;
		}
	}
}


#endif /* TIMERS_H_ */