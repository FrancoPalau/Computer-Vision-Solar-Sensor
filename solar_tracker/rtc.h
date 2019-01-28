/*
 * rtc.h
 *
 * Created: 20/03/2016 15:27:58
 *  Author: Jonathan
 */ 


#ifndef RTC_H_
#define RTC_H_

#include "i2c.h"

typedef struct
{
	uint8_t Second;	/* 0..59 */
	uint8_t Minute;	/* 0..59 */
	uint8_t Hour;	/* 1..7 */
}Hora_t;

typedef struct
{
	uint8_t Day;	/* 1.. 31 */
	uint8_t Month;	/* 1..12 */
	uint8_t Year;	/* 00..99 */	
}Fecha_t;

typedef struct
{
		Hora_t	hora;
		Fecha_t fecha;	
}RTC_t;

#define		DS3231_SECONDS			0x00
#define		DS3231_MINUTES			0x01
#define		DS3231_HOURS			0x02

#define		DS3231_WEEKDAY			0x03
#define		DS3231_DAYS				0x04
#define		DS3231_MONTHS			0x05
#define		DS3231_YEARS			0x06

#define		MASK_SEC			0b01111111
#define		MASK_MIN			0b01111111
#define		MASK_HORA			0b00111111
#define		MASK_DIA			0b00111111
#define		MASK_MES			0b00011111
#define		MASK_ANIO			0b11111111

#define		DS3231_READ			0b11010001
#define		DS3231_WRITE		0b11010000

uint8_t BCD_Decimal(uint8_t);
uint8_t Decimal_BCD(uint8_t);

void	RTC_Init();

uint8_t	DS3231_GetReg(uint8_t );
void	DS3231_SetReg(uint8_t , uint8_t );

void	RTC_SetHora (Hora_t* );
void	RTC_SetFecha(Fecha_t* );
void	RTC_GetHora (Hora_t* );
void	RTC_GetFecha(Fecha_t* );

void	RTC_GetTime(RTC_t *);
void	RTC_SetTime(RTC_t * );

#endif /* RTC_H_ */