"""
    sound.py - hosts the classes and logic used to generate sound.  
"""
import math
import pygame
import numpy as np

class Wave:
    def __init__(self, amplitude, frequency, duration):
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration

    def sine(self, time):
        return int(round(self.amplitude * math.sin(2 * math.pi * self.frequency * time)))