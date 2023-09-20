"""Functions to convert object id and position into sounds."""

import math
import numpy as np
from .sound import *
from .object import Tag
import json

frequency_list = list(json.load(open("assets/frequency_list.json")))
elc_list = list(json.load(open("assets/elc_list.json")))
NUM_NODES = len(frequency_list)     # based on piano
MAX_RADIAN = 2 * math.pi
VOLUME_SCALAR = 0.095                # think it as the volume knob
SHARP_VOLUME_SCALAR = 0.25                # for sharp sounds

class ToneGenerator:
    """A generator of sound"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, tag:Tag, duration) -> Wave:
        """Generate a wave based on the position of a shape"""
        cx, cy = ctr_pos    # position of the [c]enter of zone
        ox, oy = obj_pos    # position of the [o]bject
        
        distance = math.sqrt((cx-ox)**2+(cy-oy)**2)     # Euclidean distance
        radian = np.arccos((cx-ox)/distance)            # radian = arccos(x), r = 1
        idx = None
        print("Radian:", radian)
        for i in range(NUM_NODES):
            if radian < (i+1)*MAX_RADIAN/NUM_NODES:
                idx = i
                break
        frequency = frequency_list[idx]                         # bijecting radian to each discrete frequency 
        amplitude = distance * elc_list[idx] * VOLUME_SCALAR    # amplitude = distance * elc

        print(f"Amplitude: {amplitude}, Frequency: {frequency}")
        match tag:
            case Tag.TRIANGLE.value:
                return Triangle(amplitude, frequency, duration)
            case Tag.SQUARE.value:
                return Square(amplitude*SHARP_VOLUME_SCALAR, frequency, duration)
            case Tag.CIRCLE.value:
                return Sine(amplitude, frequency, duration)
            case Tag.STAR.value:
                return Sawtooth(amplitude*SHARP_VOLUME_SCALAR, frequency, duration)
            case Tag.ARROW.value:
                return Pulse(amplitude*SHARP_VOLUME_SCALAR, frequency, duration)
            case _:
                # raise Exception(f"Wave Undefined with tag: {tag}")
                print(f"Wave Undefined with tag: {tag}")
                return None
    
def main():
    """for testing"""
    print("Test start")
    sound = Sound(22050, 8)
    wave = ToneGenerator.pos_to_wave((0,0),(1000,10000),Tag.SQUARE.value,1)
    # wave = Sawtooth(2000, 500, 1)
    sound.play(wave)
    print("Played")

if __name__ == "__main__":
    main()

