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

ASSET_MENU_BUTTON_HIDE = 'assets/images/menu/button_hide.png'
ASSET_MENU_BUTTON_QUIT = 'assets/images/menu/button_quit.png'
ASSET_MENU_BUTTON_CALIBRATE = 'assets/images/menu/button_calibrate.png'
ASSET_MENU_BUTTON_SWAP_CAMERA = 'assets/images/menu/button_swap_camera.png'
ASSET_MENU_BUTTON_TOGGLE_FULLSCREEN = 'assets/images/menu/button_toggle_fullscreen.png'
ASSET_MENU_BUTTON_RECONNECT_BOARD = 'assets/images/menu/button_reconnect_board.png'

asset_menu_bar = pygame.image.load(ASSET_MENU_BAR)
asset_menu_bar_hover = pygame.image.load(ASSET_MENU_BAR_STATE_HOVER)
asset_menu_bar_mouse = pygame.image.load(ASSET_MENU_BAR_STATE_MOUSE)

asset_menu_popup_container = pygame.image.load(ASSET_MENU_POPUP_CONTAINER)
asset_menu_popup_item_hover = pygame.image.load(ASSET_MENU_POPUP_ITEM_HOVER)
asset_menu_popup_item_mouse = pygame.image.load(ASSET_MENU_POPUP_ITEM_MOUSE)

asset_menu_button_hide = pygame.image.load(ASSET_MENU_BUTTON_HIDE)
asset_menu_button_quit = pygame.image.load(ASSET_MENU_BUTTON_QUIT)
asset_menu_button_calibrate = pygame.image.load(ASSET_MENU_BUTTON_CALIBRATE)
asset_menu_button_toggle_fullscreen = pygame.image.load(ASSET_MENU_BUTTON_TOGGLE_FULLSCREEN)
asset_menu_button_swap_camera = pygame.image.load(ASSET_MENU_BUTTON_SWAP_CAMERA)
asset_menu_button_reconnect_board = pygame.image.load(ASSET_MENU_BUTTON_RECONNECT_BOARD)

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

# Initialise menu options
items = [
    MenuItem(asset_menu_button_toggle_fullscreen, lambda controller: controller.toggle_fullscreen()),
    MenuItem(asset_menu_button_swap_camera, lambda controller: controller.swap_camera()),
    MenuItem(asset_menu_button_calibrate, lambda controller: controller.setup_calibration()),
    MenuItem(asset_menu_button_reconnect_board, lambda controller: controller.reconnect_board()),
    MenuItem(asset_menu_button_quit, lambda controller: controller.exit()),
    MenuItem(asset_menu_button_hide, lambda controller: None)
]

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
        self.w = asset_menu_bar.get_width()
        self.h = asset_menu_bar.get_height() 
        self.last_time_updated = datetime.datetime.now()

    def update(self, controller: AppController):
        """
            Updates the control on every loop iteration.
            
            Arguments:
                controller -- the app controller this control runs from
        """

        time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        (screen_w, screen_h) = controller.get_screen_size()
        self.x = screen_w - self.w
        self.y = screen_h - self.h
        
        menu_x = screen_w - asset_menu_popup_container.get_width()
        menu_height = asset_menu_popup_container.get_height()
        # Expand and collapse popup
        if self.expanded:
            min_offset = -menu_height
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
        (screen_w, screen_h) = controller.get_screen_size()
        
        # Draw main container for overlay if somewhat expanded
        if self.menu_offset < 0:
            menu_x = screen_w - asset_menu_popup_container.get_width()
            menu_height = asset_menu_popup_container.get_height()
            menu_y = self.y + self.h + self.menu_offset
            screen.blit(asset_menu_popup_container, (menu_x, menu_y))
            button_height = asset_menu_popup_item_mouse.get_height()
            button_width = asset_menu_popup_item_mouse.get_width()
            # Draw all menu items
            for button in items:
                bg_state = self.select_state(controller, 
                                             (menu_x, menu_y, button_width, button_height), None,
                                             asset_menu_popup_item_hover, asset_menu_popup_item_mouse)
                if bg_state is not None:
                    screen.blit(bg_state, (menu_x, menu_y))

                screen.blit(button.descriptor, (menu_x, menu_y))    
                
                menu_y += button_height

        # Determine bar state and draw bar respectively
        bar_state = self.select_state(controller, (self.x, self.y, self.w, self.h+1), 
                                      asset_menu_bar, asset_menu_bar_hover, asset_menu_bar_mouse)

        screen.blit(bar_state, (self.x, self.y))

        
        
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
            Receives an event from the pygame interface.
            
            Arguments:
                controller -- the app controller this control runs from
                event -- the pygame event that happened
        """
        
        # Check to make sure the app isn't calibrating (deny access to menu)
        if controller.calibrating:
            return
        
        (screen_w, screen_h) = controller.get_screen_size()
        
        # Activate corresponding mouse event 
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = event.button == MOUSE_LEFT
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down:
                # Activate whatever control the mouse is over
                if controller.is_mouse_over((self.x, self.y, self.w, self.h+1)):
                    self.toggle()
                else:
                    # Check all menu items for clicked button
                    menu_x = screen_w - asset_menu_popup_container.get_width()
                    menu_y = self.y + self.h + self.menu_offset
                    button_width = asset_menu_popup_item_mouse.get_width()
                    button_height = asset_menu_popup_item_mouse.get_height()
                    for button in items:
                        if controller.is_mouse_over((menu_x, menu_y, button_width, button_height)):
                            self.expanded = False # Hide menu
                            button.function(controller)
                            break
                
                        menu_y += button_height

                
            self.mouse_down = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle()
        pass