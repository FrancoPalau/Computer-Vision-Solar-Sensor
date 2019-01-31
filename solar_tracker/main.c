/*
* CEDIACjunio.c
*
* Created: 8/6/2018 15:31:59
* Author : lauta
*/

#include "Timers.h"

int main(void)
{
	DDRD=0b11110011;
	inicializarExternas();
	inicializarTimer1();
	inicializarTimer2();
	inicializarTimer3();
	inicializarTimer5();
	RTC_Init();
	DESACT_T3;
	DESACT_T4;
	configuraUART0(myBaudRate0,1,0);
	stdout = stdin = &uart_io0;
	printf("UART0 funciona\r\n");
	sei();
	homingA();
	homingE();

	while (1)
	{
		if(estadoSensor == APAGADO){
			// Control a lazo abierto
			if(nuevaFecha==1)
			{
				char nombre[30];
				generarNombre(nombre);
				f_close(&fin);
				res = f_mount(0,&fs);
				if (res == FR_OK)
				{
					res = f_open(&fin,nombre, FA_OPEN_EXISTING | FA_READ);
				}
				nuevaFecha=0;
			}
			if(nuevaHora==1)
			{
				cantlineas=(segundos-SEG_INF)/PASO_SEG;
				int x=0;
				res2=f_lseek(&fin,0);
				if (res == FR_OK && res2==FR_OK)
				{
					do
					{
						f_gets(line, sizeof(line), &fin);
						x++;
					} while (x!=cantlineas);
					char* azimuth;
					char* elevacion;
					azimuth=strtok(line,",");
					elevacion=strtok(NULL,",");
					consignaA=atof(azimuth);
					consignaE=atof(elevacion);
					printf("Azimuth:%f---Elevacion:%f\r\n",consignaA,consignaE);
					pasosA=(int)(fabs(consignaA-posA)*REDUCCION_A/PASO);
					pasosE=(int)(fabs(consignaE-posE)*REDUCCION_E/PASO);
					printf("Pasos A: %d, Pasos E: %d\r\n",pasosA,pasosE);
				}
				nuevaHora=0;
			}
			if(nuevaConsigna==1)
			{
				if (res == FR_OK)
				{
					f_gets(line, sizeof(line), &fin);
					char* azimuth;
					char* elevacion;
					azimuth=strtok(line,",");
					elevacion=strtok(NULL,",");
					consignaA=atof(azimuth);
					consignaE=atof(elevacion);
					printf("Azimuth:%f---Elevacion:%f\r\n",consignaA,consignaE);
					pasosA=(int)(fabs(consignaA-posA)*REDUCCION_A/PASO);
					pasosE=(int)(fabs(consignaE-posE)*REDUCCION_E/PASO);
					printf("Pasos A: %d, Pasos E: %d\r\n",pasosA,pasosE);
				}
				nuevaConsigna=0;
			}
		}
		if(flagHomingA==1 && flagHomingE==1)
		{
			if(consignaA>posA && pasosA!=0)
			{
				ACT_INT_T3;
				ACTIVAR_T3;
				IZQ_A;
			}
			else if (consignaA<posA && pasosA!=0)
			{
				ACT_INT_T3;
				ACTIVAR_T3;
				DER_A;
			}			
			if(consignaE>posE && pasosE!=0)
			{
				ACT_INT_T4;
				ACTIVAR_T4;
				DER_E;
			}
			else if (consignaE<posE && pasosE!=0)
			{
				ACT_INT_T4;
				ACTIVAR_T4;
				IZQ_E;		
			}
		}
		else
		{
			homingA();
			homingE();
		}
	}
	return 0;
}

void generarNombre(char* nombre){
	if(dia<10)
	{
		if (mes<10)
		{
			sprintf(nombre,"0%d0%d.txt",dia,mes);
		}
		else
		{
			sprintf(nombre,"0%d%d.txt",dia,mes);
		}
	}
	else
	{
		if (mes<10)
		{
			sprintf(nombre,"%d0%d.txt",dia,mes);
		}
		else
		{
			sprintf(nombre,"%d%d.txt",dia,mes);
		}
	}
}

void homingA(){
	ACTIVAR_T3;
	DESACT_INT_T3;
	printf("Entre homingA\r\n");
	while(!finCarreraA){
		IZQ_A;
	}
	_delay_ms(100);
	while(finCarreraA){
		DER_A;
	}
	DESACT_T3;
	TIMER3_TOP;
	printf("Sali HomingA\r\n");
	posA=0;
	consignaA=0;
	flagHomingA=1;
	PORTE &= ~(1<<4);
}

void homingE(){
	ACTIVAR_T4;
	DESACT_INT_T4;
	printf("Entre homingE\r\n");
	while(!finCarreraE){
		IZQ_E;
	}
	_delay_ms(100);
	while(finCarreraE){
		DER_E;
	}
	DESACT_T4;
	TIMER4_TOP;
	printf("Sali HomingE\r\n");
	posE=0;
	consignaE=0;
	flagHomingE=1;
	PORTH &= ~(1<<4);
}




