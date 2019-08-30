#ifndef EXINT_CONFIG_H_
#define EXINT_CONFIG_H_

#include <avr/io.h>
#include <avr/interrupt.h>

void EXINT_init(void);
ISR(INT0_vect);
ISR(INT1_vect);

int limswitchA;
int limswitchB;

#endif /* EXINT_CONFIG_H_ */