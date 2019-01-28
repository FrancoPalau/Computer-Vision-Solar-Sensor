/*
* rtc.c
*
* Created: 20/03/2016 15:37:58
*  Author: Jonathan
*/

#include "rtc.h"

uint8_t BCD_Decimal(uint8_t numero){
	return (((numero&0xF0)>>4)*10+(numero&0x0F));
}

uint8_t Decimal_BCD(uint8_t numeroB){
	return (((numeroB/10)<<4) +(numeroB%10));
}

void RTC_Init()
{
	I2C_Init();
}

uint8_t DS3231_GetReg( uint8_t address)
{
	uint8_t	ret;
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(address);
	I2C_ReStart();
	I2C_Write(DS3231_READ);
	ret = I2C_Read(NACK);
	I2C_Stop();
	return ret;
}

void DS3231_SetReg( uint8_t address, uint8_t val)
{
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(address);
	I2C_Write(val);
	I2C_Stop();
}

void RTC_SetHora( Hora_t * hora)
{
	hora->Second=Decimal_BCD(hora->Second);
	hora->Minute=Decimal_BCD(hora->Minute);
	hora->Hour=Decimal_BCD(hora->Hour);
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(DS3231_SECONDS);
	I2C_Write(hora->Second);
	I2C_Write(hora->Minute);
	I2C_Write(hora->Hour);
	I2C_Stop();
}

void RTC_SetFecha( Fecha_t * fecha)
{
	fecha->Day=Decimal_BCD(fecha->Day);
	fecha->Month=Decimal_BCD(fecha->Month);
	fecha->Year=Decimal_BCD(fecha->Year);
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(DS3231_DAYS);
	I2C_Write(fecha->Day);
	I2C_Write(fecha->Month);
	I2C_Write(fecha->Year);
	I2C_Stop();
}

void RTC_GetHora( Hora_t* hora)
{
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(DS3231_SECONDS);
	I2C_ReStart();
	I2C_Write(DS3231_READ);
	hora->Second = (I2C_Read(ACK))& MASK_SEC;
	hora->Minute = (I2C_Read(ACK))& MASK_MIN;
	hora->Hour   = (I2C_Read(NACK))& MASK_HORA;
	I2C_Stop();
	hora->Second=BCD_Decimal(hora->Second);
	hora->Minute=BCD_Decimal(hora->Minute);
	hora->Hour=BCD_Decimal(hora->Hour);
}

void RTC_GetFecha( Fecha_t* fecha )
{
	I2C_Start();
	I2C_Write(DS3231_WRITE);
	I2C_Write(DS3231_DAYS);
	I2C_ReStart();
	I2C_Write(DS3231_READ);
	fecha->Day   = (I2C_Read(ACK)) & MASK_DIA;
	fecha->Month = (I2C_Read(ACK)) & MASK_MES;
	fecha->Year  = (I2C_Read(NACK)) & MASK_ANIO;
	I2C_Stop();
	fecha->Day=BCD_Decimal(fecha->Day);
	fecha->Month=BCD_Decimal(fecha->Month);
	fecha->Year=BCD_Decimal(fecha->Year);
}

void RTC_GetTime( RTC_t * rtc)
{
	RTC_GetHora(&rtc->hora);
	RTC_GetFecha(&rtc->fecha);
}

void RTC_SetTime( RTC_t * rtc)
{
	RTC_SetHora(&rtc->hora);
	RTC_SetFecha(&rtc->fecha);
}

