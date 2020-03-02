avr-gcc -g -Os -mmcu=atmega328p -c main.c timer_config.c uart_config.c
avr-gcc -g -mmcu=atmega328p -o main.elf main.o timer_config.o uart_config.o
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
