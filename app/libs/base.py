"""
    Contains the two main classes of the pygame implementation:
    AppController and Control.
"""

# Import pygame for window rendering
import pygame

# import screeninfo

# Import camera
from .devices.camera import Camera

# Import audio system
from .sound import *

# Import control board
from .devices.control_board import ControlBoard

# Import camera object
from .object import *

# Create partial implementation of zone control

MOUSE_LEFT = 1  # Left pygame mouse button
MOUSE_RIGHT = 3  # Right pygame mouse button


class Control:
    pass


class Controller:
    pass


class AppController:
    """
    A basic controller for the pygame, which allows user-controls
    to interfere, interact, or 'see' the state of the window
    (including controls currently existing)
    """

    def __init__(self, screen: pygame.Surface):
        """
        Creates the controller
        """
        self.controls = []  # Control list
        self.static_controls = []  # Static control list
        self.controllers = []  # Controller list (for app logic)
        self.added_controls = []  # Next control list (controls added)
        self.removed_controls = []  # Next control list (controls removed)
        self.running = True
        self.calibrating = False
        self.playback_checkmark_required = True
        self.camera = Camera()
        self.board = ControlBoard()
        self.single_update = False
        self.screen = screen
        self.sound_player = Sound()
        self.show_camera_error = True
        self.show_model_error = True
        self.show_board_error = True

        self.objects = []
        self.use_test_control = False
        self.zones = []  # A list of zones (derived from controls)
        self.hover_control = None
        self.add_mouse_object = False
        self.display_feed = False
        self.object_attributes = {}
        self.persistent_objects = []  # Testing objects
        self.zone_border_object = Tag.ARROW.value
        self.current_screen = 0
        self.is_fullscreen = True
        self.board_valid = False

    def setup_calibration(self):
        """
        Setups the app to calibrate the camera.

        It achieves this by removing all standard controls, and
        then adding the calibration control.
        """
        # Import calibration control
        from libs.controls.calibration import Calibration

        # 'stash' controls so that they can be reinstated later
        self.stashed_controls = self.controls
        self.controls = []

        # Add new instance of calibration control
        self.add_control(Calibration(self))
        self.calibrating = True

        pass

    def finish_calibration(self):
        """
        Finishes the calibration by reinstating the controls
        that were previously displayed on screen
        """
        self.reinstate_controls()
        self.calibrating = False
        self.camera.save_calibration()

    def reinstate_controls(self):
        """
        Reinstates the previous controls that were 'stashed'
        """
        self.controls = self.stashed_controls

    def setup_main_control(self):
        """
        Reinstates or adds a new instance of the main control.

        If any zones exist, then they are re-added afterwards.
        """
        
        if self.use_test_control:
            # Import main control
            from libs.controls.testcontrol import TestControl

            # Add main control (test control)
            self.add_control(TestControl(self))

        # Re-add zones
        for zone in self.zones:
            self.add_control(zone, False)

    def swap_camera(self):
        """
        Swaps the current camera with another camera.
        """
        self.camera.init_next_camera()

    def toggle_fullscreen(self):
        """
        Allows the user to reposition the window
        """
        if self.is_fullscreen:
            pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.is_fullscreen = not self.is_fullscreen
        pass

    def get_object_attributes(self, object):
        """
        Gets the attributes for a
        specific object.
        """
        if not object.tag in self.object_attributes:
            return {}
        return self.object_attributes[object.tag]

    def get_object_attribute(self, object, attribute_name):
        """
        Gets a single attribute for a specific
        object
        """
        attributes = self.get_object_attributes(object)
        if attribute_name in attributes:
            return attributes[attribute_name]
        return None

    def set_object_attribute(self, object, attribute_name, attribute_value):
        """
        Sets the given attribute on the object.
        """
        if not object.tag in self.object_attributes:
            self.object_attributes[object.tag] = {}

        self.object_attributes[object.tag][attribute_name] = attribute_value

    def update(self):
        """
        Updates the app controller (updates camera), and checks for mouse hovers
        controls
        """

        self.camera.update(self)
        self.check_next_zone_mode()

        # Add persistent objects for testing
        for persistent_object in self.persistent_objects:
            self.objects.append(persistent_object)

        # Add mouse object for testing
        if self.add_mouse_object:
            (mx, my) = pygame.mouse.get_pos()
            self.objects.append(CamObject("mouse", (mx, my, 12, 20), 1))

        # Update currently (mouse) hovered control
        self.hover_control = None
        for control in self.controls:
            if control.interactive and control.is_mouse_over():
                self.hover_control = control
                break

        self.set_volume()

    def create_zone(self, position):
        """
        Creates a new zone at the given position.
        """
        from .controls.zone import Zone

        zone = Zone(self)

        # Set zone initial position
        (zone.x, zone.y) = position
        (w, h) = self.get_screen_size()
        zone.bound((0, 0, w, h))

        self.add_control(zone)
        return zone

    def set_cam_objects(self, object_list):
        """
        Updates the app's currently recognized objects.
        """
        self.objects = object_list

    def get_cam_objects(self):
        """
        Gets the app's currently recognized objects.
        """
        return self.objects

    def get_cam_objects_in_bounds(self, bounds):
        """
        Gets the app's currently recognized objects within
        the specified bounds
        """
        object_list = []
        for object in self.objects:
            if object.within(bounds):
                object_list.append(object)

        return object_list

    def has_object_in_bounds(self, tag, bounds):
        """
        Returns true if an object with the given tag
        exists within the bounds given.

        Arguments:
            tag - the tag of objects to check
            bounds - the bounds to check for
        """
        for object in self.objects:
            if object.tag == tag and object.within(bounds):
                return True
        return False

    def get_cam_objects_in_global(self):
        """
        Gets the list of camera objects that are in the 'global zone'.
        i.e. all objects that are not contained within a zone.
        """
        object_list = []

        # Add objects that do not belong in any zone.
        for object in self.objects:
            zone_object = False
            # Detect whether object belongs in zone
            for zone in self.zones:
                if object.within((zone.x, zone.y, zone.w, zone.h)):
                    zone_object = True
                    break

            if not zone_object:
                object_list.append(object)

        return object_list

    def get_screen_size(self):
        """
        Gets the current size of the pygame window
        """
        return pygame.display.get_surface().get_size()

    def is_running(self):
        """
        Returns True if the window will continue
        running on the next main loop iteration.
        """
        return self.running

    def get_controls(self):
        """
        Gets the list containing all controls
        currently active on the window.

        May not contain new controls, and may
        contain old controls.
        """
        return self.controls

    def get_static_controls(self):
        """
        Gets the list containing all static controls
        currently active on the window.
        """
        return self.static_controls

    def get_controllers(self):
        """
        Gets the list containing all logic controllers
        """
        return self.controllers

    def add_control(self, control: Control, check_zone=True):
        """
        Adds the control to the next controls list.
        If it is a zone, then adds it to the zone list as well unless
        if check_zone is false.
        """
        self.added_controls.append(control)
        if control.is_zone:
            self.zones.append(control)

    def add_static_control(self, control: Control):
        """
        Adds the control to the static controls list.
        These controls will never be removed (system controls)
        """
        self.static_controls.append(control)

    def add_persistent_object(self, tag, pos, size):
        """
        Adds a persistent object to the controller.
        """
        (x, y) = pos
        (w, h) = size
        self.persistent_objects.append(CamObject(tag, (x, y, w, h)))

    def remove_persistent_object(self):
        """
        Removes the last persistent object.
        """
        if len(self.persistent_objects) > 0:
            self.persistent_objects = self.persistent_objects[
                0 : len(self.persistent_objects) - 1
            ]

    def remove_control(self, control: Control):
        """
        Adds the control to the removed controls list.
        If it is a zone, then remove it from the zone list as well.
        """
        self.removed_controls.append(control)
        if control.is_zone:
            self.zones.remove(control)

    def destroy_all_controls(self):
        """
        Destroys all resources used by controls and removes them all
        """
        for control in self.controls:
            control.destroy()
        self.controls = []

    def add_controller(self, controller: Controller):
        """
        Adds a controller to the list of controllers.

        NOTE: the controller cannot be removed, and is supposed
        to remove in effect for the lifetime of the app.
        """
        self.controllers.append(controller)

    def set_clean_state(self):
        """
        Clears the newly added controls and removed controls
        list.
        """
        self.added_controls = []
        self.removed_controls = []

    def exit(self):
        """
        Exits the window by ensuring the main loop
        will exit.
        """
        self.running = False

    def is_mouse_over(self, bounds):
        """
        Returns true if the mouse is over a certain bounds
        """
        (mx, my) = pygame.mouse.get_pos()
        (bx, by, bw, bh) = bounds

        return mx >= bx and my >= by and mx < bx + bw and my < by + bh

    def connect_board(self):
        """
        Initializes the control board.
        """
        self.board.connect()

    def set_volume(self):
        """
        Sets the volume of the audio system.
        """
        volume = self.board.get_volume()
        channels = pygame.mixer.get_num_channels()
        for i in range(channels):
            channel = pygame.mixer.Channel(i)
            channel.set_volume(volume)

    def check_next_zone_mode(self):
        """
        Sets the modes of the currently selected zones.
        
        If the type of the zone is wavegen, then it switches the chords.
        If the type of the zone is arrangement, then it speeds up the arrangement.
        """
        if self.board.get_button_down():
            for zone in self.zones:
                if zone.selected:
                    zone.next_mode()

    def board_connected(self):
        """
        Returns true if the control board is connected.
        """
        return self.board.is_connected()


