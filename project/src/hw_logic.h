#ifndef HW_LOGIC_H_
#define HW_LOGIC_H_

#include <avr/io.h>

// Input definitions
#define LED DDB5

#define DIR_A DDB0
#define DIR_B DDB3

#define DIR_CLK_A (PORTB |= (1 << DIR_A))
#define DIR_ACLK_A (PORTB &= ~(1 << DIR_A))

#define DIR_CLK_B (PORTB |= (1 << DIR_B))
#define DIR_ACLK_B (PORTB &= ~(1 << DIR_B))

void HW_init(void);

// void homingA(void);

double position_A;
double position_B;

int pA;
int pB;

double setpointA;
double setpointB;

int steps_A;
int steps_B;

int flagHomingA;
int flagHomingB;

char flag;

#endif /* HW_LOGIC_H_ */