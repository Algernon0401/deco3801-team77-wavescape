import serial
import time
from serial.tools import list_ports

class ControlBoard:
    """
    The control board that is connected to the computer via USB.
    The control board has support for 3 analog inputs and 3 digital inputs currently.
    """

    def __init__(self, baudrate = 115200) -> None:
        self.ser = None # serial connection
        self.baudrate = baudrate
        # dictionary to store the readings
        self.readings = {
            "A0": 1023,
            "A1": 1023,
            "A2": 1023,
            "D3": 1023,
            "D4": 1023,
            "D5": 1023,
        }
        self.connect()
    
    def connect(self) -> bool:
        """
        Connects or reconnects to the control board.
        """
        if self.ser is not None:
            # already connected
            if self.ser.isOpen():
                return True
            else:
                self.ser.close()
        
        # find the port
        ports = list_ports.comports()
        for port in ports:
            if "Arduino" in port.description:
                # Connect
                self.ser = serial.Serial(port.device, self.baudrate)
                return True
            
        return False
    
    def is_connected(self) -> bool:
        """
        Returns whether the control board is connected or not.
        """
        if self.ser is None:
            return False
        return self.ser.isOpen()

    def read_from_port(self) -> None:
        """
        Reads from the serial port and updates the readings dictionary.
        """
        if self.ser is None or not self.ser.isOpen():
            return
        self.ser.flushInput()
        line = self.ser.readline().decode('utf-8').split(";")[:-1]
        for entry in line:
            entry = entry.split(":")
            if len(entry) == 2 and entry[0] != '' and entry[0] in self.readings:
                self.readings[entry[0]] = int(entry[1])
    
    def get_reading(self, pin: str) -> int:
        """
        Returns the value of the pin.
        """
        self.read_from_port()
        return self.readings[pin]
    
    def get_readings(self) -> dict:
        """
        Returns the values of all the pins.
        """
        self.read_from_port()
        return self.readings
    
    def close(self):
        """
        Closes the serial connection to the control board
        """
        self.ser.close()
        print("Serial connection closed")

# Test code
if __name__ == "__main__":
    board = ControlBoard()
    board.connect()
    while True:
        try:
            val = board.get_reading("A0")
            print("                      ", end = "\r")
            print(f"A0: {val}", end = "\r")
            time.sleep(0.1)
        except KeyboardInterrupt:
            board.close()
            break
