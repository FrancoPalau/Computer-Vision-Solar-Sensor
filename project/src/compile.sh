avr-gcc -g -Os -mmcu=atmega328p -c main.c timer_config.c uart_config.c exint_config.c hw_logic.c
avr-gcc -g -mmcu=atmega328p -o main.elf main.o timer_config.o uart_config.o exint_config.o hw_logic.o
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
make clean
