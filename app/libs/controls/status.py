"""
    status.py - status for camera device and model
    
    Contains a control which displays the status of the camera and YOLO model.
    (i.e. Camera Loading... Camera Off. etc)
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *

ASSET_CAMERA_INVALID_OVERLAY = 'assets/images/camera_invalid_overlay.png'
ASSET_CAMERA_LOADING_OVERLAY = 'assets/images/camera_loading_overlay.png'
ASSET_MODEL_INVALID_OVERLAY = 'assets/images/model_invalid_overlay.png'
ASSET_MODEL_LOADING_OVERLAY = 'assets/images/model_loading_overlay.png'

invalid_camera_overlay = pygame.image.load(ASSET_CAMERA_INVALID_OVERLAY)
loading_camera_overlay = pygame.image.load(ASSET_CAMERA_LOADING_OVERLAY)
invalid_model_overlay = pygame.image.load(ASSET_MODEL_INVALID_OVERLAY)
loading_model_overlay = pygame.image.load(ASSET_MODEL_LOADING_OVERLAY)

class Status(Control):
    """
        Displays the status of the camera and YOLO model.
    """
    
    def __init__(self, controller: AppController):
        """
            Initializes the status text control, which displays
            the status of the device and model on screen
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.x = 0
        self.y = 0
        self.camera_verified = False
    
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        if controller.camera.model_loading:
            self.camera_verified = False
        pass
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        overlay_y = 5
        # Check if camera is loading, and if so display loading image
        if controller.camera.loading:
            screen.blit(loading_camera_overlay, (5,overlay_y))
            overlay_y += 20
        else:    
            # Capture frame, and if none then display invalid camera image.
            frame = True
            if not self.camera_verified:
                frame = controller.camera.capture_video()
                if frame is not None:
                    self.camera_verified = True
            if frame is None:
                screen.blit(invalid_camera_overlay, (5,overlay_y))
                overlay_y += 20
        
        # Check if model is loading, and if so display loading image.
        if controller.camera.model_loading:
            screen.blit(loading_model_overlay, (5,overlay_y))
            overlay_y += 20
        elif controller.camera.model is None:
            screen.blit(invalid_model_overlay, (5,overlay_y))
            overlay_y += 20
        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        pass