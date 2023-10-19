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
from ..assets import *


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
            screen.blit(asset_loading_camera_overlay, (5,overlay_y))
            overlay_y += 20
        elif controller.show_camera_error:    
            # Capture frame, and if none then display invalid camera image.
            frame = True
            if not self.camera_verified:
                frame = controller.camera.capture_video()
                if frame is not None:
                    self.camera_verified = True
            if frame is None:
                screen.blit(asset_invalid_camera_overlay, (5,overlay_y))
                overlay_y += 20
        
        # Check if model is loading, and if so display loading image.
        if controller.camera.model_loading:
            screen.blit(asset_loading_model_overlay, (5,overlay_y))
            overlay_y += 20
        elif controller.show_model_error and controller.camera.model is None:
            screen.blit(asset_invalid_model_overlay, (5,overlay_y))
            overlay_y += 20
            
        # Check if board is invalid (since board loads quickly, no need for loading overlay).
        if controller.show_board_error and not controller.board_connected():
            screen.blit(asset_invalid_board_overlay, (5,overlay_y))
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