"""
    Contains the two main classes of the pygame implementation:
    AppController and Control.
"""

# Import pygame for window rendering
import pygame

# Import camera
from .devices.camera import Camera


class Control:
    pass


class AppController:
    """
    A controller for the pygame, which allows user-controls
    to interfere, interact, or 'see' the state of the window
    (including controls currently existing)
    """

    def __init__(self, screen: pygame.Surface):
        """
        Creates the controller with the given screen
        """
        self.screen = screen
        self.controls = []  # Control list
        self.added_controls = []  # Next control list (controls added)
        self.removed_controls = []  # Next control list (controls removed)
        self.running = True
        self.camera = Camera()
        self.objects = []

    def update(self):
        """
        Updates the app controller (updates camera)
        """
        self.camera.update(self)

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

    def add_control(self, control: Control):
        """
        Adds the control to the next controls list
        """
        self.added_controls.append(control)

    def remove_control(self, control: Control):
        """
        Adds the control to the removed controls list
        """
        self.removed_controls.append(control)

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
        pass

    def update(self, controller: AppController):
        """
        Updates the control on every loop iteration.

        Arguments:
            controller -- the app controller this control runs from
        """
        pass

    def render(self, controller: AppController, screen: pygame.Surface):
        """
        Updates the control on every loop iteration.

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
