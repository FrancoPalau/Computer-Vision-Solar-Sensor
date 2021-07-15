#!/usr/bin/python
# coding=utf-8

# INPUTS: TIME
# OUTPUTS: FLAGS AND SECONDS COUNTED 

from numpy.lib.function_base import copy
from pruebas.msg import numsteps
from datetime import datetime
import time
import rospy

# PHICHAL CONSTANTS
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

#FLAGS AND TIME CONSTANTS

PASO_SEG = 5 # Que es esto??
SEG_INF = 21600 # Y esto?

HOUR_INF = 6
HOUR_SUP = 21

SEC_HOUR = 3600
SEC_MIN = 60

month = datetime.now().month
day = datetime.now().day
second = datetime.now().second


# Database path
PATH = "/home/pi/seguidorsolar_ws/src/pruebas/time_data/data/"

# Create publisher
pub_num_steps_open_loop = rospy.Publisher('num_steps_open_loop',numsteps)

# Set loop status parameter
rospy.set_param('close_loop_flag',False)

def calc_step(id):
    global setpoint_A, setpoint_B,position_A,position_B

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
        step = int((setpoint - position) * reduction / STEP)
        if(step != 0):
            position_A=setpoint_A
        print("A-------")
        print(setpoint)
        print(position)
        print(step)
    elif (id == 'B'):
        reduction = REDUCTION_B
        setpoint = setpoint_B
        position = position_B
        step = int((setpoint - position) * reduction / STEP)
        if(step != 0):
            position_B=setpoint_B
        print("B--------")
        print(setpoint)
        print(position)
        print(step)
    return step


def time_process():
    
    rospy.init_node('open_loop', anonymous=True)

    flag_hour = 0
    flag_date = 1
    flag_setpoint = 0

    # Date and hour update in the creation of the process
    # Ver mejor cuando actualizar y declarar cada cosa
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second

    while not rospy.is_shutdown():

        loop_status = rospy.get_param("/close_loop_flag")

        if(not loop_status):
            num_steps_open_loop = numsteps()
            # Hour update
            hour = datetime.now().hour

            # System only works between 6AM and 9PM
            if (HOUR_INF <= hour and hour < HOUR_SUP):
            

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
                
                steps_A,steps_B = data_process(flag_date,flag_hour,flag_setpoint,second)
                num_steps_open_loop.al = steps_A
                num_steps_open_loop.az = steps_B

            else:
                print("Night mode: " + str(datetime.now()))
                num_steps_open_loop.al = 0
                num_steps_open_loop.az = 0
            
            pub_num_steps_open_loop.publish(num_steps_open_loop)
            rospy.sleep(5.0)
        else:
            rospy.loginfo("Entering close loop")
            num_steps_open_loop = numsteps()
            num_steps_open_loop.al = 0
            num_steps_open_loop.az = 0
            pub_num_steps_open_loop.publish(num_steps_open_loop)
            rospy.sleep(5.0)
        

def data_process(flag_date,flag_hour,flag_setpoint,second):
    global setpoint_A, setpoint_B

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
        # print(setpoint_A, setpoint_B)

        # Number of steps to take based on the setpoint and the current position
        steps_A = calc_step('A')
        steps_B = calc_step('B')

        # print(steps_A, steps_B)

        flag_hour = 0

    if (flag_setpoint):
        # Obtain azimuth and elevation coordinates
        setpoint_A, setpoint_B = get_coord(file_name, lines_count)

        # Number of steps to take based on the setpoint and the current position
        steps_A = calc_step('A')
        steps_B = calc_step('B')
        flag_setpoint = 0

    

    return steps_A,steps_B


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
    time_process()
