"""
    ddcam.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame
from datetime import *
from random import randint
from mpmath import cot
import threading
import math

# Import app controller, control base class, camera and sound class
from ..base import Control
from ..base import AppController
from ..devices.camera import *
from ..object import *
from ..sound import *
from ..tone_generator import ToneGenerator

ASSET_ZONE_BORDER = 'assets/images/zone_border_l.png'
ASSET_ZONE_BORDER_CORNER = 'assets/images/zone_border_c.png'

zone_border_l = pygame.image.load(ASSET_ZONE_BORDER)
zone_border_t = pygame.transform.rotate(zone_border_l, 90)
zone_border_corner_tl = pygame.image.load(ASSET_ZONE_BORDER_CORNER)
zone_border_corner_tr = pygame.transform.rotate(zone_border_corner_tl, -90)
zone_border_corner_br = pygame.transform.rotate(zone_border_corner_tr, -90)
zone_border_corner_bl = pygame.transform.rotate(zone_border_corner_br, -90)

HIGH_AMP = 4000
TYPE_NONE = -1
TYPE_SINE = 0
TYPE_SQUARE = 1
TYPE_SAWTOOTH = 2
TYPE_TRIANGLE = 3
TYPE_PULSE = 4

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

    def render(self, controller, screen):
        """
        Renders the given tree/graph animations and elements onto the screen
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

            # Create point list
            points = [(self.center, color_from)]

            time = 0
            
            if connection.object is not None:
                time = connection.object.get_time_since_creation()

            cycles = freq / 500
            dist_per_cycle = dist / cycles
            time_per_cycle = freq / 5000
            point_color = color_from
            type_to = TYPE_TRIANGLE
            if type_to == TYPE_SINE:
                for d in range(dist):
                    # create point that is not translated from start.
                    px = d 
                    perc = 1 - abs(dist / 2 - d) / (dist / 2)
                    factor = math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
                    py = factor * amp_dist * perc
                    point_color = color_from.lerp(color_to, d / dist)
                    # rotate point around origin (sx, sy)
                    points.append(
                        (
                            (cx1 + px * math.cos(slope_rot) - py * math.sin(slope_rot),
                            cy1 + py * math.cos(slope_rot) + px * math.sin(slope_rot)),
                            point_color
                        )
                    )
            elif type_to == TYPE_SQUARE:
                for d in range(dist):
                    # create point that is not translated from start.
                    px = d 
                    perc = 1 - abs(dist / 2 - d) / (dist / 2)
                    factor = math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
                    if factor < 0:
                        factor = -1
                    else:
                        factor = 1
                    py = factor * amp_dist * perc
                    point_color = color_from.lerp(color_to, d / dist)
                    # rotate point around origin (sx, sy)
                    points.append(
                        (
                            (cx1 + px * math.cos(slope_rot) - py * math.sin(slope_rot),
                            cy1 + py * math.cos(slope_rot) + px * math.sin(slope_rot)),
                            point_color
                        )
                    )         
            elif type_to == TYPE_PULSE:
                duty_cycle = 0.125
                for d in range(dist):
                    # create point that is not translated from start.
                    px = d 
                    perc = 1 - abs(dist / 2 - d) / (dist / 2)
                    factor = math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
                    if factor > (2 * duty_cycle - 1):
                        factor = -1
                    else:
                        factor = 1
                    py = factor * amp_dist * perc
                    point_color = color_from.lerp(color_to, d / dist)
                    # rotate point around origin (sx, sy)
                    points.append(
                        (
                            (cx1 + px * math.cos(slope_rot) - py * math.sin(slope_rot),
                            cy1 + py * math.cos(slope_rot) + px * math.sin(slope_rot)),
                            point_color
                        )
                    )        
            elif type_to == TYPE_TRIANGLE:
                duty_cycle = 0.125
                for d in range(dist):
                    # create point that is not translated from start.
                    px = d 
                    perc = 1 - abs(dist / 2 - d) / (dist / 2)
                    factor = math.sinh(math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle))
                    py = factor * amp_dist * perc
                    point_color = color_from.lerp(color_to, d / dist)
                    # rotate point around origin (sx, sy)
                    points.append(
                        (
                            (cx1 + px * math.cos(slope_rot) - py * math.sin(slope_rot),
                            cy1 + py * math.cos(slope_rot) + px * math.sin(slope_rot)),
                            point_color
                        )
                    )    
            elif type_to == TYPE_SAWTOOTH:
                duty_cycle = 0.125
                for d in range(dist):
                    # create point that is not translated from start.
                    px = d 
                    perc = 1 - abs(dist / 2 - d) / (dist / 2)
                    factor = math.tanh(cot(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle))
                    py = factor * amp_dist * perc
                    point_color = color_from.lerp(color_to, d / dist)
                    # rotate point around origin (sx, sy)
                    points.append(
                        (
                            (cx1 + px * math.cos(slope_rot) - py * math.sin(slope_rot),
                            cy1 + py * math.cos(slope_rot) + px * math.sin(slope_rot)),
                            point_color
                        )
                    )       
            
            points.append((connection.center, color_to))

            lpx = cx1
            lpy = cy1
            for i in range(1, len(points)):
                (center, color) = points[i]
                (px,py) = center
                pygame.draw.line(screen, color, (lpx, lpy), (px, py))
                lpx = px
                lpy = py
            
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
        self.w = 128
        self.h = 128 # Standard size
        # Allow for center definitions (zone stabilisation)
        self.center_x = 0
        self.center_y = 0
        self.interactive = True
        self.audio_system = Sound()
        self.tone_gen = ToneGenerator()
        self.object_attributes = {}
        self.graph = None
        self.current_objects = []
        self.sounds_active = True
        sound_thread = threading.Thread(target=self.handle_sound)
        sound_thread.start()
        
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
        
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        center = self.get_center()
        (self.center_x, self.center_y) = center
        objects = controller.get_cam_objects_in_bounds(self.get_bounds())
        
        # Remove corner objects (of type)
        
        actual_objects = []
        
        for object in objects:
            # Check to see if it is a zone-border object
            if object.tag == controller.zone_border_object:
                continue
            actual_objects.append(object)
        
        objects = actual_objects
        self.current_objects = actual_objects
        
        # Object connectivity graph via distance.
        graph = self.create_connectivity_tree(None, objects, center, center)
        self.graph = graph

        # NOTE from Sam to Luke:
        # in game development, there are often lag between one frame to the next.
        # To account for this, time passed is used so that animation is not slowed
        # down with program. With python, it is especially noticeable when it slows
        # down (as by no means python is a fast language due to being dynamically
        # interpreted)
        # 
        # time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        # ...do logic...
        # self.last_time_updated = datetime.datetime.now()
        
        for object in objects:
            if object.get_object_attribute("ripple_count") is None:
                object.set_object_attribute("ripple_count", randint(1, 5))
            if object.get_object_attribute("ripple_colour") is None:
                object.set_object_attribute("ripple_colour", pygame.Color(randint(1, 255), randint(1, 255), randint(1, 255), 100))

        return
        
    def play_sounds(self, objects):
        # Play sound for each object
        waves = []
        # print(len(objects))
        # print([o.get_center() for o in objects])
        for obj in objects:
            # print(obj.get_center())
            # print((self.center_x, self.center_y))
            can_play = True
            
            # Check whether we must play the sound
            last_played = obj.get_object_attribute("last_played")
            if last_played is not None:
                can_play = False
                if datetime.datetime.now() > last_played + timedelta(seconds=1):
                    can_play = True

            if can_play:
                # print(obj.get_center())
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
        
        if len(waves) > 0:
            print(f"Playing {len(waves)} waves...")
            for wave in waves:
                print(f"Wave: F:({wave.frequency})")
            self.audio_system.chorus(waves)


    def handle_sound(self):
        while self.sounds_active:
            time.sleep(0.1)
            self.play_sounds(self.current_objects)

    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        corner_width = zone_border_corner_tl.get_width()
        corner_height = zone_border_corner_tl.get_height()
        border_width = zone_border_l.get_width()
        
        # Draw corners
        screen.blit(zone_border_corner_tl, (self.x,self.y))
        screen.blit(zone_border_corner_tr, (self.x + self.w - corner_width, self.y))
        
        screen.blit(zone_border_corner_bl, (self.x, 
                                            self.y + self.h - corner_height))
        screen.blit(zone_border_corner_br, (self.x + self.w - zone_border_corner_tl.get_width(), 
                                            self.y + self.h - corner_height))
        
        # Draw spanning rectangle
        
        # Vertical lines
        screen.blit(pygame.transform.scale(zone_border_l, (border_width, self.h 
                                                           - corner_height * 2)),
                    (self.x, self.y + corner_height))
        
        screen.blit(pygame.transform.scale(zone_border_l, (border_width, self.h 
                                                           - corner_height * 2)),
                    (self.x + self.w - border_width, self.y + corner_height))
        
        # Horizontal lines
        screen.blit(pygame.transform.scale(zone_border_t, (self.w - corner_width * 2,  
                                                           border_width)),
                    (self.x + corner_width, self.y))
        
        screen.blit(pygame.transform.scale(zone_border_t, (self.w - corner_width * 2,
                                                           border_width)),
                    (self.x + corner_width, self.y + self.h - border_width))
        
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