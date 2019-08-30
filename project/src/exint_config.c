#include "exint_config.h"

void EXINT_init(void){
    EICRA|=(1<<ISC00);
    EIMSK|=(1<<INT0);

    EICRA|=(1<<ISC10);
    EIMSK|=(1<<INT1);
}

ISR(INT0_vect){
	if(PIND & (1 << PIND2)){
		limswitchA=0;
	} else {
		limswitchA=1;
	}
}

ISR(INT1_vect){
	if(PIND & (1 << PIND3)){
		limswitchB = 0;
	} else {
		limswitchB = 1;
	}
}
