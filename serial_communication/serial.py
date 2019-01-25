import serial

def create_serial_port():
    # Create port
    port = serial.Serial()
    # Configuration
    port.baudrate = 9600
    port.timeout = 2.0
    port.port = 'COM3'
    # Finally, open port
    port.open()
    return port

def create_step_query(num_steps):
    pass

def create_singal_query(signal):
    pass

def write_query(port, query):
    query = query + "\r"
    port.write(query.encode())