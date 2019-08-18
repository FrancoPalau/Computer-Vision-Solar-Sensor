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


def homing(channel):
    """ Interruption routine in the homing process once 
    the limit switch is pressed
    """

    global FINC_A, FINC_B
    global mA, mB

    print("Limit switch pressed")
    
    if (channel == FINC_A):
        mA.stop()
        mA.changeDir()
        mA.changeVel(10)
        mA.start()
        while (GPIO.input(FINC_A)):
            time.sleep(0.1)
        mA.stop()
        print("Limit Switch A unpressed")
        mA.changeVel(30)
    
    if (channel == FINC_B):
        mB.stop()
        mB.changeDir()
        mB.changeVel(10)
        mB.start()
        while (GPIO.input(FINC_B)):
            time.sleep(0.1)
        mB.stop()
        print("Limit Switch B unpressed")
        mB.changeVel(30)

    return


if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # LED blinking as visual indicator
    LED_BLINK = 11
    ledstate = False
    GPIO.setup(LED_BLINK, GPIO.OUT, initial=ledstate)

    # Limit switch A setup
    FINC_A = 12
    limitswitch_setup(FINC_A, 'PUD_DOWN', RISING=True, int_routine=homing)

    # Limit switch 2 setup
    FINC_B = 22
    limitswitch_setup(FINC_B, 'PUD_DOWN', RISING=True, int_routine=homing)

    # Stepper A setup
    mA = Stepper(13, 16)
    mA.start()

    # Stepper B setup
    mB = Stepper(15, 18)
    mB.start()

    try:
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
