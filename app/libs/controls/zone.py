"""
    zone.py - contains zone controls and functions
"""
import pygame
from datetime import *
from random import randint
from mpmath import cot
import threading
import math
import numpy as np

from multiprocessing import Queue

# Import app controller, control base class, camera and sound class
from ..base import Control
from ..base import AppController
from ..devices.camera import *
from ..object import *
from ..sound import *
from ..tone_generator import ToneGenerator

ZTYPE_OBJ_WAVEGEN = 0 # Generate waves for an object
ZTYPE_OBJ_ARRANGEMENT = 1 # Generate a tune arrangement from objects

PLAYBACK_MARKER_TAG = Tag.ARROW.value # Object to indicate playback is checked in playback box.
PLAYBACK_COOLDOWN = 2 #seconds

ASSET_ZONE_BORDER = 'assets/images/zone_border_l.png'
ASSET_ZONE_BORDER_CORNER = 'assets/images/zone_border_c.png'

ASSET_STAR = 'assets/images/obj_star.png'
ASSET_SQUARE = 'assets/images/obj_square.png'
ASSET_CIRCLE = 'assets/images/obj_circle.png'
ASSET_TRIANGLE = 'assets/images/obj_triangle.png'

objimg_star = pygame.image.load(ASSET_STAR)
objimg_square = pygame.image.load(ASSET_SQUARE)
objimg_circle = pygame.image.load(ASSET_CIRCLE)
objimg_triangle = pygame.image.load(ASSET_TRIANGLE)

zone_border_l = pygame.image.load(ASSET_ZONE_BORDER)
zone_border_t = pygame.transform.rotate(zone_border_l, 90)
zone_border_corner_tl = pygame.image.load(ASSET_ZONE_BORDER_CORNER)
zone_border_corner_tr = pygame.transform.rotate(zone_border_corner_tl, -90)
zone_border_corner_br = pygame.transform.rotate(zone_border_corner_tr, -90)
zone_border_corner_bl = pygame.transform.rotate(zone_border_corner_br, -90)

HIGH_AMP = 4000

WAVE_SPAN = 80 # How long a wave is in pixels
WAVE_QUALITY = 4 # The quality of the wave (larger numbers are faster but less visually appealing)
WAVE_CYCLES = 2 # How many cycles of a wave is displayed

# Time taken to complete one cycle revolution
# = (1 / FREQ) * WAVE_TIME_FREQUENCY_RATIO
# e.g. if ratio is 2000, and freq is 1000, then time taken to play one cycle = 2s
WAVE_TIME_FREQUENCY_RATIO = 2000 

TYPE_NONE = -1
TYPE_SINE = 0
TYPE_SQUARE = 1
TYPE_SAWTOOTH = 2
TYPE_TRIANGLE = 3
TYPE_PULSE = 4

def sine_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the sine wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    return math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)

def square_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the square wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    factor = math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
    if factor < 0:
        factor = -1
    if factor > 0:
        factor = 1
    return factor

def pulse_factor(duty_cycle, d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the pulse wave factor for the given distance d and duty cycle.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    factor = math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
    if factor > (2 * duty_cycle - 1):
        factor = -1
    else:
        factor = 1
    return factor

def triangle_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the triangle wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    return math.sinh(math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle))

def sawtooth_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the sawtooth wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    return math.tanh(cot(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle))

def line_rotation(d, origin_x, origin_y, rot):
        """
        Gets the rotation for a line factor at distance d.
        
        Arguments:
            d -- the distance between 0 and distance to calculate the position for.
            origin_x -- the origin point x pos to rotate the wave around
            origin_y -- the origin point y pos to rotate the wave around
            rot -- the rotation to rotate the wave around
        """

        # Store cos and sin for computational efficiency
        rot_cos = math.cos(rot)
        rot_sin = math.sin(rot)

        # Perform 2D rotation around the origin
        return (
            origin_x + d * rot_cos,
            origin_y + d * rot_sin
        )

