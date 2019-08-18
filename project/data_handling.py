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
    
    month = datetime.now().month
    day = datetime.now().day

    fin = get_name(day, month)
    print(fin)