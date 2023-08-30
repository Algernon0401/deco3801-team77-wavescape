"""Functions to convert object id and position into sounds."""

import math
import numpy as np
from sound import *
from object import Shape

MIN_FREQUENCY = 0
MAX_FREQUENCY = 20000
MAX_RADIAN = 2

class ToneGenerator:
    """A generator of sound"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, shape:Shape, duration) -> Wave:
        """Generate a wave based on the position of a shape"""
        cx, cy = ctr_pos    # position of the center of zone
        ox, oy = obj_pos    # position of the object
        
        amplitude = math.sqrt((cx-ox)**2+(cy-oy)**2)    # amplitude = distance
        radian = np.arccos((cx-ox)/amplitude)           # radian = arccos(x), r = 1
        frequency = radian / MAX_RADIAN * MAX_FREQUENCY # bijecting radian to frequency evenly

        match shape:
            case Shape.TRIANGLE:
                return Triangle(amplitude, frequency, duration)
            case Shape.SQUARE:
                return Square(amplitude, frequency, duration)
            case Shape.CIRCLE:
                return Sine(amplitude, frequency, duration)
            case Shape.STAR:
                return Sawtooth(amplitude, frequency, duration)
            case Shape.ARROW:
                return Pulse(amplitude, frequency, duration)
            case _:
                raise Exception("Shape Undefined")
    
def main():
    """for testing"""
    print("Test start")
    sound = Sound(22050, 8)
    wave = ToneGenerator.pos_to_wave((0,0),(1,1),Shape.SQUARE,10)
    sound.play(wave)
    print("Played")

if __name__ == "__main__":
    main()

