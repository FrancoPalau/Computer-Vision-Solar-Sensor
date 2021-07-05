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

from hardware import Stepper, limitswitch_setup
from homing import int_homing, homing_process


if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # LED blinking as visual indicator
    LED_BLINK = 11
    ledstate = False
    GPIO.setup(LED_BLINK, GPIO.OUT, initial=ledstate)

    # Limit switch A setup
    FINC_A = 12
    limitswitch_setup(FINC_A, 'PUD_DOWN', RISING=True, int_routine=int_homing)

    # Limit switch 2 setup
    FINC_B = 22
    limitswitch_setup(FINC_B, 'PUD_DOWN', RISING=True, int_routine=int_homing)

    # Stepper A setup
    mA = Stepper(13, 16)

    # Stepper B setup
    mB = Stepper(15, 18)

    try:
        # Homing process of both stepper motors
        homing_process(mA, mB)

        while (1):
            time.sleep(0.5)
            ledstate = not(ledstate)
            GPIO.output(LED_BLINK, ledstate)

    except KeyboardInterrupt:
        mA.stop()
        mB.stop()
        GPIO.cleanup()
        print("\nExiting...")
        # Acá hacer el processes join