def wave_rotation(factor, d, dist, amp_dist, origin_x, origin_y, rot):
        """
        Gets the rotation for a wave factor at distance d.
        
        Arguments:
            d -- the distance between 0 and distance to calculate the position for.
            dist -- the full display distance of the wave.
            time -- the current time in seconds that the wave object has existed for.
            amp_dist -- the maximum amp height to display for this wave.
            dist_per_cycle -- the distance given by dist / (displayed frequency).
            time_per_cycle -- the time for one cycle to revolve
            origin_x -- the origin point x pos to rotate the wave around
            origin_y -- the origin point y pos to rotate the wave around
            rot -- the rotation to rotate the wave around
        """
        amp_percentage = 1 - abs(dist / 2 - d) / (dist / 2)
        
        # Store cos and sin for computational efficiency
        rot_cos = math.cos(rot)
        rot_sin = math.sin(rot)
        
        # Calculate the height (amplitude) of the wave at d (from center)
        y = factor * amp_percentage * amp_dist
        
        # Perform 2D rotation around the origin
        return (
            origin_x + d * rot_cos - y * rot_sin,
            origin_y + y * rot_cos + d * rot_sin
        )

class ObjectNode:
    """
        A node representing a object placed in the zone.
        
        Object distances between each other can be calculated via object.distance(x,y)
    """
    def __init__(self, object, center, connectedNodes):
        """
            Initialise a node with the given connections.
        """
        self.object = object
        self.center = center
        self.connections = connectedNodes
        self.completed = False
        self.wave_lines = []
        
    def destroy_children_in_list(self, list):
        """
        Destroys all objects used in this node/subtree in list.
        """
        if self.object in list:
            list.remove(self.object)
            
        for connection in self.connections:
            connection.destroy_children_in_list(list)

    def sound_type(self):
        """
        Gets the sound type of the object,
        returning

        0 = Sine
        1 = Square
        2 = Sawtooth
        3 = Triangle
        4 = Pulse
        """
        if self.object is None:
            return TYPE_NONE
        
        match self.object.tag:
            case Tag.TRIANGLE.value:
                return TYPE_TRIANGLE
            case Tag.SQUARE.value:
                return TYPE_SQUARE
            case Tag.CIRCLE.value:
                return TYPE_SINE
            case Tag.STAR.value:
                return TYPE_SAWTOOTH
            case Tag.ARROW.value:
                return TYPE_PULSE
            case _:
                return TYPE_NONE
    
    def prerender_update(self, controller):
        """
        An alternate update method using a different thread for expensive operations for
        the sole-purpose of generating drawing data.
        """
        for connection in self.connections:
             # At moment, visualisation produce the wave line of the object connected to.
            type_from = self.sound_type()
            type_to = connection.sound_type()
            
            # Get colours from ripples
            color_from = pygame.Color(255, 255, 255, 100)
            if self.object is not None:
                color_from = self.object.get_object_attribute("ripple_colour") 
                if color_from is None:
                    color_from = pygame.Color(255, 255, 255, 100)
                    
            color_to = color_from
            if connection.object is not None:
                color_to = connection.object.get_object_attribute("ripple_colour") 
                if color_to is None:
                    color_to = pygame.Color(255, 255, 255, 100)
                    
            (cx1, cy1) = self.center
            (cx2, cy2) = connection.center
            
            amplitude = 2000 # to be edited later
            
            dist = int(math.sqrt((cx2 - cx1) * (cx2 - cx1) + (cy2 - cy1) * (cy2 - cy1)))
            amp_dist = (dist / 4) * (amplitude / HIGH_AMP) 
            freq = 2400
            slope_rot = math.atan2(cy2 - cy1, cx2 - cx1)
            points = []
            add_point = points.append
            
            time = 0
            
            if connection.object is not None:
                time = connection.object.get_time_since_creation()

             
            dist_per_cycle = WAVE_SPAN / WAVE_CYCLES
            time_per_cycle = (1 / freq) * WAVE_TIME_FREQUENCY_RATIO
            wave_span = WAVE_SPAN
            if wave_span > dist:
               wave_span = dist
            #t = datetime.datetime.now()
            
            # Generate wave points from wave rotation and factor
            if type_to == TYPE_SINE:
                add_point((self.center, color_from))
                wave_start = line_rotation(dist / 2 - wave_span/2, cx1, cy1, slope_rot)
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point((
                        wave_rotation(
                             sine_factor(d, time, dist_per_cycle, time_per_cycle),
                             d, wave_span, amp_dist, wsx, wsy, slope_rot
                             ), # get position of sine wave at distance.
                        color_from.lerp(color_to, d / wave_span)   
                    ))
                
                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_SQUARE:
                add_point((self.center, color_from))
                wave_start = line_rotation(dist / 2 - wave_span/2, cx1, cy1, slope_rot)
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point((
                        wave_rotation(
                             square_factor(d, time, dist_per_cycle, time_per_cycle),
                             d, wave_span, amp_dist, wsx, wsy, slope_rot
                             ), # get position of sine wave at distance.
                        color_from.lerp(color_to, d / wave_span)   
                    ))
                
                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_PULSE:
                duty_cycle = 0.125
                add_point((self.center, color_from))
                wave_start = line_rotation(dist / 2 - wave_span/2, cx1, cy1, slope_rot)
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point((
                        wave_rotation(
                             pulse_factor(duty_cycle,d, time, dist_per_cycle, time_per_cycle),
                             d, wave_span, amp_dist, wsx, wsy, slope_rot
                             ), # get position of sine wave at distance.
                        color_from.lerp(color_to, d / wave_span)   
                    ))
                
                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_TRIANGLE:
                add_point((self.center, color_from))
                wave_start = line_rotation(dist / 2 - wave_span/2, cx1, cy1, slope_rot)
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point((
                        wave_rotation(
                             triangle_factor(d, time, dist_per_cycle, time_per_cycle),
                             d, wave_span, amp_dist, wsx, wsy, slope_rot
                             ), # get position of sine wave at distance.
                        color_from.lerp(color_to, d / wave_span)   
                    ))
                
                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_SAWTOOTH:
                add_point((self.center, color_from))
                wave_start = line_rotation(dist / 2 - wave_span/2, cx1, cy1, slope_rot)
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point((
                        wave_rotation(
                             sawtooth_factor(d, time, dist_per_cycle, time_per_cycle),
                             d, wave_span, amp_dist, wsx, wsy, slope_rot
                             ), # get position of sine wave at distance.
                        color_from.lerp(color_to, d / wave_span)   
                    ))
                
                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            else:
                points = [(self.center, color_from)] # Single line
            
            points.append((connection.center, color_to))
            
            if len(points) == 0:
                pass
            
            connection.wave_lines = points # Update to new wave list.
            
            connection.prerender_update(controller)
            
        self.completed = True
            
    def render(self, controller, screen):
        """
        Renders the given tree/graph animations and elements onto the screen
        """
        self.prerender_update(controller)
        
        for connection in self.connections:
            # Render all lines in wave lines
            last_center = self.center
            wave_lines = connection.wave_lines    
            
            #pygame.draw.aalines(screen, pygame.Color(255,255,255,255), False, wave_lines)
            
            for line in wave_lines: 
                 (center, color) = line
                 pygame.draw.aaline(screen, color, last_center, center)
                 last_center = center
            
            connection.render(controller, screen)
        
