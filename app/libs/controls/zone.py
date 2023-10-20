"""
    zone.py - contains zone controls and functions
"""
import pygame
from ..geometry import *
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
from ..tone_generator import ToneGenerator, CHORDS
from ..assets import *

ZTYPE_OBJ_WAVEGEN = 0  # Generate waves for an object
ZTYPE_OBJ_ARRANGEMENT = 1  # Generate a tune arrangement from objects

PLAYBACK_MARKER_TAG = (
    Tag.PLUS.value
)  # Object to indicate playback is checked in playback box.

SELECTION_MARKER_TAG = (
    Tag.ARROW.value
) # Object to indicate zone is selected when placed inside it.
PLAYBACK_COOLDOWN = 0.1  # seconds

HIGH_AMP = 4000

WAVE_SPAN = 80  # How long a wave is in pixels
WAVE_QUALITY = (
    4  # The quality of the wave (larger numbers are faster but less visually appealing)
)
WAVE_CYCLES = 2  # How many cycles of a wave is displayed

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

METRONOME_BPM = 60  # Beats Per Minute
BPM_AMOUNTS = [30, METRONOME_BPM, 90, 120, 150, 180, 210, 240]

highlighted_zones_rlock = threading.RLock()
highlighted_zones = {
    Tag.STAR.value: False,
    Tag.CIRCLE.value: False,
    Tag.SQUARE.value: False,
    Tag.TRIANGLE.value: False,
}

def sine_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the sine wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    return math.sin(
        2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle
    )


