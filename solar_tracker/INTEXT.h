/*
* INTEXT.h
*
* Created: 2/7/2018 15:27:03
*  Author: lauta
*/

#include "Variables.h"

#ifndef INTEXT_H_
#define INTEXT_H_

void inicializarExternas(){
	EICRA=(1<<ISC30)|(1<<ISC20);
	EIMSK=(1<<INT2)|(1<<INT3);
}

ISR(INT2_vect){
	//printf("Entre\r\n");
	if(PIND&(1<<PIND2)){
		finCarreraA=0;
		}else{
		finCarreraA=1;
	}
}

ISR(INT3_vect){
	//printf("Entre\r\n");
	if(PIND&(1<<PIND3)){
		finCarreraE=0;
		}else{
		finCarreraE=1;
	}
}

#endif /* INTEXT_H_ */