/*
 * I2C.h
 *
 * Created: 20/03/2016 15:09:28
 *  Author: Jonathan
 */ 


#ifndef I2C_H_
#define I2C_H_

#include <avr/io.h>
#include <util/twi.h>

#define		NACK	0
#define		ACK		1
#define		F_SCL	100000 

void		I2C_Init(void);
uint8_t		I2C_Start(void);
uint8_t		I2C_ReStart(void);
void		I2C_Stop(void);
uint8_t		I2C_Write(uint8_t );
uint8_t		I2C_Read(uint8_t );

#endif /* I2C_H_ */



