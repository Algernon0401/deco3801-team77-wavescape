"""Functions to convert object id and position into sounds."""

import math
import numpy as np
from .sound import *
from .object import Tag
import json

frequency_list = list(json.load(open("assets/frequency_list.json")))
elc_list = list(json.load(open("assets/elc_list.json")))
NUM_NODES = len(frequency_list)     # based on piano
MAX_ANGLE = 360
VOLUME_SCALAR = 0.75                # think it as the volume knob
SHARP_VOLUME_SCALAR = 1# 0.25                # for sharp sounds

class ToneGenerator:
    """A generator of sound"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, max_dist, tag:Tag) -> Wave:
        """Generate a wave based on the position of a shape"""
        cx, cy = ctr_pos    # position of the [c]enter of zone
        ox, oy = obj_pos    # position of the [o]bject
        # print(cx, cy)
        # print(ox, oy)
        
        distance = math.sqrt((cx-ox)**2+(cy-oy)**2)     # Euclidean distance
        angle = (math.atan2((cy-oy),(cx-ox)) * 180 / math.pi) + 180
        # print("Angle:", angle)

        # Slice lists
        start_pct, end_pct = 0.5, 0.8
        short_f_list, f_nodes = shorten_lookup(frequency_list, start_pct, end_pct)
        short_elc_list, _ = shorten_lookup(elc_list, start_pct, end_pct)

        num_nodes = f_nodes # NUM_NODES
        idx = None
        # fix the frequency to nearest note
        idx = num_nodes - 1
        for i in range(num_nodes):
            if angle < (i+1) * MAX_ANGLE / num_nodes:
                idx = i
                break

        # bijecting radian to each discrete frequency 
        frequency = short_f_list[idx]
        amplitude = 2 ** (16 - 1) - 1 #distance * elc_list[idx] #* VOLUME_SCALAR    # amplitude = distance * elc
        elc_scalar = short_elc_list[idx] / max(short_elc_list)
        print("ELC scalar:", elc_scalar)
        print("Dist scalar:", distance / max_dist)
        volume = distance / max_dist * elc_scalar
        print("Volume:", volume)
        # print(f"Amplitude: {amplitude}, Frequency: {frequency}")
        # print(f"Created {tag}")
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
            
def shorten_lookup(lookup: list, start_pct: int, end_pct: int):
    start_idx = math.floor(len(lookup) * start_pct)
    end_idx = math.ceil(len(lookup) * end_pct)
    shortened = lookup[start_idx:end_idx]
    return shortened, len(shortened)
            
    
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

