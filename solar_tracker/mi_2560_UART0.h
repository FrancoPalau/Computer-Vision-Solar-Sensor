
#include "INTEXT.h"

#define  myBaudRate0 57600


int mi_putc0(char c, FILE *stream)
{
	while(!(UCSR0A&(1<<UDRE0))); // Espera mientras buffer de transmisión esté ocupado
	UDR0 = c;					 // UDR0 recibe el nuevo dato c a transmitir
	return 0;
}

int mi_getc0(FILE *stream)
{
	while (!(UCSR0A&(1<<RXC0))); // Espera mientras la recepción no esté completa
	return UDR0;				 // Cuando se completa, se lee UDR0
}

// Redefinimos las primitivas de E/S para recibir/transmitir caracteres por UART
#define fgetc()  mi_getc0(&uart_io0)
#define fputc(x) mi_putc0(x,&uart_io0)

// Declara un parámetro tipo stream de E/S para igualar los parámetros en stdio
FILE uart_io0 = FDEV_SETUP_STREAM(mi_putc0, mi_getc0, _FDEV_SETUP_RW);

void configuraUART0(uint32_t BAUD, uint8_t intRx, uint8_t intTx)
{
	//Parámetros de la comunicación
	UBRR0   =  F_CPU/16/BAUD-1;	// Configura baudrate
	UCSR0A &=~ (1<<U2X0);		// Velocidad simple (1 para doble)
	UCSR0B |=  (1<<RXEN0);		// Habilita recepción
	UCSR0B |=  (1<<TXEN0);		// Habilita transmisión
	UCSR0C |=  (1<<USBS0);		// 2 bits de STOP
	UCSR0C |=  (3<<UCSZ00);		// 8 bits de dato
	//El stream (FILE) uart_io es la E/S estandar, es decir para fputc y fgetc
	//stdout = stdin = &uart_io0;
	if(intRx)
	{
		UCSR0A &=~ (1<<RXC0);	//Apaga flag de interrupción por Recepción Completa
		UCSR0B |=  (1<<RXCIE0);	//Habilita interrupción RX
	}
	if(intTx)
	{
		UCSR0A &=~ (1<<TXC0);	//Apaga flag de interrupción por Transmisión Completa
		UCSR0B |=  (1<<TXCIE0);	//Habilita interrupción TX
	}
}

void interpretaComando0()
{
	int aux = 0;
	switch(comando0[0])		
	{
		case 'S':
			switch(comando0[1]){
				case 'A':
					estadoSensor = APAGADO;
					printf("Sensor Apagado\r\n");
					break;
				case 'P':
					estadoSensor = PRENDIDO;
					printf("Sensor Prendido\r\n");
					break;
				case 'Z':
					aux = atoi(&comando0[2]);
					consignaA = (float)aux*PASO/(float)REDUCCION_A + posA;
					pasosA = abs(aux);
					printf("Azi:%f---Ele:%f\r\n",consignaA,consignaE);
					printf("PA: %d, PE: %d\r\n",pasosA,pasosE);
					break;
				case 'E':
					aux = atoi(&comando0[2]);
					consignaE = (float)aux*PASO/(float)REDUCCION_E + posE;
					pasosE = abs(aux);
					printf("Azi:%f---Ele:%f\r\n",consignaA,consignaE);
					printf("PA: %d, PE: %d\r\n",pasosA,pasosE);
					break;
				default:
					break;	
			}			
			break;						
		case 'U':
			rtc_uart.fecha.Day=(int)(comando0[1]-'0')*10+(int)(comando0[2]-'0');
			rtc_uart.fecha.Month=(int)(comando0[4]-'0')*10+(int)(comando0[5]-'0');
			rtc_uart.fecha.Year=(int)(comando0[7]-'0')*10+(int)(comando0[8]-'0');
			rtc_uart.hora.Hour=(int)(comando0[10]-'0')*10+(int)(comando0[11]-'0');
			rtc_uart.hora.Minute=(int)(comando0[13]-'0')*10+(int)(comando0[14]-'0');
			rtc_uart.hora.Second=(int)(comando0[16]-'0')*10+(int)(comando0[17]-'0');
			RTC_SetTime(&rtc_uart);
			break;
		default:
			break;
	}
}

ISR(USART0_RX_vect)
{
	char dato;
	dato=fgetc();
	switch(dato)
	{
		case ':':	// Delimitador de inicio
		indcom0=0;   // Inicializa índice de buffer de recepción
		cmd0 = 1;	// Comando en curso
		break;
		
		case 8:		// Basckspace
		if(indcom0>0) indcom0--;
		break;
		
		case '\r':	// Delimitador de final
		if(cmd0==1)				 // Si hay comando en curso
		{
			comando0[indcom0] = 0; // coloca NULL luego del último caracter recibido
			interpretaComando0(); // Llama a función interprete de comandos
			cmd0 = 0;			 // fin de comando en curso
		}
		break;
		default:				// Todo lo que está entre delimitadores, Ej. 'T','3','4','2'
		if(indcom0<30) comando0[indcom0++]=dato; // Guarda en elemento del buffer e incrementa indcom para apuntar a siguiente
		break;
	}
	UCSR0A &=~ (1<<RXC0);	//Apaga el flag de interrupción por RX
}



