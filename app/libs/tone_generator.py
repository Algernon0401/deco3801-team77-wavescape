"""Functions to convert object id and position into sounds."""

import math
import numpy as np
from sound import *
from object import Tag
import json

frequency_map = json.load(open("assets/frequency_map.json"))
MIN_FREQUENCY = frequency_map["C0"]
MAX_FREQUENCY = frequency_map["B8"]
MAX_RADIAN = 2

class ToneGenerator:
    """A generator of sound"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, tag:Tag, duration) -> Wave:
        """Generate a wave based on the position of a shape"""
        cx, cy = ctr_pos    # position of the center of zone
        ox, oy = obj_pos    # position of the object
        
        amplitude = math.sqrt((cx-ox)**2+(cy-oy)**2)    # amplitude = distance
        radian = np.arccos((cx-ox)/amplitude)           # radian = arccos(x), r = 1
        frequency = radian / MAX_RADIAN * MAX_FREQUENCY # bijecting radian to frequency evenly

        print(f"Amplitude: {amplitude}, Frequncy: {frequency}")
        match tag:
            case Tag.TRIANGLE:
                return Triangle(amplitude, frequency, duration)
            case Tag.SQUARE:
                return Square(amplitude, frequency, duration)
            case Tag.CIRCLE:
                return Sine(amplitude, frequency, duration)
            case Tag.STAR:
                return Sawtooth(amplitude, frequency, duration)
            case Tag.ARROW:
                return Pulse(amplitude, frequency, duration)
            case _:
                raise Exception(f"Wave Undefined with tag: {tag}")
    
def main():
    """for testing"""
    print("Test start")
    sound = Sound(22050, 8)
    wave = ToneGenerator.pos_to_wave((0,0),(1000,10000),Tag.SQUARE,1000)
    sound.play(wave)
    print("Played")

if __name__ == "__main__":
    main()