def square_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the square wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    factor = math.sin(
        2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle
    )
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
    factor = math.sin(
        2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle
    )
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
    return math.sinh(
        math.sin(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
    )


def sawtooth_factor(d, time, dist_per_cycle, time_per_cycle):
    """
    Gets the sawtooth wave factor for the given distance d.
    i.e. the y position (percentage) should display at given dist using max amplitude.
    """
    return math.tanh(
        cot(2 * math.pi * d / dist_per_cycle + 2 * math.pi * time / time_per_cycle)
    )


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
    return (origin_x + d * rot_cos, origin_y + d * rot_sin)


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
    return (origin_x + d * rot_cos - y * rot_sin, origin_y + y * rot_cos + d * rot_sin)


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
        self.chord = "minor"
        self.is_global = False
        self.is_zone = True
        self.w = 128
        self.h = 128  # Standard size
        self.tone_gen = ToneGenerator()
        self.playing = {}
        # Allow for center definitions
        self.center_x = 0
        self.center_y = 0
        self.interactive = True
        self.object_attributes = {}
        self.graph = None
        self.current_objects = []
        self.sounds_active = True
        self.type = ZTYPE_OBJ_WAVEGEN
        self.wave_gen_tag = Tag.STAR.value  # default value for wavegen zone
        self.scaled_x = 0  # Ratio 0-1 of screen
        self.scaled_y = 0
        self.scaled_w = 0
        self.scaled_h = 0
        self.addsize_w = 0
        self.addsize_h = 0
        self.offset_x = 0
        self.offset_y = 0
        self.invalidate_waves = False
        self.metre = 0
        self.sound_enabled = False  # True if sound playback occurs
        self.sound_forced = False # True if the playback box is checked
        self.arrangement_bpm = METRONOME_BPM # 0.5 seconds per bar
        self.time_since_playback_existed = datetime.datetime.min
        # self.time_since_playback_placed = datetime.datetime.min
        self.arrange_thread = None
        self.selected = False

    def get_max_dist(self):
        """Returns min distance from centre to edge (max for tone generator to use)."""
        # return math.sqrt((self.w/2)**2 + (self.h/2)**2)
        return min(self.w, self.h) / 2

    def get_object_attributes(self, object):
        """
        Gets the zone-based attributes for a
        specific object.
        """
        if not object.tag in self.object_attributes:
            return {}
        return self.object_attributes[object.tag]

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
        return ObjectNode(
            object,
            center,
            [
                ObjectNode(o, o.get_center(), [])
                for o in objects
                if (
                    o.tag == "circle"
                    or o.tag == "square"
                    or o.tag == "triangle"
                    or o.tag == "star"
                )
            ],
        )

    def get_playback_box_bounds(self, controller: AppController):
        """
        Returns the bounds of a fixed playback checkbox,
        that is 30 in w/h.
        """
        return (self.x - 40, self.y, 30, 30)

    def next_mode(self):
        """
        Sets the next mode of the zone.
        
        If the type is wavegen, then switches the chords.
        Else if the type is arrangement, then speeds up the arrangement.
        """
        if self.type == ZTYPE_OBJ_WAVEGEN:
            # Get the chord that is next in the list
            for i, chord in enumerate(CHORDS):
                if chord == self.chord:
                    self.chord = CHORDS[(i + 1) % len(CHORDS)]
                    break
            
            self.invalidate_waves = True
                
        elif self.type == ZTYPE_OBJ_ARRANGEMENT:
            # Get the time that is next in the list
            for i, time in enumerate(BPM_AMOUNTS):
                if self.arrangement_bpm == time:
                    self.arrangement_bpm = BPM_AMOUNTS[(i + 1) % len(BPM_AMOUNTS)]
                    break
                    
    def update(self, controller: AppController):
        """
        Updates the control on every loop iteration.

        Arguments:
            controller -- the app controller this control runs from
        """
        global highlighted_zones_rlock
        global highlighted_zones
        objects = None
        (w, h) = controller.get_screen_size()
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
                highlighted = False
                with highlighted_zones_rlock:
                    if highlighted_zones[self.wave_gen_tag]:
                        highlighted = True
                
                # Update time since the playback marker was in the checkbox
                if (
                    controller.has_object_in_bounds(
                        PLAYBACK_MARKER_TAG, self.get_playback_box_bounds(controller)
                    )
                ):
                    self.time_since_playback_existed = datetime.datetime.now()
                
                time_passed = (
                        datetime.datetime.now() - self.time_since_playback_existed
                ).total_seconds()
                
                # Update whether the sounds in the zone should play
                if highlighted:
                    self.sound_enabled = True
                elif controller.playback_checkmark_required:
                    self.sound_enabled = (
                        time_passed < PLAYBACK_COOLDOWN
                    ) 
                else:
                    self.sound_enabled = True

                # Update whether the sound was forced to play (via marker)
                self.sound_forced = (
                    time_passed < PLAYBACK_COOLDOWN
                ) 
                
        if self.type == ZTYPE_OBJ_ARRANGEMENT:
            # Create thread for playing arranged sounds
            if self.arrange_thread is None:
                self.arrange_thread = threading.Thread(
                    target=self.metre_count, args=[controller]
                )
                self.arrange_thread.start()
            
            # Detect whether this arrangement zone should stop
            # based on whether a zone has been forced to play with a plus.
            self.sound_enabled = True
            for zone in controller.zones:
                if zone.type == ZTYPE_OBJ_WAVEGEN:
                    if zone.sound_forced:
                        self.sound_enabled = False
                        break

        center = self.get_center()
        (self.center_x, self.center_y) = center

        # Remove corner objects (of type)

        actual_objects = []

        # Update whether the zone is selected.
        self.selected = False
        for object in objects:
            if object.tag == SELECTION_MARKER_TAG:
                self.selected = True
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
                object.set_object_attribute("ripple_count", randint(2, 5))
            if object.get_object_attribute("ripple_colour") is None:
                object.set_object_attribute(
                    "ripple_colour",
                    pygame.Color(
                        randint(1, 255), randint(1, 255), randint(1, 255), 100
                    ),
                )

        if self.type == ZTYPE_OBJ_ARRANGEMENT:
            with highlighted_zones_rlock:
                highlighted_zones = dict.fromkeys(highlighted_zones, False)
            (x, y, w, h) = self.get_bounds()
            
            highlighted_objects = controller.get_cam_objects_in_bounds(
                (x + self.metre * w / 8, y, w / 8, h)
            )
            
            play_sounds = self.sound_enabled
            for object in highlighted_objects:
                if object is not None:
                    with highlighted_zones_rlock:
                        highlighted_zones[object.tag] = play_sounds

        return

    def metre_count(self, controller):
        """Cycles the arrangement zone highlight."""
        while controller.is_running():
            time.sleep(60 / self.arrangement_bpm)
            if self.sound_enabled:
                self.metre = 0 if self.metre == 7 else self.metre + 1  # loop from 0 to 7

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
        corner_width = asset_zone_border_corner_tl.get_width()
        corner_height = asset_zone_border_corner_tl.get_height()
        border_width = asset_zone_border_l.get_width()

        tl = asset_zone_border_corner_tl
        tr = asset_zone_border_corner_tr
        bl = asset_zone_border_corner_bl
        br = asset_zone_border_corner_br
        l = asset_zone_border_l
        t = asset_zone_border_t

        if self.selected:
            tl = asset_zone_border_corner_tl_sel
            tr = asset_zone_border_corner_tr_sel
            bl = asset_zone_border_corner_bl_sel
            br = asset_zone_border_corner_br_sel
            l = asset_zone_border_l_sel
            t = asset_zone_border_t_sel

        # Draw corners
        screen.blit(tl, (x, y))
        screen.blit(tr, (x + w - corner_width, y))

        screen.blit(bl, (x, y + h - corner_height))
        screen.blit(
            br,
            (x + w - tl.get_width(), y + h - corner_height),
        )

        # Draw spanning rectangle

        # Vertical lines
        screen.blit(
            pygame.transform.scale(l, (border_width, h - corner_height * 2)),
            (x, y + corner_height),
        )

        screen.blit(
            pygame.transform.scale(l, (border_width, h - corner_height * 2)),
            (x + w - border_width, y + corner_height),
        )

        if self.type == ZTYPE_OBJ_ARRANGEMENT:
            for i in range(7):
                screen.blit(
                    pygame.transform.scale(l, (border_width, h - corner_height * 2)),
                    (x + (i + 1) * w / 8 - border_width, y + corner_height),
                )

        # Horizontal lines
        screen.blit(
            pygame.transform.scale(t, (w - corner_width * 2, border_width)),
            (x + corner_width, y),
        )

        screen.blit(
            pygame.transform.scale(t, (w - corner_width * 2, border_width)),
            (x + corner_width, y + h - border_width),
        )

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
                objimg = asset_objimg_star
            elif self.wave_gen_tag == Tag.SQUARE.value:
                objimg = asset_objimg_square
            elif self.wave_gen_tag == Tag.TRIANGLE.value:
                objimg = asset_objimg_triangle
            elif self.wave_gen_tag == Tag.CIRCLE.value:
                objimg = asset_objimg_circle

            if objimg is not None:
                screen.blit(
                    objimg,
                    (
                        px + pw / 2 - objimg.get_width() / 2,
                        py + ph * 1.5 + 10 - objimg.get_height() / 2,
                    ),
                )
                screen.blit(
                    objimg,
                    (
                        self.x + self.w / 2 - objimg.get_width() / 2,
                        self.y + self.h / 2 - objimg.get_height() / 2,
                    ),
                )

            if self.sound_enabled:
                screen.blit(
                    asset_playback,
                    (
                        px + pw / 2 - asset_playback.get_width() / 2,
                        py + ph * 2.5 + 10 - asset_playback.get_height() / 2,
                    ),
                )

            # Draw octave circles
            max_dist = self.get_max_dist()
            for i in range(2):
                dist = (i + 1) * max_dist / 3
                pygame.draw.circle(
                    screen, pygame.Color(255, 255, 255), self.get_center(), dist, 2
                )

            lines = 3 if self.chord == "major" or self.chord == "minor" else 4
            rot_per_line = math.pi * 2 / lines
            rot = 0
            for i in range(lines):
                (cx, cy) = self.get_center()
                max_length = math.sqrt((self.x - cx) ** 2 + (self.y - cy) ** 2)
                line = (
                    (cx, cy),
                    (
                        (
                            max_length * math.cos(rot) + cx,
                            max_length * math.sin(rot) + cy,
                        )
                    ),
                )

                # Check zero slope lines and fix length
                if rot == 0 or (lines == 4 and (i == 0 or i == 2)):
                    length = self.w / 2
                elif rot == math.pi / 2 or (lines == 4 and (i == 1 or i == 3)):
                    length = self.h / 2
                elif rot == math.pi:
                    length = self.w / 2
                elif rot == 3 * math.pi / 2:
                    length = self.h / 2

                if lines == 3:
                    # Get intersection point of box to line
                    intersection = line_intersection_box(
                        line, (self.x, self.y, self.w, self.h)
                    )
                    length = max_length
                    if intersection is not None:
                        (px, py) = intersection
                        # Calculate length according to distance to intersection
                        length = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)

                if length > max_length:
                    length = max_length

                length -= 2  # Reduce length so that it doesn't draw over the border

                pygame.draw.line(
                    screen,
                    pygame.Color(255, 255, 255),
                    (cx, cy),
                    (length * math.cos(rot) + cx, length * math.sin(rot) + cy),
                    2,
                )
                rot += rot_per_line

        if self.type == ZTYPE_OBJ_ARRANGEMENT:
            zone_metre_indicator = pygame.Surface((self.w / 8, self.h), pygame.SRCALPHA)
            zone_metre_indicator.fill((255, 255, 255, 96))
            screen.blit(
                zone_metre_indicator, (self.x + self.metre * self.w / 8, self.y)
            )
            
            for object in self.current_objects:
                obj_img = None
                if object.tag == Tag.CIRCLE.value:
                    obj_img = asset_objimg_circle_dark
                elif object.tag == Tag.SQUARE.value:
                    obj_img = asset_objimg_square_dark
                elif object.tag == Tag.TRIANGLE.value:
                    obj_img = asset_objimg_triangle_dark
                elif object.tag == Tag.STAR.value:
                    obj_img = asset_objimg_star_dark

                if obj_img is not None:
                    (cx, cy) = object.get_center()
                    screen.blit(
                        obj_img,
                        (cx - object.w / 2, cy - object.h / 2),
                    )

        if self.is_global and not controller.use_global_zone:
            return  # No effects as global zone not in use

        # Draw animations between objects and on objects
        if self.graph is not None:
            self.graph.render(controller, screen, self)

        if self.type == ZTYPE_OBJ_WAVEGEN:
            # Draw chord text
            text = asset_tiny_font.render(
                    self.chord, True, pygame.Color(192,192,192)
                )
            text_rect = text.get_rect()
            text_rect.center = (self.x + 5 + text_rect.width / 2, +  self.y + 7)
            screen.blit(text, text_rect)

    def generate_ripples(self, screen: pygame.Surface, obj: CamObject):
        """
        Generates a ripple effect on the given object.
        """
        state = (math.sin(obj.get_time_since_creation() * 5) + 1) * 30
        ripple_count = obj.get_object_attribute("ripple_count")
        if ripple_count is None:
            ripple_count = 3
        colour = obj.get_object_attribute("ripple_colour")
        if colour is None:
            colour = pygame.Color(255, 255, 255, 100)

        for i in range(ripple_count):
            colour.a = 100 - (i * 20)  # Update alpha
            adj_state = state + (i * 10)
            rect = pygame.Rect(obj.get_center(), (0, 0)).inflate(
                (adj_state * 2, adj_state * 2)
            )
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
        self.sounds_active = False  # Dispose of extra threads


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

            amplitude = 2000  # to be edited later

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
            # t = datetime.datetime.now()

            # Generate wave points from wave rotation and factor
            if type_to == TYPE_SINE:
                add_point((self.center, color_from))
                wave_start = line_rotation(
                    dist / 2 - wave_span / 2, cx1, cy1, slope_rot
                )
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point(
                        (
                            wave_rotation(
                                sine_factor(d, time, dist_per_cycle, time_per_cycle),
                                d,
                                wave_span,
                                amp_dist,
                                wsx,
                                wsy,
                                slope_rot,
                            ),  # get position of sine wave at distance.
                            color_from.lerp(color_to, d / wave_span),
                        )
                    )

                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_SQUARE:
                add_point((self.center, color_from))
                wave_start = line_rotation(
                    dist / 2 - wave_span / 2, cx1, cy1, slope_rot
                )
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point(
                        (
                            wave_rotation(
                                square_factor(d, time, dist_per_cycle, time_per_cycle),
                                d,
                                wave_span,
                                amp_dist,
                                wsx,
                                wsy,
                                slope_rot,
                            ),  # get position of sine wave at distance.
                            color_from.lerp(color_to, d / wave_span),
                        )
                    )

                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_PULSE:
                duty_cycle = 0.125
                add_point((self.center, color_from))
                wave_start = line_rotation(
                    dist / 2 - wave_span / 2, cx1, cy1, slope_rot
                )
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point(
                        (
                            wave_rotation(
                                pulse_factor(
                                    duty_cycle, d, time, dist_per_cycle, time_per_cycle
                                ),
                                d,
                                wave_span,
                                amp_dist,
                                wsx,
                                wsy,
                                slope_rot,
                            ),  # get position of sine wave at distance.
                            color_from.lerp(color_to, d / wave_span),
                        )
                    )

                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_TRIANGLE:
                add_point((self.center, color_from))
                wave_start = line_rotation(
                    dist / 2 - wave_span / 2, cx1, cy1, slope_rot
                )
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point(
                        (
                            wave_rotation(
                                triangle_factor(
                                    d, time, dist_per_cycle, time_per_cycle
                                ),
                                d,
                                wave_span,
                                amp_dist,
                                wsx,
                                wsy,
                                slope_rot,
                            ),  # get position of sine wave at distance.
                            color_from.lerp(color_to, d / wave_span),
                        )
                    )

                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            elif type_to == TYPE_SAWTOOTH:
                add_point((self.center, color_from))
                wave_start = line_rotation(
                    dist / 2 - wave_span / 2, cx1, cy1, slope_rot
                )
                add_point((wave_start, color_from))
                (wsx, wsy) = wave_start
                for d in range(0, wave_span, WAVE_QUALITY):
                    add_point(
                        (
                            wave_rotation(
                                sawtooth_factor(
                                    d, time, dist_per_cycle, time_per_cycle
                                ),
                                d,
                                wave_span,
                                amp_dist,
                                wsx,
                                wsy,
                                slope_rot,
                            ),  # get position of sine wave at distance.
                            color_from.lerp(color_to, d / wave_span),
                        )
                    )

                add_point((line_rotation(wave_span, wsx, wsy, slope_rot), color_to))
                add_point((connection.center, color_to))
            else:
                points = [(self.center, color_from)]  # Single line

            points.append((connection.center, color_to))

            if len(points) == 0:
                pass

            connection.wave_lines = points  # Update to new wave list.

            connection.prerender_update(controller)

        self.completed = True

    def render(self, controller, screen, zone: Zone):
        """
        Renders the given tree/graph animations and elements onto the screen
        """
        self.prerender_update(controller)

        for connection in self.connections:
            # Render all lines in wave lines
            last_center = self.center
            wave_lines = connection.wave_lines

            # pygame.draw.aalines(screen, pygame.Color(255,255,255,255), False, wave_lines)

            for line in wave_lines:
                (center, color) = line
                pygame.draw.aaline(screen, color, last_center, center)
                last_center = center

                wave_img = None

            zone.generate_ripples(screen, connection.object)

            type = connection.sound_type()

            if type == TYPE_SINE:
                wave_img = asset_waveimg_sine
            elif type == TYPE_SQUARE:
                wave_img = asset_waveimg_square
            elif type == TYPE_TRIANGLE:
                wave_img = asset_waveimg_triangle
            elif type == TYPE_SAWTOOTH:
                wave_img = asset_waveimg_sawtooth

            if wave_img is not None:
                (cx, cy) = connection.center
                screen.blit(
                    wave_img,
                    (cx - wave_img.get_width() / 2, cy - wave_img.get_height() / 2),
                )
