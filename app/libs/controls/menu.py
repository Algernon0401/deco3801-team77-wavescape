"""
    menu.py - the main menu (mouse only) for setting up the system.
    
    Contains, updates and renders the main menu bar which can be
    expanded to activate certain modes for setting up the workspace.
"""
import pygame
from datetime import *

# Import app controller, control base class, camera and sound class
from ..base import *
from ..devices.camera import *
from ..object import *
from ..sound import *

ASSET_MENU_BAR = 'assets/images/menu/bar.png'
ASSET_MENU_BAR_STATE_HOVER = 'assets/images/menu/bar.hover.png'
ASSET_MENU_BAR_STATE_MOUSE = 'assets/images/menu/bar.mouse.png'
ASSET_MENU_POPUP_ITEM_HOVER = 'assets/images/menu/item.hover.png'
ASSET_MENU_POPUP_ITEM_MOUSE = 'assets/images/menu/item.mouse.png'
ASSET_MENU_POPUP_CONTAINER = 'assets/images/menu/container.png'

ASSET_MENU_BUTTON_QUIT = 'assets/images/menu/button_quit.png'
ASSET_MENU_BUTTON_CALIBRATE = 'assets/images/menu/button_calibrate.png'
ASSET_MENU_BUTTON_SWAP_CAMERA = 'assets/images/menu/button_swap_camera.png'

asset_menu_bar = pygame.image.load(ASSET_MENU_BAR)
asset_menu_bar_hover = pygame.image.load(ASSET_MENU_BAR_STATE_HOVER)
asset_menu_bar_mouse = pygame.image.load(ASSET_MENU_BAR_STATE_MOUSE)

asset_menu_popup_container = pygame.image.load(ASSET_MENU_POPUP_CONTAINER)
asset_menu_popup_item_hover = pygame.image.load(ASSET_MENU_POPUP_ITEM_HOVER)
asset_menu_popup_item_mouse = pygame.image.load(ASSET_MENU_POPUP_ITEM_MOUSE)

asset_menu_button_quit = pygame.image.load(ASSET_MENU_BUTTON_QUIT)
asset_menu_button_calibrate = pygame.image.load(ASSET_MENU_BUTTON_CALIBRATE)
asset_menu_button_swap_camera = pygame.image.load(ASSET_MENU_BUTTON_SWAP_CAMERA)

class MenuItem:
        """
        Depicts an item on the main menu.
        """

        def __init__(self, descriptor, function):
            """
            Creates a menu item with the given image descriptor and function.

            Arguments:
                descriptor -- an image that will be drawn onto the UI
                function -- the function that will be activated when this is clicked.
            """
            self.descriptor = descriptor
            self.function = function

class Menu(Control):
    """
        Controls for the main menu.
    """

    
    
    def __init__(self, controller: AppController):
        """
            Initializes the control
            
            Arguments:
                controller -- the app controller this control runs from
        """
        super().__init__(controller)
        self.interactive = True
        self.mouse_down = False 
        self.expanded = False
        self.menu_offset = 0 # Offset from bottom
        # Initialise menu options
        self.items = [
            MenuItem(asset_menu_button_swap_camera, controller.swap_camera),
            MenuItem(asset_menu_button_calibrate, controller.setup_calibration),
            MenuItem(asset_menu_button_quit, controller.exit)
        ]
        self.last_time_updated = datetime.datetime.now()

    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """

        time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        (self.w, self.h) = controller.get_screen_size()
        self.x = self.w - 20 - asset_menu_bar.get_width()
        self.y = self.h - asset_menu_bar.get_height()
        
        menu_height = asset_menu_popup_container.get_height()
        # Expand and collapse popup
        if self.expanded:
            min_offset = -menu_height - self.h
            if self.menu_offset > min_offset:
                self.menu_offset -= time_passed * 1000
                self.menu_offset += time_passed * self.menu_offset
                if self.menu_offset < min_offset:
                    self.menu_offset = min_offset
        else:
            if self.menu_offset < 0:
                self.menu_offset += time_passed * 1000
                self.menu_offset -= time_passed * self.menu_offset
                if self.menu_offset > 0:
                    self.menu_offset = 0
        
        self.last_time_updated = datetime.datetime.now()
        pass

    def toggle(self):
        """
        Toggles whether the menu is visible or not.
        """
        self.expanded = not self.expanded

    def select_state(self, controller: AppController, bounds, state_normal, state_hover, state_down):
        """
        Selects either the normal, hover, or down state depending on the
        current mouse position and state in the bounds
        """

        if not controller.is_mouse_over(bounds):
            return state_normal
        
        if self.mouse_down:
            return state_down
        
        return state_hover

    
    def render(self, controller: AppController, screen: pygame.Surface):
        """
            Renders the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
                screen -- the surface this control is drawn on.
        """

        # Draw main container for overlay if somewhat expanded
        if self.menu_offset < 0:
            menu_height = asset_menu_popup_container.get_height()
            menu_y = self.y + self.h + self.menu_offset
            screen.blit(asset_menu_popup_container, (self.x, menu_y))
            button_height = asset_menu_popup_item_mouse.get_height()
            # Draw all menu items
            for button in self.items:
                bg_state = self.select_state(controller, 
                                             (self.x, menu_y, self.w, button_height), None,
                                             asset_menu_popup_item_hover, asset_menu_popup_item_mouse)
                if bg_state is not None:
                    screen.blit(bg_state, (self.x, menu_y))

                screen.blit(button.descriptor, (self.x, menu_y))    
                
                menu_y += button_height

        # Determine bar state and draw bar respectively
        bar_state = self.select_state(controller, (self.x, self.y, self.w, self.h), 
                                      asset_menu_bar, asset_menu_bar_hover, asset_menu_bar_mouse)

        screen.blit(bar_state, (self.x, self.y))

        
        
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = event.button == MOUSE_LEFT
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down:
                # Activate whatever control the mouse is over
                if controller.is_mouse_over((self.x, self.y, self.w, self.h)):
                    self.toggle()
                else:
                     # Check all menu items for clicked button
                    menu_y = self.y + self.h + self.menu_offset
                    button_height = asset_menu_popup_item_mouse.get_height()
                    for button in self.items:
                        if controller.is_mouse_over((self.x, menu_y, self.w, button_height)):
                            button.function()
                            break
                
                        menu_y += button_height

                
            self.mouse_down = False
        pass