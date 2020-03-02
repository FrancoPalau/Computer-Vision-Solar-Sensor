
#ifndef TIMER_CONFIG_H_
#define TIMER_CONFIG_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/atomic.h>

#include "uart_config.h"

#define STEP_A DDB1
#define STEP_B DDB2

/*
#define ENA_INTA TIMSK1 |= (1 << OCIE1A)
#define DIS_INTA TIMSK1 &= ~(1 << OCIE1A)

#define ENA_INTB TIMSK1 |= (1 << OCIE1B)
#define DIS_INTB TIMSK1 &= ~(1 << OCIE1B)
*/

#define ENA_INTA DDRB |= (1 << STEP_A)
#define DIS_INTA DDRB &= ~(1 << STEP_A)
#define IS_ENA_INTA (DDRB & (1 << STEP_A))

#define ENA_INTB DDRB |= (1 << STEP_B)
#define DIS_INTB DDRB &= ~(1 << STEP_B)
#define IS_ENA_INTB (DDRB & (1 << STEP_B))


void TIMER_init(void);

ISR (TIMER1_COMPA_vect);
ISR (TIMER1_COMPB_vect);

double position_A;
double position_B;

int pA;
int pB;

#endif /* TIMER_CONFIG_H_ */