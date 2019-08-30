
#include "hw_logic.h"

#include "timer_config.h"
#include "exint_config.h"

void HW_init(void){
    DDRB |= (1 << LED);
    DDRB |= (1 << STEP_A) | (1 << STEP_B);
    DDRB |= (1 << DIR_A) | (1 << DIR_B);

    flagHomingA = 0;
    flagHomingB = 0;

    pA = 0;
    pB = 0;

    position_A = 0;
    position_B = 0;

    flag = 0;

    setpointA = 0;
    setpointB = 0;

    steps_A = 0;
    steps_B = 0;
}

// REVISAR HOMING 
// NO SE TIENEN QUE EJECUTAR LAS RUTINAS DE INTERRUPCION
/*
void homingA(void){

    DIS_INTA;
	printf(":HA\r\n");

	while(!limswitchA){
		DIR_ACLK_A;
	}
	_delay_ms(100);

	while(limswitchA){
		DIR_CLK_A;
	}

	DIS_INTA;
	printf(":HAD\r\n");
	position_A = 0;
	setpointA = 0;
	flagHomingA=1;
	// PORTE &= ~(1<<4); Y esto?
}

void homingE(){
	
    DIS_INTB;
	printf(":HE\r\n");

	while(!limswitchB){
		DIR_ACLK_B;
	}
	_delay_ms(100);

	while(limswitchB){
		DIR_CLK_B;
	}
	DESACT_T4;
	TIMER4_TOP;
	printf("Sali HomingE\r\n");
	posE=0;
	consignaE=0;
	flagHomingE=1;
	// PORTH &= ~(1<<4); Y esto?
}
*/