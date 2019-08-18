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

# from time_handling import flag_date, flag_hour
from time_handling import second, day, month
from time_handling import PASO_SEG, SEG_INF 


def data_process():

    flag_date = 1
    flag_hour = 1

    while (1):

        if (flag_date):
            # Obtain the name of the file
            file_name = "/home/gonzalof/PARABOLA/" + get_name(day, month)
            flag_date = 0
        
        if (flag_hour):
            lines_count = (second - SEG_INF) / PASO_SEG
            fp = open(file_name)
            for i, line in enumerate(fp):
                if (i > lines_count):
                    set_point = line
                    break
            [azim, elev] = [float(s) for s in set_point.strip().split(",")]
            print(azim, elev)

        time.sleep(1)



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


if __name__ == "__main__":

    data_process()