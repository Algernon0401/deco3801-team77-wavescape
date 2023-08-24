"""
    ddcam.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class and camera
from ..base import Control
from ..base import AppController
from ..devices.camera import *
from ..object import *

ASSET_ZONE_BORDER = 'assets/images/zone_border_l.png'
ASSET_ZONE_BORDER_CORNER = 'assets/images/zone_border_c.png'

zone_border_l = pygame.image.load(ASSET_ZONE_BORDER)
zone_border_t = pygame.transform.rotate(zone_border_l, 90)
zone_border_corner_tl = pygame.image.load(ASSET_ZONE_BORDER_CORNER)
zone_border_corner_tr = pygame.transform.rotate(zone_border_corner_tl, -90)
zone_border_corner_br = pygame.transform.rotate(zone_border_corner_tr, -90)
zone_border_corner_bl = pygame.transform.rotate(zone_border_corner_br, -90)

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
        self.interactive = True
    
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
        
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        pass