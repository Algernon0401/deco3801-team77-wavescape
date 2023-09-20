## need to install pyserial
import threading
import serial
import time
import math
# configure the serial connections (the parameters differs on the device you are connecting to)


class ControlBoard:

    def __init__(self, port="COM5", baudrate=115200) -> None:
        self.port = port
        self.baudrate = baudrate
        # open the serial port
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        # dictionary to store the readings
        self.readings = {
            "A0": 0,
            "A1": 0,
            "A2": 0,
            "D3": 0,
            "D4": 0,
            "D5": 0,
        }
        # create a thread to read from the serial port
        self.thread = threading.Thread(target=self.read_from_port, args=(self))
        self.thread.start()

    def read_from_port(self) -> None:
        controls = self.ser.readline().decode('utf-8').split(";")[:-1] #this reads the serial port and splits the data into a list and removes the last element which is the newline character
        for control in controls:
            control = control.split(":")
            if control[0] != '':
                self.readings[control[0]] = int(control[1])
                        

        
    def get_val(self, pin: str) -> int:
        val = self.readings[pin]
        return math.floor(val/10)
    
    def close(self):
        self.ser.close()

if __name__ == "__main__":
    board = ControlBoard()
    while True:
        try :
            # sleep for 1 second
            val = board.get_val("A0")
            for i in range(val):
                print("█", end="")
            print("")
        except KeyboardInterrupt:
            board.close()
            break
