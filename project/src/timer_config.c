#include "timer_config.h"

void TIMER_init(void){
    ICR1 = 5000;
    
    OCR1A = (ICR1 >> 1) & 0x7fff;
    OCR1B = (ICR1 >> 1) & 0x7fff;

    // Fast PWM mode configuration
    TCCR1A |= (1 << WGM11);
    TCCR1B |= (1 << WGM12) | (1 << WGM13);

    // Clear OC1A/OC1B on compare match, set OC1A/OC1B at BOTTOM (non-inverting mode)
    TCCR1A |= (1 << COM1A1) | (1 << COM1B1);

    // Prescaler configuration in 8 (clk_I/O / 8)
    TCCR1B |= (1 << CS11);

    // Disable interrupcion by compare match with OCR1A and OCR1B
    TIMSK1 |= (1 << OCIE1A);
    TIMSK1 |= (1 << OCIE1B);
}

ISR (TIMER1_COMPA_vect){
    ATOMIC_BLOCK(ATOMIC_FORCEON) {
        if (IS_ENA_INTA){
            pA++;
            printf("pa:%d\r\n", pA);
            if (pA == steps_A){
                position_A = setpointA;
                printf(":A=%d\r\n", position_A);
                pA = 0;
                steps_A = 0;
                DIS_INTA;
            }
            if(pA > steps_A){
                pA = 0;
                DIS_INTA;
		    }
        }
	}
}

ISR (TIMER1_COMPB_vect){
    ATOMIC_BLOCK(ATOMIC_FORCEON) {
        if (IS_ENA_INTB){
            pB++;
            printf("pb:%d\r\n", pB);
            if (pB == steps_B){
                position_B = setpointB;
                printf(":E=%d\r\n", position_B);
                pB = 0;
                steps_B = 0;
                DIS_INTB;
            }
            if(pB > steps_B){
                pB = 0;
                DIS_INTB;
            }
        }
	}
}
