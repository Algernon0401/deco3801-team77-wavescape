"""
    tone_generator.py - Functions to convert object id and position into sounds.
"""

import math
import numpy as np
from .sound import *
from .object import Tag
import json

frequency_map = json.load(open("assets/frequency_map.json"))
elc_map = json.load(open("assets/elc_map.json"))
frequency_list = list(json.load(open("assets/frequency_list.json")))
elc_list = list(json.load(open("assets/elc_list.json")))
NUM_NODES = len(frequency_list)  # based on piano
MAX_ANGLE = 360
SHARP_VOLUME_SCALAR = 0.65  # for sharp sounds
MAX_ELC = max(elc_map.values())
CHORD_STEPS = {
    "major": [4, 3],
    "minor": [3, 4],
    "diminished": [3, 3],
    "7th": [4, 3, 3],
    "major 7th": [4, 3, 4],
    "minor 7th": [3, 4, 3],
}

CHORDS = ["major", "major 7th", "minor", "minor 7th"]

pitch_list = []
octave_list = []
for note in frequency_map.keys():
    if note == "CONTRIBUTION":
        continue
    octave = note[-1]
    if octave not in octave_list:
        octave_list.append(octave)
    note_name = note[: len(note) - 1]
    if note_name not in pitch_list:
        pitch_list.append(note_name)


class ToneGenerator:
    """A generator of sound"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def pos_to_wave(ctr_pos, obj_pos, max_dist, tag: Tag, chord="minor 7th") -> Wave:
        """Generate a wave based on the position of a shape

        Args:
            ctr_pos (tuple): centre of the zone
            obj_pos (tuple): centre of the object
            max_dist (int): radius of the zone
            tag (Tag): object type

        Returns:
                Wave: new wave
        """
        cx, cy = ctr_pos  # position of the [c]enter of zone
        ox, oy = obj_pos  # position of the [o]bject

        # Euclidean distance
        distance = math.sqrt((cx - ox) ** 2 + (cy - oy) ** 2)
        # angle from right horizontal, going ccw (i.e. unit circle)
        angle = (math.atan2((cy - oy), (cx - ox)) * 180 / math.pi) + 180

        # Slice lists
        start_pct, end_pct = 0.4, 0.65

        short_o_list, o_nodes = shorten_lookup(octave_list, start_pct, end_pct)
        short_p_list = get_chord_notes(pitch_list, root_note="C", chord=chord)
        p_nodes = len(short_p_list)

        num_nodes = p_nodes
        idx = None
        # fix the pitch to nearest
        idx = num_nodes - 1
        for i in range(num_nodes):
            if angle < (i + 1) * MAX_ANGLE / num_nodes:
                idx = i
                break
        p = short_p_list[idx]

        num_nodes = o_nodes
        idx = None
        # fix the octave to nearest
        idx = num_nodes - 1
        for i in range(num_nodes):
            if distance < (i + 1) * max_dist / num_nodes:
                idx = i
                break

        o = short_o_list[idx]
        note = p + o

        # bijecting radian to each discrete frequency
        frequency = frequency_map[note]
        amplitude = (
            2 ** (DEFAULT_BIT_RATE - 1) - 1
        ) # DEFAULT_BIT_RATE is 16
        elc_scalar = elc_map[note]
        volume = 1 * elc_scalar

        match tag:
            case Tag.TRIANGLE.value:
                return Triangle(amplitude, frequency, volume)
            case Tag.SQUARE.value:
                return Square(amplitude, frequency, volume * SHARP_VOLUME_SCALAR)
            case Tag.CIRCLE.value:
                return Sine(amplitude, frequency, volume)
            case Tag.STAR.value:
                return Sawtooth(amplitude, frequency, volume * SHARP_VOLUME_SCALAR)
            case Tag.ARROW.value:
                return Pulse(amplitude, frequency, volume)
            case _:
                print(f"Wave Undefined with tag: {tag}")
                return None


def shorten_lookup(lookup: list, start_pct: int, end_pct: int):
    """Create a subset of a lookup.

    Args:
        lookup (list): original lookup
        start_pct (int): start (percentage through lookup)
        end_pct (int): end (percentage through lookup)

    Returns:
        list: shortened lookup
        int: length of shortened lookup
    """
    start_idx = math.floor(len(lookup) * start_pct)
    end_idx = math.ceil(len(lookup) * end_pct)
    shortened = lookup[start_idx:end_idx]
    return shortened, len(shortened)


def get_chord_notes(note_list, root_note="C", chord="major"):
    """Gets the notes that make up a chord.

    Args:
        note_list (_type_): list of all notes
        root_note (str, optional): root note of the chord. Defaults to "C".
        chord (str, optional): chord name. Defaults to "major".

    Returns:
        list: notes of the chord
    """
    ratio = CHORD_STEPS[chord]
    chord_notes = [root_note]
    for r in ratio:
        prev_note_idx = note_list.index(chord_notes[-1])
        chord_notes.append(note_list[prev_note_idx + r])
    return chord_notes