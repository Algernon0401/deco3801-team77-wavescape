"""
    Contains the two main classes of the pygame implementation:
    AppController and Control.
"""

# Import pygame for window rendering
import pygame

# Import camera
from .devices.camera import Camera
from .object import CamObject

# Create partial implementation of zone control

MOUSE_LEFT = 1 # Left pygame mouse button
MOUSE_RIGHT = 3 # Right pygame mouse button

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
        Creates the controller with the given screen
        """
        self.screen = screen
        self.controls = []  # Control list
        self.controllers = [] # Controller list (for app logic)
        self.added_controls = []  # Next control list (controls added)
        self.removed_controls = []  # Next control list (controls removed)
        self.running = True
        self.camera = Camera()
        self.objects = []
        self.zones = [] # A list of zones (derived from controls)
        self.hover_control = None
        self.add_mouse_object = False
        self.add_test_zone = False
        self.object_attributes = {}
        self.persistent_objects = [] # Testing objects
    
    def get_object_attributes(self, object):
        """
            Gets the attributes for a
            specific object.
        """
        if not object.tag in self.object_attributes:
            return {}
        return  self.object_attributes[object.tag]
    
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

        # Add persistent objects for testing 
        for persistent_object in self.persistent_objects:
            self.objects.append(persistent_object)

        # Update currently (mouse) hovered control
        self.hover_control = None
        for control in self.controls:
            if control.interactive and control.is_mouse_over():
                self.hover_control = control
                break
            
        # Add mouse object for testing
        if self.add_mouse_object:
            (mx,my) = pygame.mouse.get_pos()
            self.objects.append(CamObject("mouse", (mx,my, 12, 20), 1))
        
        # Add test zone object for testing (using square object)
        if self.add_test_zone:
            self.objects.append(CamObject("square", (64,64, 64, 64)))
            self.objects.append(CamObject("square", (394,64, 64, 64)))
            self.objects.append(CamObject("square", (64,364, 64, 64)))
            self.objects.append(CamObject("square", (394,364, 64, 64)))
        
        # Update logic controllers
        for controller in self.controllers:
            controller.update(self)
        
    def create_zone(self, position):
        """
        Creates a new zone at the given position.
        """
        from .controls.zone import Zone
        zone = Zone(self)
        
        # Set zone initial position
        (zone.x, zone.y) = position
        (w,h) = self.get_screen_size()
        zone.bound((0,0,w,h))
        
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
    
    def get_controllers(self):
        """
        Gets the list containing all logic controllers
        """
        return self.controllers

    def add_control(self, control: Control):
        """
        Adds the control to the next controls list.
        If it is a zone, then adds it to the zone list as well.
        """
        self.added_controls.append(control)
        from .controls.zone import Zone
        if control is Zone:
            self.zones.append(control)

    def add_persistent_object(self, tag, pos, size):
        """
        Adds a persistent object to the controller.
        """
        (x,y) = pos
        (w,h) = size
        self.persistent_objects.append(CamObject(
            tag,
            (x,y,w,h)
        ))

    def remove_persistent_object(self):
        """
        Removes the last persistent object.
        """
        if len(self.persistent_objects) > 0:
            self.persistent_objects = self.persistent_objects[0:len(self.persistent_objects)-1]
    def remove_control(self, control: Control):
        """
        Adds the control to the removed controls list.
        If it is a zone, then remove it from the zone list as well.
        """
        self.removed_controls.append(control)
        from .controls.zone import Zone
        if control is Zone:
            self.zones.remove(control)
            
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
        self.interactive = False # Set to True if this control interacts in any way
        pass
    
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
        return mx >= self.x and my >= self.y and mx < self.x + self.w and my < self.y + self.h
    
    def bound(self, bounds):
        """
        Ensures the control is fully displayed within the bounds,
        assuming that the control can fit inside the bounds.
        """
        (x,y,w,h) = bounds
        
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
        (xf,yf,wf,hf) = bounds
        (x,y,w,h) = (self.x, self.y, self.w, self.h)
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