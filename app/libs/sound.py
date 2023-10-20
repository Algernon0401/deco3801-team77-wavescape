"""
    sound.py - hosts the classes and logic used to generate sound.
"""

import math
import time
import pygame
import numpy as np
from scipy import signal
import threading
import functools

DEFAULT_BIT_RATE = 16

class Wave:
    """Base class representing a sound wave."""

    def __init__(self, amplitude, frequency, volume):
        self.amplitude = amplitude
        self.frequency = frequency
        self.volume = volume
        self.buffering = False
        self.buffer = None
        # self.buffer = Sound.generate_buffer(Sine(100, 100, 0.5))
        # self.tsound = pygame.sndarray.make_sound(self.buffer)

    def generate(self, time):
        """Generates the amplitude of the wave at given time step. Template function only.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return 0

    def sign(self, x):
        """Get the sign of x"""
        if x == 0:
            return 1
        return x / abs(x)

    def __eq__(self, other):
        return (
            self.amplitude == other.amplitude
            and self.frequency == other.frequency
            and self.volume == other.volume
            and type(self) == type(other)
        )

    def __hash__(self):
        return hash((self.amplitude, self.frequency, self.volume, type(self)))


class Sine(Wave):
    """Represents a sine wave."""

    def __init__(self, amplitude, frequency, volume):
        super().__init__(amplitude, frequency, volume)

    def generate(self, time):
        """Generates the amplitude of a sine wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(
            round(self.amplitude * math.sin(2 * math.pi * self.frequency * time))
        )


class Square(Wave):
    """Represents a square wave."""

    def __init__(self, amplitude, frequency, volume):
        super().__init__(amplitude, frequency, volume)

    def generate(self, time):
        """Generates the amplitude of a square wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(
            round(
                self.amplitude
                * self.sign(math.sin(2 * math.pi * self.frequency * time))
            )
        )


class Triangle(Wave):
    """Represents a triangle wave."""

    def __init__(self, amplitude, frequency, volume):
        super().__init__(amplitude, frequency, volume)

    def generate(self, time):
        """Generates the amplitude of a triangle wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(
            round(
                self.amplitude
                * 2
                / math.pi
                * math.asin(math.sin(2 * math.pi * self.frequency * time))
            )
        )


class Sawtooth(Wave):
    """Represents a sawtooth wave."""

    def __init__(self, amplitude, frequency, volume):
        super().__init__(amplitude, frequency, volume)

    def generate(self, time):
        """Generates the amplitude of a sawtooth wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(
            round(
                self.amplitude
                * 2
                * (
                    math.pi * self.frequency * time
                    - math.floor(math.pi * self.frequency * time + 1 / 2)
                )
            )
        )


class Pulse(Wave):
    """Represents a pulse wave."""

    def __init__(self, amplitude, frequency, volume, duty_cycle=0.175):
        super().__init__(amplitude, frequency, volume)
        self.duty_cycle = duty_cycle

    def pulse_sign(self, time):
        """Helper function for generating a pulse wave.

        Args:
            time (float): current time step.

        Returns:
            int: sign of the wave at current time step.
        """
        return int(
            (
                math.pi * self.frequency * time
                - math.floor(math.pi * self.frequency * time)
            )
            < self.duty_cycle
        )

    def generate(self, time):
        """Generates the amplitude of a pulse wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(round(self.amplitude * self.pulse_sign(time)))


class Sound:
    """Class for playing sounds, with one or more waves"""

    def __init__(self, sample_rate=44100, bit_rate=DEFAULT_BIT_RATE, speaker="both"):
        """
        Args:
            sample_rate (int, optional): the audio sample rate. Defaults to 44100.
            bit_rate (int, optional): the audio bit rate. Defaults to 16.
            speaker (str, optional): the output channel - left, right or both. Defaults to "both".
        """
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.speaker = speaker
        self.playing = {}
        self.wave_cache = []

        self.LEFT = 0
        self.RIGHT = 1

        # init pygame
        pygame.mixer.init(self.sample_rate, self.bit_rate, 6, allowedchanges=0)
        self.max_channels = pygame.mixer.get_num_channels()

    def get_next_channel(self):
        """Get the next available channel. Increase number of channels if none available."""
        c = pygame.mixer.find_channel()
        if c is None:
            pygame.mixer.set_num_channels(self.max_channels * 2)
        return pygame.mixer.find_channel()

    def play(self, wave: Wave):
        """Takes a wave object and plays its corresponding sound.

        Args:
            wave (Wave): a wave object
        """
        if wave is None:
            return

        if wave in self.playing.values():
            return

        channel = self.get_next_channel()
        self.playing[channel] = wave

        if wave.buffer is None:
            return  # NOTE: Now using sound_controller's buffer generation
            # do not halt any other sounds

        pygame_sound = pygame.mixer.Sound(wave.buffer)
        pygame_sound.set_volume(wave.volume)
        channel.play(pygame_sound, loops=-1)
        channel.queue(pygame_sound)

    def cleanup(self, waves: list):
        """Stop playing all active Waves that are not in waves.

        Args:
            waves (list): waves to continue playing
        """
        cull_list = []
        for channel, wave in self.playing.items():
            if wave not in waves:
                channel.stop()
                cull_list.append(channel)
        for channel in cull_list:
            self.playing.pop(channel)

    @functools.cache
    def generate_buffer(self, wave: Wave):
        """Generate the audio buffer for the given Wave.

        Args:
            wave (Wave): wave to generate buffer for.

        Returns:
            np.float16: numpy array of generated buffer
        """

        time = np.linspace(0, 1, int(wave.frequency), endpoint=False)
        if isinstance(wave, Sine):
            return np.sin(
                2
                * np.pi
                * np.arange(self.sample_rate / wave.frequency)
                * wave.frequency
                / self.sample_rate
            ).astype(np.float16)
        elif isinstance(wave, Square):
            return (
                np.round(
                    (
                        np.sin(
                            2
                            * np.pi
                            * np.arange(self.sample_rate / wave.frequency)
                            * wave.frequency
                            / self.sample_rate
                        )
                        + 1
                    )
                    / 2
                )
                * 2
                - 1
            ).astype(np.float16)
        elif isinstance(wave, Sawtooth):
            return (signal.sawtooth(time) + 1).astype(np.float16)
        elif isinstance(wave, Triangle):
            return (signal.sawtooth(time, width=0.5) + 1).astype(np.float16)
        return None