"""
    ddcam.py
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *

ASSET_CAMERA_INVALID_OVERLAY = 'assets/images/camera_invalid_overlay.png'
ASSET_CAMERA_LOADING_OVERLAY = 'assets/images/camera_loading_overlay.png'

class DDCamVisual(Control):
    """
        Reads the camera directly and displays it on screen. 
        (Test control)
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
        self.invalid_camera_overlay = pygame.image.load(ASSET_CAMERA_INVALID_OVERLAY)
        self.loading_camera_overlay = pygame.image.load(ASSET_CAMERA_LOADING_OVERLAY)
        self.font = pygame.font.Font('assets/fonts/arial.ttf', 12)
    
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
        # Check if camera is loading, and if so display loading image
        if controller.camera.loading:
            screen.blit(self.loading_camera_overlay, (145,5))
        else:    
            # Capture frame, and if none then display invalid camera image.
            frame = controller.camera.capture_video_pygame()        
            if frame is None:
                screen.blit(self.invalid_camera_overlay, (145,5))
            else:
                screen.blit(pygame.transform.scale(frame, controller.get_screen_size()), (0,0), None)   
        
        # Test every object location (draw location)
        for object in controller.objects:
            tag = object.tag
            (bx,by,bw,bh) = object.bounds
            r = pygame.Surface((bw,bh))
            r.set_alpha(128)
            r.fill((255,255,255))
            screen.blit(r, (bx,by))
            text = self.font.render(tag, True, pygame.Color(0, 128, 128))
            text_rect = text.get_rect()
            text_rect.center = (bx+bw/2,by+bh/2)
            screen.blit(text, text_rect)

        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        pass