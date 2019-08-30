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