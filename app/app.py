"""
    app.py - initializes the window and controls the main logic of the app.  
"""

import sys

# Import camera class.
from libs.devices.camera import *

# Import control base and app controller
from libs.base import *

# Import controls
from libs.controls.ddcam import *
from libs.controls.border import *
from libs.controls.menu import *

# Import logic controllers
from libs.controllers.zone_controller import * 

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
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Main loop (runs infinitely until window exits)
    controller = AppController(screen)
    
    # Read command line arguments
    try:
        for arg in sys.argv[1:]:
            if arg == "-mo":
                controller.add_mouse_object = True
            if arg == "-tz":
                controller.add_persistent_object(controller.zone_border_object, (190,190), (24,24))
                controller.add_persistent_object(controller.zone_border_object, (390,190), (24,24))
                controller.add_persistent_object(controller.zone_border_object, (390,390), (24,24))
                controller.add_persistent_object(controller.zone_border_object, (190,390), (24,24))
    except:
        print("Invalid command-line arguments")
        
    # Add initial controls (displayed first)
    
    controller.add_control(DDCamVisual(controller))

    # Add static system controls (displayed last)

    controller.add_static_control(AppBorder(controller))
    controller.add_static_control(Menu(controller))

    # Add logic controllers
    controller.add_controller(ZoneController(controller))

    while controller.is_running():
        # Update camera objects and basic logic
        controller.update()

        # Update all controls
        for control in controller.get_controls():
            control.update(controller)

        # Update all static (overlay) controls
        for control in controller.get_static_controls():
            control.update(controller)

        # Update all logic controls
        for lc in controller.get_controllers():
            lc.update(controller)
            
        # Get all events from pygame, and exit if QUIT event exists.
        # Pass all events to controls.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and event.key == pygame.KMOD_ALT | pygame.K_F4
            ):
                controller.exit()
                break
            else:
                # Update display controls
                for control in controller.get_controls():
                    control.event(controller, event)

                # Update static (system) controls
                for control in controller.get_static_controls():
                    control.event(controller, event)

                # Update logic controllers
                for lc in controller.get_controllers():
                    lc.event(controller, event)
        
        # Update control list
        for control in controller.added_controls:
            controller.controls.append(control)

        for control in controller.removed_controls:
            controller.controls.remove(control)

        # Update controller to clean state (no removed/added controls)
        controller.set_clean_state()

        # Clear screen
        screen.fill(pygame.Color(0, 0, 0))

        # Render all controls
        for control in controller.get_controls():
            control.render(controller, controller.screen)

        # Render all overlaying controls (all controls that must be on top of everything else)
        for control in controller.get_static_controls():
            control.render(controller, controller.screen)

        # Update the screen
        pygame.display.flip()

    # Release resources
    controller.camera.destroy()

    print("App Exiting...")


if __name__ == "__main__":
    app_init()
