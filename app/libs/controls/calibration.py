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
from ..assets import *

DISPLAY_OFFSET_FROM_BOTTOM = 300
NO_OF_CALIBRATION_STEPS = 5

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
        self.current_step = 0
        self.adjust_mode = 0 # 0 for x, 1 for y.
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
        
        if self.current_step == 0:
            feed = controller.camera.capture_video_pygame()
            if feed is not None:
                screen.blit(pygame.transform.scale(feed, (screen_w, screen_h)), (0,0))
        else:
            # Display calibration circles
            cc_width = asset_calibration_circle.get_width()
            cc_height = asset_calibration_circle.get_height()
            
            screen.blit(asset_calibration_circle, (50-cc_width/2, 50-cc_height/2))
            screen.blit(asset_calibration_circle, (screen_w-50-cc_width/2, 50-cc_height/2))
            screen.blit(asset_calibration_circle, (50-cc_width/2, screen_h-50-cc_height/2))
            screen.blit(asset_calibration_circle, (screen_w-50-cc_width/2, screen_h-50-cc_height/2))
            screen.blit(asset_calibration_circle, (screen_w/2-cc_width/2, screen_h/2-cc_height/2))
        
            # Display circles shapes
            for obj in controller.get_cam_objects():
                if obj.tag == Tag.CIRCLE.value:     
                    screen.blit(pygame.transform.scale(asset_calibration_circle_obj, (obj.w, obj.h)), (obj.x, obj.y))
        
        # Ensure step images are placed in center of screen.
        placement_x = screen_w / 2 - asset_calibration_step_one.get_width() / 2 
        
        # Display corresponding calibration step
        step_img = None
        if self.current_step == 0:
            step_img = asset_calibration_step_zero
        elif self.current_step == 1:
            step_img = asset_calibration_step_one
        elif self.current_step == 2:
            if self.adjust_mode == 0:
                step_img = asset_calibration_step_two
            else:
                step_img = asset_calibration_step_two_alt
        elif self.current_step == 3:
            if self.adjust_mode == 0:
                step_img = asset_calibration_step_three
            else:
                step_img = asset_calibration_step_three_alt
        elif self.current_step == 4:
            if self.adjust_mode == 0:
                step_img = asset_calibration_step_four
            else:
                step_img = asset_calibration_step_four_alt
        elif self.current_step == 5:
            if self.adjust_mode == 0:
                step_img = asset_calibration_step_five
            else:
                step_img = asset_calibration_step_five_alt
             
        if step_img is not None:
            screen.blit(step_img, (placement_x, screen_h-self.step_tip_offset))
        pass
    
    def next_step(self, controller: AppController):
        """
            Moves onto the next step
        """
        # Move onto next step
        self.current_step += 1
                
        # Check if we are finished calibration
        if self.current_step >= NO_OF_CALIBRATION_STEPS+1:
            # Finish calibration
            controller.finish_calibration()
            
    def last_step(self, controller: AppController):
        """
            Moves onto the last step
        """
        # Move onto next step
        self.current_step -= 1
        if self.current_step <= 0:
            self.current_step = 0        
        
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                self.next_step(controller)
            elif event.button == MOUSE_RIGHT:
                # Change between adjusting x/y
                self.adjust_mode = 1 - self.adjust_mode
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.next_step(controller)
            elif event.key == pygame.K_LEFT:
                self.last_step(controller)
        elif event.type == pygame.MOUSEWHEEL:
            if self.current_step == 0:
                # Darkness threshold
                next_threshold = (
                    controller.camera.dark_threshold 
                    + (1 if event.y > 0 else -1)
                )
                if next_threshold < 0:
                    next_threshold = 0
                if next_threshold > 255:
                    next_threshold = 255
                controller.camera.dark_threshold = next_threshold
            elif self.current_step == 2:
                # Center offset
                if self.adjust_mode == 0:
                    controller.camera.offset_x += event.y / 500
                else:
                    controller.camera.offset_y += event.y / 500
            elif self.current_step == 3:
                # Object sizing
                if self.adjust_mode == 0:
                    controller.camera.scale_x += event.y / 50
                else:
                    controller.camera.scale_y += event.y / 50
            elif self.current_step == 4:
                if self.adjust_mode == 0:
                    controller.camera.skew_top += event.y / 500
                else:
                    controller.camera.skew_left += event.y / 500
            elif self.current_step == 5:
                if self.adjust_mode == 0:
                    controller.camera.skew_bottom += event.y / 500
                else:
                    controller.camera.skew_right += event.y / 500
                
        pass