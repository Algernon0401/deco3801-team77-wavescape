"""
    ddcam.py - directly display camera
    
    Contains a simple control for demonstration purposes, which
    involves displaying the current input of the camera.
"""
import pygame

# Import app controller, control base class, camera and sound class
from ..base import Control
from ..base import AppController
from ..devices.camera import *
from ..object import *
from ..sound import *
from ..assets import *


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
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

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
        (self.w, self.h) = controller.get_screen_size()

        corner_width = asset_app_border_corner_tl.get_width()
        corner_height = asset_app_border_corner_tl.get_height()
        border_width = asset_app_border_l.get_width()

        # Draw corners
        screen.blit(asset_app_border_corner_tl, (self.x, self.y))
        screen.blit(
            asset_app_border_corner_tr, (self.x + self.w - corner_width, self.y)
        )

        screen.blit(
            asset_app_border_corner_bl, (self.x, self.y + self.h - corner_height)
        )
        screen.blit(
            asset_app_border_corner_br,
            (
                self.x + self.w - asset_app_border_corner_tl.get_width(),
                self.y + self.h - corner_height,
            ),
        )

        # Draw spanning rectangle

        # Vertical lines
        screen.blit(
            pygame.transform.scale(
                asset_app_border_l, (border_width, self.h - corner_height * 2)
            ),
            (self.x, self.y + corner_height),
        )

        screen.blit(
            pygame.transform.scale(
                asset_app_border_l, (border_width, self.h - corner_height * 2)
            ),
            (self.x + self.w - border_width, self.y + corner_height),
        )

        # Horizontal lines
        screen.blit(
            pygame.transform.scale(
                asset_app_border_t, (self.w - corner_width * 2, border_width)
            ),
            (self.x + corner_width, self.y),
        )

        screen.blit(
            pygame.transform.scale(
                asset_app_border_t, (self.w - corner_width * 2, border_width)
            ),
            (self.x + corner_width, self.y + self.h - border_width),
        )

    def event(self, controller: AppController, event: pygame.event.Event):
        """
        Receives an event from the pygame interface.

        Arguments:
            controller -- the app controller this control runs from
            event -- the pygame event that happened
        """
        pass
