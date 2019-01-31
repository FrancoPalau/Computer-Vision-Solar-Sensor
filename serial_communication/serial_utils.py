import serial
import time
from utils.utils import get_mean, num_steps
import numpy as np

def create_serial_port():
    # Create port
    port = serial.Serial()
    # Configuration
    port.baudrate = 115200
    port.timeout = 2.0
    port.port = 'COM3'
    # Finally, open port
    port.open()
    return port


def create_step_query(num_steps, type):
     if type == "az":
         return ":SZ" + str(num_steps[1]) # le doy lo que se mueve azimuth, entonces le paso la distacia al eje Altitud
     elif type == "al":
         return ":SE" + str(num_steps[0])


def create_signal_query(signal):
    if signal == 0:
        return ":SA"
    elif signal == 1:
        return ":SP"


def write_query(port, query):
    query = query + '\r'
    port.write(query.encode())


def close_port(port):
    port.close()


if __name__ == "__main__":
    port = create_serial_port()
    time.sleep(3)
    write_query(port, create_signal_query(1))
    list_centers = [(-120, 80), (-121, 81), (-119, 79)]
    time.sleep(0.01) # 10 miliseconds
    write_query(port, create_step_query(num_steps(np.mean(list_centers, axis=0)), "az"))
    time.sleep(3)
    list_centers = [(-120, 80), (-121, 81), (-119, 79)]
    write_query(port, create_step_query(num_steps(np.mean(list_centers, axis=0)), "az"))
    time.sleep(2)
    write_query(port, create_signal_query(0))
    time.sleep(2)
    close_port(port)