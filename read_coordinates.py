import serial
import serial.tools.list_ports as list_ports
from time import time
from matplotlib import pyplot as plt

def get_serial_port() -> str:
    """
    This function lists all the serial ports available and asks for a port to chose and return that port as string
    """
    ports = sorted(list_ports.comports())
    i = 1
    for port, desc, _ in ports:
        print("{}. {}: {}".format(i, port, desc))
        i += 1
    
    # Read input from user
    option = int(input("Select serial port: "))
    if (option < 1) or (option > len(ports)):
        raise ValueError(f"Invalid option {option}")

    port_option = ports[option - 1][0]
    return port_option

def read_coordinates(serial_port: str | serial.Serial = "COM51", baudrate: int = 115200, timeout: int = -1) -> list:
    """
    Function to read the coordinates from PSoC4 UART.

    params:

    serial_port: str
        USB port of the PSoC4 UART
    
    baudrate: int
        Baudrate of the UART communication

    read_time: int
        Read the data for "read_time" number of seconds.
    """
    if timeout == -1:
        timeout = None

    start_time = time()
    if (type(serial_port) == str):
        kitprog_comport = serial.Serial(port = serial_port, baudrate=baudrate, timeout = timeout)
    else:
        kitprog_comport = serial_port
    coordinates = []
    data = kitprog_comport.readline()
    while data != b"-1\r\n":
        if data == b"":
            break
        else:
            x, y = data.decode("utf-8").split(", ")
            x = int(x)
            y = int(y)
            coordinates.append([x, y])
            data = kitprog_comport.readline()

    if (timeout != None) and ((time() - start_time) < timeout):
        coordinates_new = read_coordinates(serial_port=kitprog_comport, timeout = (time() - start_time))
        return coordinates + coordinates_new

    return coordinates


def plot_coordinates(coordinates: list) -> None:
    x_coords = [coordinates[i][0] for i in range(len(coordinates))]
    y_coords = [coordinates[i][1] for i in range(len(coordinates))]
    plt.plot(x_coords, y_coords)
    plt.show()


def print_coordinates(coordinates: list) -> None:
    print("[", end = "")
    for i in range(len(coordinates)):
        print(f"({coordinates[i][0]}, {coordinates[i][1]}), ", end = "")
    print("]")
