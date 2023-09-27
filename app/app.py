"""
    app.py - initializes the window and controls the main logic of the app.  
"""
import pygame

# Initialize the pygame module
pygame.init()

import sys

# Import camera class.
from libs.devices.camera import *

from threading import *

# Import control base and app controller
from libs.base import *

# Import controls
from libs.controls.border import *
from libs.controls.menu import *
from libs.controls.status import *

# Import logic controllers
from libs.controllers.zone_controller import * 



def app_init():
    """
    Initializes the app
    """
    
    print("App Initializing...")

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
                controller.add_persistent_object(controller.zone_border_object, (790,190), (24,24))
                controller.add_persistent_object(controller.zone_border_object, (790,790), (24,24))
                controller.add_persistent_object(controller.zone_border_object, (190,790), (24,24))
            if arg == "-gz":
                controller.use_global_zone = True
            if arg == "-feed":
                controller.display_feed = True
    except:
        print("Invalid command-line arguments")
        
    # Add initial controls (displayed first)
    # In this app, only the main control should be added.
    # Zone are later configured, and re-added if necessary.
    controller.setup_main_control()

    # Add static system controls (displayed last)

    controller.add_static_control(Menu(controller))
    controller.add_static_control(Status(controller))

    # Add logic controllers
    controller.add_controller(ZoneController(controller))

    # Create render thread
    threading.Thread(target=app_render, args=[controller, screen]).start()

    while controller.is_running():
        # Update camera objects and basic logic
        controller.update()

        # Update all controls
        for control in controller.get_controls():
            control.update(controller)

        # Update all static (overlay) controls
        for control in controller.get_static_controls():
            control.update(controller)
            
        # Update global zone control
        controller.global_zone.update(controller)

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
            control.destroy()
            controller.controls.remove(control)

        # Update controller to clean state (no removed/added controls)
        controller.set_clean_state()

        # Single update (to allow rendering)
        controller.single_update = True

    # Release resources
    controller.destroy_all_controls()
    controller.camera.destroy()
    controller.audio_system.destroy()

    print("App Exiting...")

def app_render(controller: AppController, screen: pygame.Surface):
    """
    Continuously renders the app.
    """
    while controller.is_running():
        if not controller.single_update:
            time.sleep(0.06)
            continue

        # Clear screen
        screen.fill(pygame.Color(0, 0, 0))

        # Render all controls
        for control in controller.get_controls():
            control.render(controller, screen)

        # Render global zone control
        controller.global_zone.render(controller, screen)

        # Render all overlaying controls (all controls that must be on top of everything else)
        for control in controller.get_static_controls():
            control.render(controller, screen)

        
        # Update the screen
        pygame.display.flip()
    print("Render thread exiting...")



if __name__ == "__main__":
    app_init()
