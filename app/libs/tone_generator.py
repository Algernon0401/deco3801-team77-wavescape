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
VOLUME_SCALAR = 0.75                # think it as the volume knob
SHARP_VOLUME_SCALAR = 0.25                # for sharp sounds

class ToneGenerator:
    """A generator of sound"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, max_dist, tag:Tag) -> Wave:
        """Generate a wave based on the position of a shape"""
        cx, cy = ctr_pos    # position of the [c]enter of zone
        ox, oy = obj_pos    # position of the [o]bject
        print(cx, cy)
        print(ox, oy)
        
        distance = math.sqrt((cx-ox)**2+(cy-oy)**2)     # Euclidean distance
        radian = np.arccos(abs(ox-cx)/distance)            # radian = arccos(x), r = 1
        print("Angle:", radian*180/math.pi)
        # check quadrant
        if ox > cx and oy < cy:
            # q1
            add = 0
            print("Q1")
        elif ox < cx and oy < cy:
            # q2
            add = MAX_RADIAN / 4
            print("Q2")
        elif ox < cx and oy > cy:
            # q3
            add = MAX_RADIAN / 2
            print("Q3")
        else: # ox > cx and oy > cx
            # q4
            add = 3 * (MAX_RADIAN / 4)
            print("Q4")
        radian += add
        # radian = np.arctan2((cy, oy), (cx, ox))
        idx = None
        # print("Radian:", radian)
        # fix the frequency to nearest note
        idx = NUM_NODES - 1
        for i in range(NUM_NODES):
            if radian < (i+1)*MAX_RADIAN/NUM_NODES:
                idx = i
                break
        frequency = frequency_list[idx]                         # bijecting radian to each discrete frequency 
        amplitude = 2 ** (16 - 1) - 1 #distance * elc_list[idx] #* VOLUME_SCALAR    # amplitude = distance * elc
        volume = distance / max_dist # * elc_list[idx]
        # print(f"Amplitude: {amplitude}, Frequency: {frequency}")
        print(f"Created {tag}")
        match tag:
            case Tag.TRIANGLE.value:
                return Triangle(amplitude, frequency, volume)
            case Tag.SQUARE.value:
                return Square(amplitude*SHARP_VOLUME_SCALAR, frequency, volume)
            case Tag.CIRCLE.value:
                return Sine(amplitude, frequency, volume)
            case Tag.STAR.value:
                return Sawtooth(amplitude*SHARP_VOLUME_SCALAR, frequency, volume)
            case Tag.ARROW.value:
                return Pulse(amplitude*SHARP_VOLUME_SCALAR, frequency, volume)
            case _:
                # raise Exception(f"Wave Undefined with tag: {tag}")
                print(f"Wave Undefined with tag: {tag}")
                return None
            
    
def main():
    """for testing"""
    print("Test start")
    sound = Sound() #22050, 8)
    wave = ToneGenerator.pos_to_wave((0,0),(10,100), 1000,Tag.CIRCLE.value)
    # wave = Sawtooth(2000, 500, 1)
    sound.play(wave)
    time.sleep(1)
    print("Played")

if __name__ == "__main__":
    main()