class Control:
    """
    This represents a single control on-screen in pygame.
    It could be the menu, an image, or an animation.
    """

    def __init__(self, controller: AppController):
        """
        Initializes the control

        Arguments:
            controller -- the app controller this control runs from
        """
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.is_zone = False
        self.interactive = False  # Set to True if this control interacts in any way
        pass

    def get_center(self):
        """
        Returns the center of the control
        """
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_bounds(self):
        """
        Returns the location and size of the control as a tuple
        """
        return (self.x, self.y, self.w, self.h)

    def is_mouse_over(self):
        """
        Returns true if the mouse is currently over this position
        """
        (mx, my) = pygame.mouse.get_pos()

        # Check if control can be hovered over
        if self.w <= 0 or self.h <= 0:
            return False

        # Check if mouse is within control bounds.
        return (
            mx >= self.x
            and my >= self.y
            and mx < self.x + self.w
            and my < self.y + self.h
        )

    def bound(self, bounds):
        """
        Ensures the control is fully displayed within the bounds,
        assuming that the control can fit inside the bounds.
        """
        (x, y, w, h) = bounds

        if self.x < x:
            self.x = x

        if self.y < y:
            self.y = y

        if self.x + self.w >= x + w:
            self.x = x + w - self.w

        if self.y + self.h >= y + h:
            self.y = y + h - self.h

    def within(self, bounds):
        """
        Returns True if the rectangle is contained within the control
        """
        (xf, yf, wf, hf) = bounds
        (x, y, w, h) = (self.x, self.y, self.w, self.h)
        return x + w >= xf and y + h >= yf and x < xf + wf and y < yf + hf

    def update(self, controller: AppController):
        """
        Updates the control on every loop iteration.

        Arguments:
            controller -- the app controller this control runs from
        """
        pass

    def render(self, controller: AppController, screen: pygame.Surface):
        """
        Renders the control on every loop iteration.

        Arguments:
            controller -- the app controller this control runs from
            screen -- the surface this control is drawn on.
        """
        pass

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
        Destroys all resources associated with the control.
        """
        pass


class Controller:
    """
    This represents a controller (excluding AppController) for the logic
    of a particular function of the app.
    """

    def __init__(self, controller: AppController):
        """
        Initializes the controller

        Arguments:
            controller -- the app controller this controller runs from
        """
        pass

    def update(self, controller: AppController):
        """
        Updates the controller on every loop iteration.

        Arguments:
            controller -- the app controller this controller runs from
        """
        pass

    def event(self, controller: AppController, event: pygame.event.Event):
        """
        Receives an event from the pygame interface.

        Arguments:
            controller -- the app controller this controller runs from
            event -- the pygame event that happened
        """
        pass
