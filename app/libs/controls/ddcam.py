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

ASSET_CAMERA_INVALID_OVERLAY = 'assets/images/camera_invalid_overlay.png'
ASSET_CAMERA_LOADING_OVERLAY = 'assets/images/camera_loading_overlay.png'
ASSET_MODEL_INVALID_OVERLAY = 'assets/images/model_invalid_overlay.png'
ASSET_MODEL_LOADING_OVERLAY = 'assets/images/model_loading_overlay.png'

class DDCamVisual(Control):
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
        self.invalid_camera_overlay = pygame.image.load(ASSET_CAMERA_INVALID_OVERLAY)
        self.loading_camera_overlay = pygame.image.load(ASSET_CAMERA_LOADING_OVERLAY)
        self.invalid_model_overlay = pygame.image.load(ASSET_MODEL_INVALID_OVERLAY)
        self.loading_model_overlay = pygame.image.load(ASSET_MODEL_LOADING_OVERLAY)
        self.display_feed = display_feed
        self.test_create_type = Tag.TRIANGLE.value
        self.font = pygame.font.Font('assets/fonts/arial.ttf', 16)
    
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
        
        overlay_y = 5
        # Check if camera is loading, and if so display loading image
        if controller.camera.loading:
            screen.blit(self.loading_camera_overlay, (5,overlay_y))
            overlay_y += 20
        else:    
            # Capture frame, and if none then display invalid camera image.
            frame = controller.camera.capture_video_pygame()        
            if frame is None:
                screen.blit(self.invalid_camera_overlay, (5,overlay_y))
                overlay_y += 20
            else:
                if self.display_feed:
                    screen.blit(pygame.transform.scale(frame, controller.get_screen_size()), (0,0), None)   
        
        # Check if model is loading, and if so display loading image.
        if controller.camera.model_loading:
            screen.blit(self.loading_model_overlay, (5,overlay_y))
            overlay_y += 20
        elif controller.camera.model is None:
            screen.blit(self.invalid_model_overlay, (5,overlay_y))
            overlay_y += 20
            
        # Test every object location (draw location)
        for object in controller.objects:
            tag = object.tag
            r = pygame.Surface((object.w,object.h))
            r.set_alpha(128)
            r.fill((255,255,255))
            screen.blit(r, (object.x,object.y))
            text = self.font.render(tag, True, pygame.Color(0, 128, 128))
            text_rect = text.get_rect()
            text_rect.center = (object.x+object.w/2,object.y+object.h/2)
            screen.blit(text, text_rect)

        # Display current object to add
        text = self.font.render(self.test_create_type, True, pygame.Color(255, 255, 255))
        text_rect = text.get_rect()
        (sx,sy) = controller.get_screen_size()
        text_rect.center = (sx/2, sy-30)
        screen.blit(text, text_rect)
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
                # Place persistent object
                (mx,my) = pygame.mouse.get_pos()
                tag = self.test_create_type
                controller.add_persistent_object(tag, (mx,my), (64,64))
            elif event.button == MOUSE_RIGHT:
                index = ALL_TAGS.index(self.test_create_type)
                index = index + 1
                if index >= len(ALL_TAGS):
                    index = 0
                self.test_create_type = ALL_TAGS[index]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                # Undo last object
                controller.remove_persistent_object()
        pass