""" Actualmente migrando el proyecto desde Arduino a RPi3

    Autores:
    - Lautaro Delgado
    - Franco Palau
    - Gonzalo Fernández

    Migración de C a Python:
    - Gonzalo Fernández
"""

# TO DO: 
# - Error handling
# - Move homing routine to homing.py

import time
import RPi.GPIO as GPIO

import os
from multiprocessing import Process

if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # LED blinking as visual indicator
    LED_BLINK = 11
    ledstate = False
    GPIO.setup(LED_BLINK, GPIO.OUT, initial=ledstate)

    try:

        while (1):
            time.sleep(0.5)
            ledstate = not(ledstate)
            GPIO.output(LED_BLINK, ledstate)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nExiting...")
        # Acá hacer el processes join
