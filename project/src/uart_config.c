#include "uart_config.h"

// Declara un parámetro tipo stream de E/S para igualar los parámetros en stdio
FILE uart_io = FDEV_SETUP_STREAM(_putc, _getc, _FDEV_SETUP_RW);

void UART_init(unsigned int ubrr){

    stdout = stdin = &uart_io;
    indcom = 0;

	UBRR0 = F_CPU/16/ubrr-1;
	UCSR0A = 0;
	UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
	UCSR0C = (1 << USBS0) | (3 << UCSZ00);
}

//	Función de TRANSMISIÓN
int _putc(char c, FILE *stream){
	while (!(UCSR0A & (1<<UDRE0))); // Espera mientras buffer de transmisión esté ocupado
	UDR0=c; // UDR0 recibe el nuevo dato c a transmitir
	return 0;
}

//	Función de RECEPCIÓN
int _getc(FILE *stream){
	while (!(UCSR0A & (1<<RXC0)));  // Espera mientras la recepción no esté completa
	return UDR0;    // Cuando se completa, se lee UDR0
}

void interprete(void){
	int aux = 0;
	switch(command[0]){
		case 'Z':
            aux = atoi(&command[1]);
            setpointA = (float)aux*PASO/(float)REDUCCION_A + position_A;
            steps_A = abs(aux);
            printf("Azi:%f---Ele:%f\r\n", setpointA, setpointB);
            printf("PA: %d, PE: %d\r\n", steps_A, steps_B);
            printf("AziCurr:%f---EleCurr:%f\r\n", position_A, position_B);
            break;

        case 'E':
            aux = atoi(&command[1]);
            setpointB = (float)aux*PASO/(float)REDUCCION_B + position_B;
            steps_B = abs(aux);
            printf("Azi:%f---Ele:%f\r\n", setpointA, setpointB);
            printf("PA: %d, PE: %d\r\n", steps_A, steps_B);
            break;
        
        case 'T':
            flag ^= 1;
            break;

		default:
			break;
	}
}


ISR (USART_RX_vect){
    char dato=getc();
    printf("%c", dato);
    switch (dato) {
        case ':':
            indcom = 0;
            break;

        case '\r':
            command[indcom] = 0;
            interprete();
            break;

        default:
            command[indcom++] = dato;
            break;
    }
}