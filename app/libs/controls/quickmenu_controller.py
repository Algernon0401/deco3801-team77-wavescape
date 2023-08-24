"""
    menu.py
    
    Contains a simple widget, that can be docked at either corner
    of the projected surface.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *
from .quickmenu import *

class QuickMenuController(Control):
    """
        Controls how quick menu's appear in the app.
    """
    
    def __init__(self, controller: AppController):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
    
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        
        # All logic is handled using pygame events (see event function)

        pass
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            (since this is simply a controller, there is no rendering)
            
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
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_RIGHT and controller.hover_control is None:
            # Create new quick menu at the position, 
            # but make sure it won't collide with another quickmenu
            # If it does then remove the old quick menu
            (mx,my) = pygame.mouse.get_pos()
            menu = QuickMenu(controller)
            menu.x = mx
            menu.y = my
            
            # Menu must fully display within bounds of screen.
            (w,h) = controller.get_screen_size()
            menu.bound((0, 0, w, h))
            
            controller.add_control(menu)
        pass