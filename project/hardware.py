""" Clases y funciones asociadas al hardware del proyecto
    Actualmente migrando el proyecto desde Arduino a RPi3

    Autores:
    - Lautaro Delgado
    - Jona
    - Franco Palau
    - Gonzalo Fernández

    Migración de C a Python:
    - Gonzalo Fernández
"""

# TO DO: Error handling

import time
import RPi.GPIO as GPIO

class Stepper:
    """
    A class used to group stepper motor settings

    ...

    Attributes
    ----------
    DIR : GPIO.OUT
        direction of the stepper motor
    STEP : GPIO.PWM
        PWM for steps of the stepper motor

    Methods
    -------
    start(duty_cycle=60)
        stepper motor will start moving
    stop()
        stepper motor will stop moving
    """

    def __init__(self, dir, step, vel=25):
        """Configure a RPi pin to do PWM (Pulse Width Modulation)
        with GPIO module

        Parameters
        ----------
        dir : int
            The RPI's pin to set as direction of the stepper motor.
            This pin will be connected to the DIR pin in the 
            Pololu's stepper motor driver (like the A4988).
        step : int
            The RPI's pin to set as PWM for steps of the stepper motor.
            This pin will be connected to the STEP pin in the 
            Pololu's stepper motor driver (like the A4988).
        """
        self.DIR = GPIO.setup(dir, GPIO.OUT, initial=0)
        GPIO.setup(step, GPIO.OUT)
        self.STEP = GPIO.PWM(step, vel)
    
    def start(self, duty_cycle=60):
        """PWM enabled and the stepper motor will start moving
        at the frequency setted

        Parameters
        ----------
        duty_cycle : float, optional
            Specify the PWM's duty cycle for the steps wave
            (default is 60%).
        """
        self.STEP.start(60)
    
    def stop(self):
        """PWM disabled and the stepper motor will stop moving
        """
        self.STEP.stop()


if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)

    # Stepper A setup
    mA = Stepper(13, 16)
    mA.start()

    try:
        while (1):
            time.sleep(0.1)

    except KeyboardInterrupt:
        mA.stop()
        GPIO.cleanup()
        print("\nExiting...")

