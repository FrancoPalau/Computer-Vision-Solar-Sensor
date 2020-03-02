""" Actualmente migrando el proyecto desde Arduino a RPi3

    Autores:
    - Lautaro Delgado
    - Franco Palau
    - Gonzalo Fernández

    Migración de C a Python:
    - Gonzalo Fernández
"""

# TO DO: Error handling

from datetime import datetime
import time

from time_handling import second, day, month
from time_handling import PASO_SEG, SEG_INF
from time_handling import flag_date, flag_hour, flag_setpoint

from stepper_handling import setpoint_A, setpoint_B
from stepper_handling import calc_step, steps_A, steps_B


# Database path
PATH = "/home/gonzalof/PARABOLA/"


def data_process():

    # Esto no se si esta bien,
    # Poner todos los flags activos al iniciar el proceso
    flag_date = 1
    flag_hour = 1
    flag_setpoint = 1

    while (1):

        if (flag_date):
            # Obtain the name of the file
            file_name = PATH + get_name(day, month)

            flag_date = 0
        
        if (flag_hour):
            lines_count = (second - SEG_INF) / PASO_SEG
            
            # Obtain azimuth and elevation coordinates
            setpoint_A, setpoint_B = get_coord(file_name, lines_count)

            # setpoint_A = azimuth
            # setpoint_B = elevation
            print(setpoint_A, setpoint_B)

            # Number of steps to take based on the setpoint and the current position
            steps_A = calc_step('A')
            steps_B = calc_step('B')

            print(steps_A, steps_B)

            flag_hour = 0

        if (flag_setpoint):
            # Obtain azimuth and elevation coordinates
            setpoint_A, setpoint_B = get_coord(file_name, lines_count)

            # Number of steps to take based on the setpoint and the current position
            steps_A = calc_step('A')
            steps_B = calc_step('B')

            flag_setpoint = 0

        time.sleep(1)

    return


def get_name(day, month):
    """Search the name of the file in the database based on 
    the date received

    Parameters
    ----------
    day : int
        The day of the date received
    month : int
        The month of the date received

    Returns
    -------
    str
        the name of the file corresponding to the date received
    """

    if (day < 10):
        if (month<10):
            return ("0%d0%d.txt" % (day, month))
        else:
            return ("0%d%d.txt" % (day, month))
    else:
        if (month<10):
            return ("%d0%d.txt" % (day, month))
        else:
            return ("%d%d.txt" % (day, month))

    
def get_coord(file_name, lines_count):
    """Obtain azimuth and elevation coordinates

    Parameters
    ----------
    file_name : str
        File name in the database corresponding to a certain date
    lines_count : int
        Line number in the file given a certain count of seconds

    Returns
    -------
    float, float
        the setpoint_A and setpoint_B for the right coordinates
    """

    fp = open(file_name)
    for i, line in enumerate(fp):
        if (i > lines_count):
            set_point = line
            break
    [setpoint_A, setpoint_B] = [float(s) for s in set_point.strip().split(",")]

    return setpoint_A, setpoint_B


if __name__ == "__main__":

    data_process()