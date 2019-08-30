
#ifndef F_CPU
#define F_CPU 16000000UL 
#endif
 
#include <avr/io.h>
#include <util/delay.h>

#include "timer_config.h"
#include "uart_config.h"
#include "hw_logic.h"

int main(void){

    TIMER_init();
    UART_init(baud_rate);
    HW_init();

    sei();

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