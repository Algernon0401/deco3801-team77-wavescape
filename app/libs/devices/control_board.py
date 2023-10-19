import serial
from serial import Serial
import time
from serial.tools import list_ports

POT_PIN = "A0"
BUTTON_PIN = "D13"


class ControlBoard:
    """
    The control board that is connected to the computer via USB.
    The control board has support for 3 analog inputs and 3 digital inputs currently.
    """

    def __init__(self, baudrate=115200) -> None:
        self.ser = None  # serial connection
        self.baudrate = baudrate
        # dictionary to store the readings
        self.readings = {
            POT_PIN: 1023,
            BUTTON_PIN: 0,
        }
        self.overide = 0
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
            if (
                "Arduino" in port.description
                or port.pid == 67
                or port.serial_number == "75630313936351803252"
            ):
                # Connect
                self.ser = Serial(port.device, self.baudrate)
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
        line = self.ser.readline().decode("utf-8").split(";")[:-1]
        for entry in line:
            entry = entry.split(":")
            if len(entry) == 2 and entry[0] != "" and entry[0] in self.readings:
                self.readings[entry[0]] = int(entry[1])

    def get_volume(self) -> int:
        """
        Returns the reading of the potentiometer.
        """
        self.read_from_port()
        return self.readings[POT_PIN] / 1023

    def get_button(self) -> int:
        """
        Returns the reading of the button.
        """
        if self.overide > 0:
            self.overide -= 1
            return 1
        self.read_from_port()
        return self.readings[BUTTON_PIN]

    def press_button(self):
        """
        Sets the reading of the button to 1.
        """
        self.overide = 2

        return self.readings[BUTTON_PIN]

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
            readings = board.get_readings()
            print("                                 ", end="\r")
            print(f"A0: {readings[POT_PIN]}, D13: {readings[BUTTON_PIN]}", end="\r")
            time.sleep(0.1)
        except KeyboardInterrupt:
            board.close()
            break
