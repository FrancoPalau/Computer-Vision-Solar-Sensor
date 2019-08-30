
#ifndef UART_CONFIG_H_
#define UART_CONFIG_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#include "timer_config.h"
#include "hw_logic.h"

#ifndef F_CPU
#define F_CPU 16000000
#endif

#define getc() _getc(&uart_io)
#define putc(x) _putc(x, &uart_io)

#define baud_rate 9600

#define PASO 7.5
#define REDUCCION_A	8
#define REDUCCION_B	8

FILE uart_io;

void UART_init(unsigned int ubrr);

int _putc(char c, FILE *stream);
int _getc(FILE *stream);

void interprete(void);

char command[30];
unsigned int indcom;

ISR (USART_RX_vect);

#endif /* UART_CONFIG_H_ */