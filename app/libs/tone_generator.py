"""Functions to convert object id and position into sounds."""

import math
import numpy as np
from sound import *
from object import Tag
import json

frequency_list = list(json.load(open("assets/frequency_list.json")))
elc_list = list(json.load(open("assets/elc_list.json")))
NUM_NODES = len(frequency_list)     # based on piano
MAX_RADIAN = 2 * math.pi
VOLUME_SCALER = 0.02                # think it as the volume knob

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
        amplitude = distance * elc_list[idx] * VOLUME_SCALER    # amplitude = distance * elc

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
    wave = ToneGenerator.pos_to_wave((0,0),(12000,1000),Tag.SQUARE,1000)
    sound.play(wave)
    print("Played")

if __name__ == "__main__":
    main()

