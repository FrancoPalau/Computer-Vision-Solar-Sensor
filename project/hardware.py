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
    changeDir()
        stepper motor will change direction
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
        vel : int, optional
            The initial frequency (angular velocity) of the stepper motor. By default the initial frequency
            is 25 Hz.
        """
        self.DIR_PIN = dir
        self.STEP_PIN = step

        self.DIR = 0
        GPIO.setup(dir, GPIO.OUT, initial=0)

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

    def changeDir(self):
        """Change the direction of the stepper motor to the
        opposite
        """
        self.DIR = not(self.DIR)
        GPIO.output(self.DIR_PIN, self.DIR)


#--------------------------------------------------------------

def finc_interrupt(channel):
    """ Interruption routune to change the direction of
    the stepper motor. Only for the purpose of testing
    """
    print("HOME")
    mA.changeDir()


if __name__ == "__main__":
    """ Hardware test:
    The following code seeks to verify the correct functioning 
    of the hardware. 
    It consists of the slow start-up of a stepper motor, which 
    changes its direction of rotation each time an entry is 
    given with the limit switch.
    """

    GPIO.setmode(GPIO.BOARD)

    LED_BLINK = 11
    ledstate = False
    GPIO.setup(LED_BLINK, GPIO.OUT, initial=ledstate)

    FINC_1 = 12
    GPIO.setup(FINC_1, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(FINC_1, GPIO.BOTH, finc_interrupt, 500)
    

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

