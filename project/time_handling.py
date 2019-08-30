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
# - Ver que es PASO_SEG y SEG_INF
# - Ver mejor cuando actualizar y declarar cada cosa


from datetime import datetime
import time

PASO_SEG = 5 # Que es esto??
SEG_INF = 21600 # Y esto?

HOUR_INF = 6
HOUR_SUP = 21

SEC_HOUR = 3600
SEC_MIN = 60

flag_hour = 0
flag_date = 0
flag_setpoint = 0

month = datetime.now().month
day = datetime.now().day
second = datetime.now().second


def time_process():

    # Date and hour update in the creation of the process
    # Ver mejor cuando actualizar y declarar cada cosa
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second

    while (1):

        # Hour update
        hour = datetime.now().hour

        # System only works between 6AM and 9PM
        if (HOUR_INF <= hour and hour > HOUR_SUP):

            # Minute and second update
            minute = datetime.now().minute
            second = datetime.now().second

            # Total seconds count
            total_sec = hour*SEC_HOUR + minute*SEC_MIN + second

            # No tengo clara esta condición (ver TO DO)
            if (datetime.now().day == day and datetime.now().month == month and ((total_sec-second) < (PASO_SEG+1))):

                second = total_sec
                flag_setpoint = 1
                flag_date = 0
                flag_hour = 0

            # Date change check (Need to change file in database)
            if (datetime.now().day != day or datetime.now().month != month):
                
                day = datetime.now().day
                month = datetime.now().month
                flag_date = 1 # Date change flag for other processes

            if ((total_sec-second) > (PASO_SEG+1)):
                second = total_sec
                flag_hour = 1

        else:
            print("Night mode: " + str(datetime.now()))

        # Valor de 5s heredado de código en C
        time.sleep(5)   
        

if __name__ == "__main__":

    time_process()