"""
    sound_controller.py - hosts SoundController.
"""

import threading
from ..base import *
from ..controls.zone import *

class SoundController(Controller):
    """
    This represents a controller (excluding AppController) for the logic
    of sound generation and playback.
    """

    def __init__(self, controller: AppController):
        """
        Initializes the controller

        Arguments:
            controller -- the app controller this controller runs from
        """
        
        # Create all possible waves that might ever need a buffer for.
        self.unbuffered_waves = [
            
        ]
        
        # Store list of immediate waves that must be created as soon as possible.
        self.immediate_waves = []
        self.immediate_wave_lock = threading.Lock()
        
        self.buffer_dict = {}
        
        self.buffering_thread = threading.Thread(target=self.buffer_generation, args=[controller])
        self.buffering_thread.start()
        pass
    
    def buffer_generation(self, controller: AppController):
        """
        Continuously creates buffers for the main thread
        """
        print("SoundBuffer thread active")
        while controller.is_running():
            next_wave = None
            if len(self.immediate_waves) > 0:
                self.immediate_wave_lock.acquire(blocking=True)
                next_wave = self.immediate_waves.pop()
                self.immediate_wave_lock.release()
            elif len(self.unbuffered_waves) > 0:
                next_wave = self.unbuffered_waves.pop()
            
            if next_wave is not None:
                try:
                    buffer = controller.sound_player.generate_buffer(next_wave)
                    arr = buffer.tolist()
                    self.buffer_dict[next_wave] = buffer
                    next_wave.buffering = False
                    self.unbuffered_waves.remove(next_wave)
                except:
                    pass
                
        print("SoundBuffer thread exited")
                
            
    
    def update(self, controller: AppController):
        """
        Updates the controller on every loop iteration.

        Arguments:
            controller -- the app controller this controller runs from
        """
        # self.play_sounds(controller, self.current_objects, controller.sound_player)
        waves = []
        for zone in controller.zones:
            if zone.type == ZTYPE_OBJ_WAVEGEN and zone.sound_enabled:
                for obj in zone.current_objects:
                    # Check whether the object already has a wave
                    obj_wave = obj.get_object_attribute("wave")
                    if obj_wave is None or zone.invalidate_waves:
                        # Create a wave object based on object type and relative position
                        obj_wave = zone.tone_gen.pos_to_wave(
                            (zone.center_x, zone.center_y),
                            obj.get_center(),
                            zone.get_max_dist(),
                            obj.tag,
                            zone.chord
                        )
                        
                        obj.set_object_attribute("wave", obj_wave)
                    if obj_wave is not None:
                        waves.append(obj_wave)
                        if obj_wave.buffer is None or zone.invalidate_waves:
                            try:
                                obj_wave.buffer = self.buffer_dict.get(obj_wave)
                                if obj_wave.buffer is None and not obj_wave.buffering:
                                    # Enqueue wave for immediate buffer generation
                                    if self.immediate_wave_lock.acquire(blocking=True, timeout=0.05):
                                        self.immediate_waves.append(obj_wave)
                                        obj_wave.buffering = True
                                        self.immediate_wave_lock.release()
                            except:
                                pass
                            
                        if obj_wave.buffer is not None:
                            controller.sound_player.play(obj_wave)
                            
                # Make sure waves are kept in cache until invalidated again
                if zone.invalidate_waves:
                    zone.invalidate_waves = False
        controller.sound_player.cleanup(waves)

 
    def event(self, controller: AppController, event: pygame.event.Event):
        """
        Receives an event from the pygame interface.

        Arguments:
            controller -- the app controller this controller runs from
            event -- the pygame event that happened
        """
        pass
    