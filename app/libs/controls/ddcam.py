"""
    ddcam.py
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *


class DDCamVisual(Control):
    """
        Reads the camera directly and displays it on screen. 
        (Test control)
        
        (Unimplemented at this point)
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
        (self.w, self.h) = controller.get_screen_size()
        # self.camera = Camera()
    
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
        pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(self.x, self.y, self.w, self.h))
        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        pass