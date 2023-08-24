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
from .menu import MenuButton

from datetime import *
ASSET_MENU_CREATE_ZONE = 'assets/images/menu/create_zone.png'

quickmenu_assets_loaded = False
quickmenu_buttons = []


class QuickMenu(Control):
    """
        Represents an instance of a quick menu.
    """
    
    def __init__(self, controller: AppController):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        global quickmenu_assets_loaded
        global quickmenu_buttons
        
        super().__init__(controller)
        self.x = 0
        self.y = 0
        
        if not quickmenu_assets_loaded:
            quickmenu_assets_loaded = True
            # All buttons must take tuple (x,y) as parameter
            quickmenu_buttons = [
                MenuButton(pygame.image.load(ASSET_MENU_CREATE_ZONE),
                           controller.create_zone)
                ]
            
        self.w = quickmenu_buttons[0].image.get_width()
        self.h = quickmenu_buttons[0].image.get_height() * len(quickmenu_buttons)
        self.hover_button = None
        self.buttons = quickmenu_buttons
        self.interactive = True
        self.lifespan = 1
        self.mouse = pygame.mouse.get_pos()
        self.last_focus_lost = datetime.now()
    
    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """
        (mx, my) = pygame.mouse.get_pos()
        
        # See which button is hovered over
        y = self.y
        self.hover_button = None
        for button in self.buttons:
            if mx >= self.x and my >= y and mx < self.x + button.width and my < y + button.height:
                self.hover_button = button
                self.last_focus_lost = datetime.now() 
                break
            y += button.height

        if self.hover_button is None:
            self.lifespan -= (datetime.now() - self.last_focus_lost).total_seconds()
            if self.lifespan <= 0:
                # We can remove this control as no hovering is detected
                controller.remove_control(self)
            self.last_focus_lost = datetime.now() 
        
        pass
    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """
        (mx, my) = pygame.mouse.get_pos()

        # Draw buttons when expanded
        y = self.y
        for button in self.buttons:
            img = button.image
                
            if self.hover_button == button:
               img = button.image_dark

            screen.blit(img, (self.x, y))
            y += button.height

        pass
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT and self.hover_button is not None:
            self.hover_button.func(self.mouse)
            controller.remove_control(self)
        pass