"""
    app.py - initializes the window and controls the main logic of the app.  
"""

# Import camera class.
from libs.devices.camera import *

# Import control base and app controller
from libs.base import *

# Import controls
from libs.controls.ddcam import *

import pygame
        
def app_init():
    """
        Initializes the app
    """
    print("App Initializing...")
    
    # Initialize the pygame module
    pygame.init()
    
    # Set the caption for the window
    pygame.display.set_caption("Friction in Design Project - AR")
    
    # Initialise full screen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    
    # Main loop (runs infinitely until window exits)
    controller = AppController(screen)
    
    # Add initial controls
    controller.add_control(DDCamVisual(controller))
    
    while controller.is_running():
        # Update all controls
        for control in controller.get_controls():
            control.update(controller)
                   
        # Get all events from pygame, and exit if QUIT event exists.
        # Pass all events to controls.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.KMOD_ALT | pygame.K_F4):
                controller.exit()
                break
            else:
                for control in controller.get_controls():
                    control.event(controller, event)
        # Update control list
        for control in controller.added_controls:
            controller.controls.append(control)


        for control in controller.removed_controls:
            controller.controls.remove(control)
            
        # Update controller to clean state (no removed/added controls)
        controller.set_clean_state()
            
        # Render all controls
        for control in controller.get_controls():
            control.render(controller, controller.screen)
            
        # Update the screen
        pygame.display.flip()
    
    print("App Exiting...")
    

if __name__ == "__main__":
    app_init()