"""
    testcontrol.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *

font = pygame.font.Font("assets/fonts/arial.ttf", 16)


class TestControl(Control):
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
        self.display_feed = display_feed
        self.test_create_type = Tag.TRIANGLE.value

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

        # Draw outcome slightly
        if controller.display_feed:
            feed = controller.camera.capture_video_pygame()
            if feed is not None:
                feed.set_alpha(50)
                screen.blit(
                    pygame.transform.scale(feed, controller.get_screen_size()), (0, 0)
                )

        # Test every object location (draw location)
        for object in controller.objects:
            tag = object.tag
            # r = pygame.Surface((object.w,object.h))
            # r.set_alpha(33)
            # r.fill((255,255,255))
            # screen.blit(r, (object.x,object.y))
            text = font.render(
                str(tag) + str(object.track_id), True, pygame.Color(0, 128, 128)
            )
            text_rect = text.get_rect()
            text_rect.center = (object.x + object.w / 2, object.y - 20)
            screen.blit(text, text_rect)

        # Display current object to add
        text = font.render(self.test_create_type, True, pygame.Color(255, 255, 255))
        text_rect = text.get_rect()
        (sx, sy) = controller.get_screen_size()
        text_rect.center = (sx / 2, sy - 30)
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
                (mx, my) = pygame.mouse.get_pos()
                tag = self.test_create_type
                controller.add_persistent_object(tag, (mx, my), (24, 24))
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
            if event.key == pygame.K_b:
                # toggle a button press
                controller.board.press_button()
        pass
