"""
    ddcam.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *

ASSET_CALIBRATION_STEP_ONE = 'assets/images/calibration.s1.png'
ASSET_CALIBRATION_STEP_TWO = 'assets/images/calibration.s2.png'
asset_calibration_step_one = pygame.image.load(ASSET_CALIBRATION_STEP_ONE)
asset_calibration_step_two = pygame.image.load(ASSET_CALIBRATION_STEP_TWO)

DISPLAY_OFFSET_FROM_BOTTOM = 300

class Calibration(Control):
    """
        Reads the camera directly.
        If display_feed is set to true, then the camera feed
        is displayed to the window.
        (Test control)
    """
    
    def __init__(self, controller: AppController, display_feed=False):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.x = 0
        self.y = 0
        (self.w, self.h) = controller.get_screen_size()
        self.current_step = 1
        self.step_tip_offset = 0
        self.last_time_updated = datetime.datetime.now()
    
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        
        time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        
        # (Animated) Move tip from bottom to slight offset 
        if self.step_tip_offset < DISPLAY_OFFSET_FROM_BOTTOM:
            self.step_tip_offset += ((DISPLAY_OFFSET_FROM_BOTTOM-self.step_tip_offset + 1) * time_passed)
            if self.step_tip_offset > DISPLAY_OFFSET_FROM_BOTTOM:
                self.step_tip_offset = DISPLAY_OFFSET_FROM_BOTTOM
                
        self.last_time_updated = datetime.datetime.now()
        pass
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        
        (screen_w,screen_h) = controller.get_screen_size()
        
        # Ensure step images are placed in center of screen.
        placement_x = screen_w / 2 - asset_calibration_step_one.get_width() / 2 
        
        # Display corresponding calibration step
        if self.current_step == 1:
            screen.blit(asset_calibration_step_one, (placement_x, screen_h-self.step_tip_offset))
        elif self.current_step == 2:
            screen.blit(asset_calibration_step_two, (placement_x, screen_h-self.step_tip_offset))
        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                # Move onto next step
                pass

        pass