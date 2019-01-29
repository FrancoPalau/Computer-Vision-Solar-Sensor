/*
* Variables.h
*
* Created: 2/7/2018 00:06:27
*  Author: lauta
*/
#include <avr/io.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "rtc.h"
#include "diskio.h"
#include "ff.h"

#ifndef VARIABLES_H_
#define VARIABLES_H_

#define DER_A	(PORTE|=(1<<DDE3))
#define DER_E	(PORTH|=(1<<DDH3))
#define IZQ_A	(PORTE &=~(1<<DDE3))	
#define IZQ_E	(PORTH &=~(1<<DDH3))
#define HORA_INF 6
#define HORA_SUP 21
#define PASO_SEG 5
#define SEG_HORA 3600
#define SEG_MIN	60
#define SEG_INF	21600
#define PASO 7.5
#define REDUCCION_A	8
#define REDUCCION_E	16
#define APAGADO 0
#define PRENDIDO 1

RTC_t rtc_uart,rtc;
unsigned int indcom0 = 0;
unsigned int cmd0 = 0;
char comando0[30];
uint8_t dia=0;
uint8_t mes=0;
uint32_t segundos=0;
int contador=0;
int nuevaFecha=0;
int nuevaHora=0;
int nuevaConsigna=0;
int estadoSensor = APAGADO;

FATFS fs;
FIL fin;
char line[80];
double posE=0;
double posA=0;
int pasosA=0;
int pasosE=0;
int pA=0;
int pE=0;
double consignaE=0;
double consignaA=0;
int flagHomingA=0;
int flagHomingE=0;
int finCarreraA;
int finCarreraE;
FRESULT res=FR_OK;
FRESULT res2=FR_OK;
int cantlineas;

void generarNombre(char*);
void homingA();
void homingE();
#endif /* VARIABLES_H_ */