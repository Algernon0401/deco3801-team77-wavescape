"""
    app.py - initializes the window and controls the main logic of the app.  
"""


def app_init():
    """
    Initializes the app
    """
    import pygame
    import sys

    # Import camera class.
    from libs.devices.camera import Camera

    import threading

    from libs.object import Tag

    # Import control base and app controller
    from libs.base import Control, AppController

    # Import controls
    from libs.controls.border import AppBorder
    from libs.controls.menu import Menu
    from libs.controls.status import Status
    from libs.controls.zone import Zone, ZTYPE_OBJ_WAVEGEN, ZTYPE_OBJ_ARRANGEMENT

    # Initialize the pygame module
    pygame.init()

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
                controller.add_mouse_object = False  # No longer valid
            if arg == "-np":
                controller.playback_checkmark_required = False
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

    # Add zones
    z_star = Zone(controller)
    z_star.type = ZTYPE_OBJ_WAVEGEN
    z_star.wave_gen_tag = Tag.STAR.value
    z_star.scaled_x = 0.02
    z_star.scaled_y = 0.02
    z_star.scaled_w = 0.31
    z_star.scaled_h = 0.47
    z_star.addsize_w = -40
    z_star.offset_x = 40

    z_circle = Zone(controller)
    z_circle.type = ZTYPE_OBJ_WAVEGEN
    z_circle.wave_gen_tag = Tag.CIRCLE.value
    z_circle.scaled_x = 0.35
    z_circle.scaled_y = 0.02
    z_circle.scaled_w = 0.31
    z_circle.scaled_h = 0.47
    z_circle.reduction_w = 40
    z_circle.offset_x = 40
    z_circle.addsize_w = -40

    z_square = Zone(controller)
    z_square.type = ZTYPE_OBJ_WAVEGEN
    z_square.wave_gen_tag = Tag.SQUARE.value
    z_square.scaled_x = 0.68
    z_square.scaled_y = 0.02
    z_square.scaled_w = 0.31
    z_square.scaled_h = 0.47
    z_square.addsize_w = -40
    z_square.offset_x = 40

    z_triangle = Zone(controller)
    z_triangle.type = ZTYPE_OBJ_WAVEGEN
    z_triangle.wave_gen_tag = Tag.TRIANGLE.value
    z_triangle.scaled_x = 0.68
    z_triangle.scaled_y = 0.51
    z_triangle.scaled_w = 0.31
    z_triangle.scaled_h = 0.47
    z_triangle.addsize_w = -40
    z_triangle.offset_x = 40

    z_arrange = Zone(controller)
    z_arrange.type = ZTYPE_OBJ_ARRANGEMENT
    z_arrange.scaled_x = 0.02
    z_arrange.scaled_y = 0.51
    z_arrange.scaled_w = 0.64
    z_arrange.scaled_h = 0.47

    controller.add_control(z_arrange)
    controller.add_control(z_triangle)
    controller.add_control(z_square)
    controller.add_control(z_circle)
    controller.add_control(z_star)

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
        # controller.global_zone.update(controller)

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

    print("App Exiting...")


def app_render(controller, screen):
    """
    Continuously renders the app.
    """
    import time
    import pygame

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
        # controller.global_zone.render(controller, screen)

        # Render all overlaying controls (all controls that must be on top of everything else)
        for control in controller.get_static_controls():
            control.render(controller, screen)

        # Update the screen
        pygame.display.flip()
    print("Render thread exiting...")


if __name__ == "__main__":
    app_init()
