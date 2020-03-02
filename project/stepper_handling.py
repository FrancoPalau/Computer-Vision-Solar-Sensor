""" Actualmente migrando el proyecto desde Arduino a RPi3

    Autores:
    - Lautaro Delgado
    - Franco Palau
    - Gonzalo Fernández

    Migración de C a Python:
    - Gonzalo Fernández
"""

from homing import flag_homingA, flag_homingB

# TO DO: 
# - Error handling

# Hardware variables
REDUCTION_A = 8
REDUCTION_B = 8
STEP = 7.5

# Current position global variables
position_A = 0
position_B = 0

# Setpoint global variables
setpoint_A = 0
setpoint_B = 0

# Steps to do global variables
steps_A = 0
steps_B = 0

# Counter for PWM control
count_A = 0
count_B = 0


def calc_step(id):
    """Calculate the number of steps to take based on the 
    setpoint and the current position

    Parameters
    ----------
    id : char
        The stepper motor's id (A or B)

    Returns
    -------
    int
        the number of steps to take
    """

    if (id == 'A'):
        reduction = REDUCTION_A
        setpoint = setpoint_A
        position = position_A
    elif (id == 'B'):
        reduction = REDUCTION_B
        setpoint = setpoint_B
        position = position_B

    step = int((setpoint - position) * reduction / STEP)
    
    return step


def stepperA_process(m):
    """Stepper motor A control process

    Parameters
    ----------
    m : Stepper
        Stepper object with all the motor setup
    """

    while (1):
        if (flag_homingA and flag_homingB):
            if ((setpoint_A > position_A) and (steps_A != 0)):
                m.changeDir(1) # Clockwise rotation?
                m.start()
            
            if ((setpoint_A < position_A) and (steps_A != 0)):
                m.changeDir(0) # Anticlockwise rotation?
                m.start()

        else:
            # Ejecutar homing

    return


def stepperB_process(m):
    """Stepper motor B control process

    Parameters
    ----------
    m : Stepper
        Stepper object with all the motor setup
    """

    active = 0

    while (1):
        if (flag_homingA and flag_homingB):
            if ((setpoint_B > position_B) and (steps_B != 0)):
                m.changeDir(1) # Clockwise rotation?
                active = 1
            
            if ((setpoint_B < position_B) and (steps_B != 0)):
                m.changeDir(0) # Anticlockwise rotation?
                active = 1

        if (active):
            mA.
            count_A += 1


        else:
            # Ejecutar homing

    return


# if __name__ == "__main__":
