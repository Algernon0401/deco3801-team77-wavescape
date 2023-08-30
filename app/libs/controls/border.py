"""
    ddcam.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame
from datetime import *

# Import app controller, control base class, camera and sound class
from ..base import Control
from ..base import AppController
from ..devices.camera import *
from ..object import *
from ..sound import *

ASSET_APP_BORDER = 'assets/images/zone_border_l.png'
ASSET_APP_BORDER_CORNER = 'assets/images/zone_border_c.png'

app_boarder_l = pygame.image.load(ASSET_APP_BORDER)
APP_BORDER_t = pygame.transform.rotate(app_boarder_l, 90)
app_boarder_corner_tl = pygame.image.load(ASSET_APP_BORDER_CORNER)
app_boarder_corner_tr = pygame.transform.rotate(app_boarder_corner_tl, -90)
app_boarder_corner_br = pygame.transform.rotate(app_boarder_corner_tr, -90)
app_boarder_corner_bl = pygame.transform.rotate(app_boarder_corner_br, -90)

class AppBorder(Control):
    """
        Draws the app border
    """
    
    def __init__(self, controller: AppController):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.interactive = False
        
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
        self.x = 0
        self.y = 0
        (self.w, self.h) = controller.get_screen_size()
        
        corner_width = app_boarder_corner_tl.get_width()
        corner_height = app_boarder_corner_tl.get_height()
        border_width = app_boarder_l.get_width()
        
        # Draw corners
        screen.blit(app_boarder_corner_tl, (self.x,self.y))
        screen.blit(app_boarder_corner_tr, (self.x + self.w - corner_width, self.y))
        
        screen.blit(app_boarder_corner_bl, (self.x, 
                                            self.y + self.h - corner_height))
        screen.blit(app_boarder_corner_br, (self.x + self.w - app_boarder_corner_tl.get_width(), 
                                            self.y + self.h - corner_height))
        
        # Draw spanning rectangle
        
        # Vertical lines
        screen.blit(pygame.transform.scale(app_boarder_l, (border_width, self.h 
                                                           - corner_height * 2)),
                    (self.x, self.y + corner_height))
        
        screen.blit(pygame.transform.scale(app_boarder_l, (border_width, self.h 
                                                           - corner_height * 2)),
                    (self.x + self.w - border_width, self.y + corner_height))
        
        # Horizontal lines
        screen.blit(pygame.transform.scale(APP_BORDER_t, (self.w - corner_width * 2,  
                                                           border_width)),
                    (self.x + corner_width, self.y))
        
        screen.blit(pygame.transform.scale(APP_BORDER_t, (self.w - corner_width * 2,  
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