class Zone(Control):
    """
        Represents a zone, which can be modified using particular
        user actions.
    """
    
    def __init__(self, controller: AppController):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.is_global = False
        self.is_zone = True
        self.w = 128
        self.h = 128 # Standard size
        self.tone_gen = ToneGenerator()
        # Allow for center definitions
        self.center_x = 0
        self.center_y = 0
        self.interactive = True
        self.object_attributes = {}
        self.graph = None
        self.current_objects = []
        self.sounds_active = True
        self.type = ZTYPE_OBJ_WAVEGEN
        self.wave_gen_tag = Tag.STAR.value # default value for wavegen zone
        self.scaled_x = 0 # Ratio 0-1 of screen
        self.scaled_y = 0
        self.scaled_w = 0
        self.scaled_h = 0
        self.addsize_w = 0
        self.addsize_h = 0
        self.offset_x = 0
        self.offset_y = 0
        self.sound_enabled = True # True if sound playback occurs
        self.time_since_playback_existed = datetime.datetime.now() 
        self.sound_thread = None
    
    def get_max_dist(self):
        return math.sqrt((self.w/2)**2 + (self.h/2)**2)
        
    def get_object_attributes(self, object):
        """
            Gets the zone-based attributes for a
            specific object.
        """
        if not object.tag in self.object_attributes:
            return {}
        return  self.object_attributes[object.tag]
    
    def get_object_attribute(self, object, attribute_name):
        """
            Gets a single zone-based attribute for a specific
            object 
        """
        attributes = self.get_object_attributes(object)
        if attribute_name in attributes:
            return attributes[attribute_name]
        return None
    
    def set_object_attribute(self, object, attribute_name, attribute_value):
        """
        Sets the given attribute on the object as a zone-based attribute.
        """
        if not object.tag in self.object_attributes:
            self.object_attributes[object.tag] = {}
        
        self.object_attributes[object.tag][attribute_name] = attribute_value
    
    def create_connectivity_tree(self, object, objects, center, base_center):
        """
            Creates a new connectivity tree from the given list of objects inside
            the zone.
        """
        return ObjectNode(object, center, [ObjectNode(o, o.get_center(), []) for o in objects])
        
        # Depreciated / obsolete workings below
        
        uncreated_objects = objects.copy()
        connections = [] # Connections for this node
        
        while len(uncreated_objects) > 0:
            
            if object is None:
                pass
            min_dist_obj = None
            min_dist = 99999
            
            # Start by selecting object with smallest distance to current center
            # Avoid base_center as much as possible (if object is not None)
            for i in range(len(uncreated_objects)):
                test_obj = uncreated_objects[i]
                dist = test_obj.distance(center)
                
                if dist < min_dist:
                    if object is not None:
                        # Test whether we should avoid creating a subtree from this object
                        # Currently not implemented, so objects will connect a single tree from
                        # closest to closest.
                        pass
                    min_dist = dist
                    min_dist_obj = test_obj

            if min_dist_obj is None:
                break
            
            if object is None:
                pass
            
            # We must form a new connectivity tree/subtree with this object.                
            uncreated_objects.remove(min_dist_obj)
            subtree = self.create_connectivity_tree(min_dist_obj, uncreated_objects, 
                                                     min_dist_obj.get_center(), base_center)
            subtree.destroy_children_in_list(uncreated_objects) # Remove created objects from list
            
            connections.append(subtree)
            
        return ObjectNode(object, center, connections) 
        
    def get_playback_box_bounds(self, controller: AppController):
        """
        Returns the bounds of a fixed playback checkbox,
        that is 30 in w/h. 
        """
        return (self.x - 40, self.y, 30, 30)
        
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        objects = None
        (w,h) = controller.get_screen_size()
        if self.is_global:
            self.x = 0
            self.y = 0
            self.w = w
            self.h = h 
            if not controller.use_global_zone:
                return
            objects = controller.get_cam_objects_in_global()
        else:
            # Adjust zone positions accordingly
            if self.scaled_w + self.scaled_h != 0:
                self.x = w * self.scaled_x + self.offset_x
                self.y = h * self.scaled_y + self.offset_y
                self.w = w * self.scaled_w + self.addsize_w
                self.h = h * self.scaled_h + self.addsize_h
            objects = controller.get_cam_objects_in_bounds(self.get_bounds())
            if self.type == ZTYPE_OBJ_WAVEGEN:
                if controller.has_object_in_bounds(PLAYBACK_MARKER_TAG, self.get_playback_box_bounds(controller)):
                    self.time_since_playback_existed = datetime.datetime.now()
                self.sound_enabled = (datetime.datetime.now() - self.time_since_playback_existed).total_seconds() < PLAYBACK_COOLDOWN
        
        if self.type == ZTYPE_OBJ_WAVEGEN:
            if self.sound_thread is None:
                self.sound_thread = threading.Thread(target=self.handle_sound, args=[controller])
                self.sound_thread.start()
        
        center = self.get_center()
        (self.center_x, self.center_y) = center
        
        
        # Remove corner objects (of type)
        
        actual_objects = []
        
        for object in objects:
            # Check to see if it is a zone-border object
            if object.tag == controller.zone_border_object:
                continue
            actual_objects.append(object)
        
        objects = actual_objects
        self.current_objects = actual_objects
        

        if self.type == ZTYPE_OBJ_WAVEGEN:
            # Object connectivity graph via distance, but only if the old graph was
            # completed or non-existing.
            self.graph = self.create_connectivity_tree(None, objects, center, center)
        
        for object in objects:
            if object.get_object_attribute("ripple_count") is None:
                object.set_object_attribute("ripple_count", randint(1, 5))
            if object.get_object_attribute("ripple_colour") is None:
                object.set_object_attribute("ripple_colour", pygame.Color(randint(1, 255), randint(1, 255), randint(1, 255), 100))

        if self.type == ZTYPE_OBJ_ARRANGEMENT:
            # You may implement your arrangement code here if you wish.
            pass

        return
        
    def play_sounds(self, controller, objects, sound_player):
        # Play sound for each object
        waves = []
        for obj in objects:
            can_play = True
            
            # Check whether we must play the sound
            last_played = obj.get_object_attribute("last_played")
            if last_played is not None:
                can_play = False
                if datetime.datetime.now() > last_played + timedelta(seconds=1):
                    can_play = True

            if can_play:
                # Check whether the object already has a wave
                obj_wave = obj.get_object_attribute("wave")
                if obj_wave is None:
                    # Create a wave object based on object type and relative position
                    obj_wave = self.tone_gen.pos_to_wave((self.center_x, self.center_y),
                                                        obj.get_center(), obj.tag, 1)
                if obj_wave is not None:
                    waves.append(obj_wave)

                obj.set_object_attribute("last_played", datetime.datetime.now())
                obj.set_object_attribute("wave", obj_wave)
                
        # Store waves list according to object tag
        controller.set_object_attribute(obj, "waves", waves)
        
        if len(waves) > 0:
            #print(f"Playing {len(waves)} waves...")
            #for wave in waves:
                #print(f"Wave: F:({wave.frequency})")
            controller.audio_system.play_waves(waves)


    def handle_sound(self, controller):
        sound_player = Sound()
        while self.sounds_active and controller.is_running():
            time.sleep(0.1)
            if not self.sound_enabled:
                continue
            # self.play_sounds(controller, self.current_objects, sound_player)
            waves = []
            for obj in self.current_objects:
                # Check whether the object already has a wave
                obj_wave = obj.get_object_attribute("wave")
                if obj_wave is None:
                    # Create a wave object based on object type and relative position
                    obj_wave = self.tone_gen.pos_to_wave((self.center_x, self.center_y),
                                                        obj.get_center(), self.get_max_dist(), obj.tag)
                waves.append(obj_wave)
                sound_player.play(obj_wave)
            sound_player.cleanup(waves)

    def prerender(self, controller: AppController):
        """
        Prepares data for rendering continuously.

        Arguments:
            controller -- the app controller this control runs from
        """
        # Draw animations between objects
        if self.graph is not None:
            self.graph.prerender(controller)
        
    def draw_border(self, screen: pygame.Surface, x, y, w, h):
        """
        Draws a zone box.
        Arguments:
                screen -- the surface this control is drawn on.
        """
        corner_width = zone_border_corner_tl.get_width()
        corner_height = zone_border_corner_tl.get_height()
        border_width = zone_border_l.get_width()
        
        # Draw corners
        screen.blit(zone_border_corner_tl, (x,y))
        screen.blit(zone_border_corner_tr, (x + w - corner_width, y))
        
        screen.blit(zone_border_corner_bl, (x, 
                                            y + h - corner_height))
        screen.blit(zone_border_corner_br, (x + w - zone_border_corner_tl.get_width(), 
                                            y + h - corner_height))
        
        # Draw spanning rectangle
        
        # Vertical lines
        screen.blit(pygame.transform.scale(zone_border_l, (border_width, h 
                                                           - corner_height * 2)),
                    (x, y + corner_height))
        
        screen.blit(pygame.transform.scale(zone_border_l, (border_width, h 
                                                           - corner_height * 2)),
                    (x + w - border_width, y + corner_height))
        
        # Horizontal lines
        screen.blit(pygame.transform.scale(zone_border_t, (w - corner_width * 2,  
                                                           border_width)),
                    (x + corner_width, y))
        
        screen.blit(pygame.transform.scale(zone_border_t, (w - corner_width * 2,
                                                           border_width)),
                    (x + corner_width, y + h - border_width))
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        self.draw_border(screen, self.x, self.y, self.w, self.h)
        
        if self.type == ZTYPE_OBJ_WAVEGEN:
            (px, py, pw, ph) = self.get_playback_box_bounds(controller)
            self.draw_border(screen, px, py, pw, ph)
        
            objimg = None
            if self.wave_gen_tag == Tag.STAR.value:
                objimg = objimg_star
            elif self.wave_gen_tag == Tag.SQUARE.value:
                objimg = objimg_square
            elif self.wave_gen_tag == Tag.TRIANGLE.value:
                objimg = objimg_triangle
            elif self.wave_gen_tag == Tag.CIRCLE.value:
                objimg = objimg_circle
                
            if objimg is not None:
                screen.blit(objimg, (px + pw / 2 - objimg.get_width() / 2, py + ph * 1.5 + 10 - objimg.get_height() / 2))
                screen.blit(objimg, (self.x + self.w / 2 - objimg.get_width() / 2, self.y + self.h / 2 - objimg.get_height() / 2))
        
        if self.is_global and not controller.use_global_zone:
            return # No effects as global zone not in use
        
        # Draw animations between objects
        if self.graph is not None:
            self.graph.render(controller, screen)
        
            
        for object in controller.get_cam_objects_in_bounds(self.get_bounds()):
            if object is None:
                continue
            self.generate_ripples(screen, object)

    def generate_ripples(self, screen: pygame.Surface, obj: CamObject):
        """
            Generates a ripple effect on the given object.
        """
        state = (math.sin(obj.get_time_since_creation()*5) + 1) * 30
        ripple_count = obj.get_object_attribute("ripple_count")
        if ripple_count is None:
            ripple_count = 3
        colour = obj.get_object_attribute("ripple_colour") 
        if colour is None:
            colour = pygame.Color(255, 255, 255, 100)
        
        for i in range(ripple_count):
            colour.a = (100 - (i * 20)) # Update alpha
            adj_state = state + (i * 10)
            rect = pygame.Rect(obj.get_center(), (0, 0)).inflate((adj_state * 2, adj_state * 2))
            surf = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.circle(surf, colour, (adj_state, adj_state), adj_state)
            screen.blit(surf, rect)
        

    def event(self, controller: AppController, event: pygame.event.Event):
        """
        Receives an event from the pygame interface.
            
        Arguments:
            controller -- the app controller this control runs from
            event -- the pygame event that happened
        """
        pass

    def destroy(self):
        """
        Destroys all resources of a zone
        """
        self.sounds_active = False # Dispose of extra threads
        
