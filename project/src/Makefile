
VPATH = src inc

main.hex: main.elf
	avr-objcopy -j .text -j .data -O ihex main.elf main.hex

main.elf: main.o
	avr-gcc -g -mmcu=atmega328p -o main.elf main.o

main.o: main.c
	avr-gcc -g -Os -mmcu=atmega328p -c main.c

upload: main.hex
	avrdude -v -p atmega328p -c arduino -P /dev/ttyUSB0 -b 57600 -D -U flash:w:main.hex:i

clean:
	-rm *.o *.elf
