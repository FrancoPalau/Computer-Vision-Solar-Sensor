/*
 * i2c.c
 *
 * Created: 20/03/2016 15:12:07
 *  Author: Jonathan
 */ 

#include "i2c.h"

void	I2C_Init(void)
{
	TWSR &=~ (3<<TWPS0);
	uint32_t TWBR_val;
	TWBR_val = ( (F_CPU/F_SCL-16)/(2*1) );
	TWBR = (uint8_t)TWBR_val;
}


uint8_t I2C_Start( void )
{
	TWCR = (1<<TWINT)|(1<<TWSTA)|(1<<TWEN);
	
	while (!(TWCR & (1<<TWINT)));
	
	if ((TWSR & 0xF8) != TW_START)
		return 0;
	
	return 1;
}


uint8_t I2C_ReStart( void )
{
	TWCR = (1<<TWINT)|(1<<TWSTA)|(1<<TWEN);
	
	while (!(TWCR & (1<<TWINT)));
	
	if ((TWSR & 0xF8) != TW_REP_START)
		return 0;
	
	return 1;
}


void I2C_Stop( void )
{
	TWCR = (1<<TWINT)|(1<<TWEN)|(1<<TWSTO);
	while(TWCR & (1<<TWSTO));
}

uint8_t I2C_Write( uint8_t data)
{
	TWDR = data;
	
	TWCR = (1<<TWINT)|(1<<TWEN) ;
	
	while (!(TWCR & (1<<TWINT)));
	
	if ((TWSR & 0xF8) != TW_MT_SLA_ACK)
		return 0;
	
	return 1;
}


uint8_t I2C_Read( uint8_t ACK_NACK)
{
	while (!(TWCR & (1<<TWINT)));
	
	TWCR = (ACK_NACK)?((1<<TWINT)|(1<<TWEN)|(1<<TWEA)):((1<<TWINT)|(1<<TWEN));
	
	while (!(TWCR & (1<<TWINT)));
	
	return	TWDR;
}