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

from stepper_handling import position_A, position_B
from stepper_handling import setpoint_A, setpoint_B

flag_homingA = 0
flag_homingB = 0


def homing_process(mA, mB):
    """ Sequential homing process of both stepper motors
    
    Parameters
    ----------
    mA : Stepper
        First stepper to execute homing process
    mB : Stepper
        Second stepper to execute homing process
    """

    mA.start()
    while (not flag_homingA)

    mB.start()
    while (not flag_homingB)

    return


def int_homing(channel):
    """Interruption routine in the homing process once 
    the limit switch is pressed

    Parameters
    ----------
    channel : int
        Since it's an interruption routine, it receives as a parameter the channel (or pin) in which the interruption occurred
    """

    global FINC_A, FINC_B
    global mA, mB

    print("Limit switch pressed")
    
    # Interruption associated to homing A
    if (channel == FINC_A):
        mA.stop()
        mA.changeDir(1)
        mA.changeVel(10)
        mA.start()
        while (GPIO.input(FINC_A)):
            time.sleep(0.1)
        mA.stop()
        print("Limit Switch A unpressed")
        mA.changeVel(30)

        position_A = 0  # Current position update
        setpoint_A = 0  # Setpoint update
        flag_homingA = 1
    
    # Interruption associated to homing B
    if (channel == FINC_B):
        mB.stop()
        mB.changeDir(1)
        mB.changeVel(10)
        mB.start()
        while (GPIO.input(FINC_B)):
            time.sleep(0.1)
        mB.stop()
        print("Limit Switch B unpressed")
        mB.changeVel(30)

        position_B = 0  # Current position update
        setpoint_B = 0  # Setpoint update
        flag_homingB = 1

    return


if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # Limit switch A setup
    FINC_A = 12
    limitswitch_setup(FINC_A, 'PUD_DOWN', RISING=True, int_routine=homing)

    # Limit switch 2 setup
    FINC_B = 22
    limitswitch_setup(FINC_B, 'PUD_DOWN', RISING=True, int_routine=homing)

    # Stepper A setup
    mA = Stepper(13, 16)

    # Stepper B setup
    mB = Stepper(15, 18)

    try:
        homing_process()

    except KeyboardInterrupt:
        mA.stop()
        mB.stop()
        GPIO.cleanup()
        print("\nExiting...")

