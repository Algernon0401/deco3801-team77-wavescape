"""
    menu.py
    
    Contains a simple widget, that can be docked at either corner
    of the projected surface.
"""
import pygame

# Import app controller, control base class and camera
from ..base import *
from ..devices.camera import *
from ..object import *

ASSET_MENU_WIDGET = 'assets/images/menu/widget.png'
ASSET_MENU_EXIT_BUTTON = 'assets/images/menu/exit_button.png'

class MenuButton:
    """
    Represents a button in the menu
    """
    def __init__(self, image, func):
        """
        Creates a menu button with the given image and function
        """
        self.image = image
        self.image_dark = image.copy()
        self.image_dark.set_alpha(180)
        self.func = func
        self.width = image.get_width()
        self.height = image.get_height()

class Menu(Control):
    """
        Represents an instance of a menu widget.
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
        self.menu_widget = pygame.image.load(ASSET_MENU_WIDGET)
        self.menu_widget_dark = self.menu_widget.copy()
        self.menu_widget_dark.set_alpha(180)
        self.w = self.menu_widget.get_width()
        self.h = self.menu_widget.get_height()
        self.font = pygame.font.Font('assets/fonts/arial.ttf', 12)
        self.expanded = False
        self.hover_button = None
        self.buttons = [
            MenuButton(pygame.image.load(ASSET_MENU_EXIT_BUTTON),
                       controller.exit)
            ]
    
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        (mx, my) = pygame.mouse.get_pos()
        self.expanded = (mx >= self.x and my >= self.y and mx < self.x + self.w and my < self.y + self.h)
        self.hover_button = None

        # See which button is hovered over
        y = self.y + self.h
        for button in self.buttons:
            if mx >= self.x and my >= y and mx < self.x + button.width and my < y + button.height:
                self.hover_button = button
                break
            y += button.height

        if self.hover_button is not None:
            self.expanded = True # Keep expanded
        
        pass
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        (mx, my) = pygame.mouse.get_pos()

        # Select widget image
        widget = self.menu_widget
        if (mx >= self.x and my >= self.y and mx < self.x + self.w and my < self.y + self.h):
            widget = self.menu_widget_dark

        # Draw widget image (menu button)
        screen.blit(widget, (0,0))

        
        # Draw buttons when expanded
        y = self.h
        if self.expanded:
            for button in self.buttons:
                img = button.image
                
                if self.hover_button == button:
                    img = button.image_dark

                screen.blit(img, (0, y))
                y += button.height

        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover_button is not None:
            self.hover_button.func()
        pass