""" Rutinas de homing de los motores y finales de carrera correspondientes
    Actualmente migrando el proyecto desde Arduino a RPi3

    Autores:
    - Lautaro Delgado
    - Franco Palau
    - Gonzalo Fernández

    Migración de C a Python:
    - Gonzalo Fernández
"""

# TO DO: Error handling

import time
import RPi.GPIO as GPIO

from hardware import Stepper, limitswitch_setup


def homing(channel):
    """ Interruption routine in the homing process once 
    the limit switch is pressed
    """

    global mA

    mA.stop()
    mA.changeDir()
    mA.changeVel(10)
    mA.start()
    while (GPIO.input(channel)):
        time.sleep(0.1)
    mA.stop()
    mA.changeVel(30)

    return


if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # LED blinking as visual indicator
    LED_BLINK = 11
    ledstate = False
    GPIO.setup(LED_BLINK, GPIO.OUT, initial=ledstate)

    # Limit switch setup
    FINC_1 = 12
    limitswitch_setup(FINC_1, 'PUD_DOWN', RISING=True, int_routine=homing)

    # Stepper A setup
    mA = Stepper(13, 16)
    mA.start()

    try:
        while (1):
            time.sleep(0.5)
            ledstate = not(ledstate)
            GPIO.output(LED_BLINK, ledstate)

    except KeyboardInterrupt:
        mA.stop()
        GPIO.cleanup()
        print("\nExiting...")

