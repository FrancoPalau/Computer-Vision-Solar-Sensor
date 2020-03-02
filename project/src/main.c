
#ifndef F_CPU
#define F_CPU 16000000UL 
#endif
 
#include <avr/io.h>
#include <util/delay.h>

#include "timer_config.h"
#include "uart_config.h"

// Input definitions
#define LED DDB5

#define DIR_A DDB0
#define DIR_B DDB3

#define DIR_CLK_A (DDRB |= (1 << DIR_A))
#define DIR_ACLK_A (DDRB &= ~(1 << DIR_A))

#define DIR_CLK_B (DDRB |= (1 << DIR_B))
#define DIR_ACLK_B (DDRB &= ~(1 << DIR_B))

int main(void){

    DDRB |= (1 << LED);
    DDRB |= (1 << STEP_A); //| (1 << STEP_B);
    DDRB |= (1 << DIR_A); // | (1 << DIR_B);

    TIMER_init();
    UART_init(baud_rate);

    sei();

    flag = 0;

    setpointA = 0;
    setpointB = 0;

    steps_A = 0;
    steps_B = 0;

    pA = 0;
    pB = 0;

    position_A = 0;
    position_B = 0;

    while (1){
        if (flag){
            if (setpointA > position_A && steps_A != 0){
                ENA_INTA;
                DIR_CLK_A;
                printf("1");
            }
            else if (setpointA < position_A && steps_A != 0){
                ENA_INTA;
                DIR_ACLK_A;
                printf("2");
            }	

            if(setpointB > position_B && steps_B != 0){
                ENA_INTB;
                DIR_CLK_B;
                printf("3");
            }
            else if (setpointB < position_B && steps_B != 0){
                ENA_INTB;
                DIR_ACLK_B;
                printf("4");	
            }
    
        } else {
            // Blinking status LED
            PORTB ^= (1 << DDB5);
            _delay_ms(500);
        }
    }
}