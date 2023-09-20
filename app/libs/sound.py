"""
    sound.py - hosts the classes and logic used to generate sound.  
    Note by SAM: moved here so that I could test sound generation.
                 Overwrite when needed, no tests added down the bottom  
"""
import math
import time
import pygame
import numpy as np
import threading

class Wave:
    """Base class representing a sound wave."""
    def __init__(self, amplitude, frequency, duration):
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration

    def generate(self, time):
        """Generates the amplitude of the wave at given time step. Template function only.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return 0
    
    def sign(self, x):
        if x == 0: return 1
        return x/abs(x)
    
    
class Sine(Wave):
    """Represents a sine wave."""
    def __init__(self, amplitude, frequency, duration):
        super().__init__(amplitude, frequency, duration)

    def generate(self, time):
        """Generates the amplitude of a sine wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(round(self.amplitude * math.sin(2 * math.pi * self.frequency * time)))
    

class Square(Wave):
    """Represents a square wave."""
    def __init__(self, amplitude, frequency, duration):
        super().__init__(amplitude, frequency, duration)

    def generate(self, time):
        """Generates the amplitude of a square wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(round(self.amplitude * self.sign(math.sin(2 * math.pi * self.frequency * time))))
    

class Triangle(Wave):
    """Represents a triangle wave."""
    def __init__(self, amplitude, frequency, duration):
        super().__init__(amplitude, frequency, duration)

    def generate(self, time):
        """Generates the amplitude of a triangle wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(round(self.amplitude * 2 / math.pi * math.asin(
                         math.sin(2 * math.pi * self.frequency * time))))


class Sawtooth(Wave):
    """Represents a sawtooth wave."""
    def __init__(self, amplitude, frequency, duration):
        super().__init__(amplitude, frequency, duration)

    def generate(self, time):
        """Generates the amplitude of a sawtooth wave at given time step.

        Args:
            time (float): current time step.

        Returns:
            int: generated amplitude
        """
        return int(round(self.amplitude * 2 * (math.pi * self.frequency * time -
                                               math.floor(math.pi * self.frequency * time + 1/2))))


class Pulse(Wave):
    """Represents a pulse wave."""
    def __init__(self, amplitude, frequency, duration, duty_cycle=0.175):
        super().__init__(amplitude, frequency, duration)
        self.duty_cycle = duty_cycle

    def pulse_sign(self, time):
        """Helper function for generating a pulse wave.

        Args:
            time (float): current time step.

        Returns:
            int: sign of the wave at current time step.
        """
        return int((math.pi * self.frequency * time - math.floor(math.pi * self.frequency * time)) < self.duty_cycle)

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
    def __init__(self, sample_rate=44100, bit_rate=16, speaker="both"):
        """
        Args:
            sample_rate (int, optional): the audio sample rate. Defaults to 44100.
            bit_rate (int, optional): the audio bit rate. Defaults to 16.
            speaker (str, optional): the output channel - left, right or both. Defaults to "both".
        """
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.speaker = speaker

        self.LEFT = 0
        self.RIGHT = 1

        # init pygame
        pygame.init()
        pygame.mixer.pre_init(self.sample_rate, self.bit_rate)

    def chorus(self, waves: list):
        """Takes a list of wave objects and plays their corresponding sounds.

        Args:
            waves (list): a list of wave objects
        """
        threads = []
        for wave in waves:
            wave_thread = threading.Thread(target=self.play, args=(wave,))
            threads.append(wave_thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def play(self, wave: Wave):
        """Takes a wave object and plays its corresponding sound.

        Args:
            wave (Wave): a wave object
        """
        num_samples = int(round(wave.duration * self.sample_rate))

        # setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
        buffer = np.zeros((num_samples, 2), dtype = np.int32)

        # figure out which of the below is the correct method (prob not necessary)
        # amplitude = 2 ** (self.bits - 1) - 1
        # self.bit_rate = math.log2(wave.amplitude + 1) + 1

        for s in range(num_samples):
            # print(f"Iteration: {s}/{num_samples} ({float('%.2g' % (s/num_samples*100))}%)", end="\r", flush=True)
            # time in seconds
            t = float(s) / self.sample_rate

            output = wave.generate(t)

            # Control which speaker to play the sound from
            if self.speaker == 'l':
                buffer[s][self.LEFT] = output # left
            elif self.speaker == 'r':
                buffer[s][self.RIGHT] = output # right
            else:
                buffer[s][0] = output # left
                buffer[s][1] = output # right
                
        sound = pygame.sndarray.make_sound(buffer)
        one_sec = 1000 # Milliseconds
        sound.play(loops = 1, maxtime=int(wave.duration * one_sec))
        time.sleep(wave.duration)

# s = Sound()

# waves = []
# freqs = [440, 480, 880]

# base_f = 75
# major_ratios = [4, 5, 6]
# minor_ratios = [10, 12, 15]
# dimin_ratios = [160, 192, 231]

# seventh_ratios = [20, 25, 30, 36]
# maj_seventh_ratios = [10, 12, 15, 18]
# min_seventh_ratios = [8, 10, 12, 15]

# for r in min_seventh_ratios:
#     w = Sine(4000, r*base_f, 1)
#     waves.append(w)
#     s.play(w)

# s.chorus(waves)