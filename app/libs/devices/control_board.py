import serial
import time
from serial.serialutil import SerialException

class ControlBoard:
    """
    The control board that is connected to the computer via USB.
    The control board has support for 3 analog inputs and 3 digital inputs currently.
    """

    def __init__(self) -> None:
        self.ser = None # serial connection
        self.port = None # port to connect to
        # dictionary to store the readings
        self.readings = {
            "A0": 1023,
            "A1": 1023,
            "A2": 1023,
            "D3": 1023,
            "D4": 1023,
            "D5": 1023,
        }
    
    def connect(self, baudrate=115200) -> None:
        """
        Connects to the control board.
        """
        if self.port is not None:
            self.ser = serial.Serial(f"COM{i}", baudrate)
            line = self.ser.readline().decode('utf-8').split(";")[:-1]
            if len(line) == 6:
                print(f"Reconnected to COM{i}")
                return
            else:
                self.ser.close()
        for i in range(10):
            try:
                self.ser = serial.Serial(f"COM{i}", baudrate)
                line = self.ser.readline().decode('utf-8').split(";")[:-1]
                if len(line) == 6:
                    self.port = f"COM{i}"
                    print(f"Connected to COM{i}")
                else:
                    self.ser.close()
            except SerialException:
                continue

    def read_from_port(self) -> None:
        """
        Reads from the serial port and updates the readings dictionary.
        """
        if self.ser is None or not self.ser.isOpen() or self.port is None:
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
