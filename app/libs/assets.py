"""
    assets.py - Hosts all of the assets (images) used in the app.
"""


import pygame

ASSET_MENU_BAR = "assets/images/menu/bar.png"
ASSET_MENU_BAR_STATE_HOVER = "assets/images/menu/bar.hover.png"
ASSET_MENU_BAR_STATE_MOUSE = "assets/images/menu/bar.mouse.png"
ASSET_MENU_POPUP_ITEM_HOVER = "assets/images/menu/item.hover.png"
ASSET_MENU_POPUP_ITEM_MOUSE = "assets/images/menu/item.mouse.png"
ASSET_MENU_POPUP_CONTAINER = "assets/images/menu/container.png"

ASSET_MENU_BUTTON_HIDE = "assets/images/menu/button_hide.png"
ASSET_MENU_BUTTON_QUIT = "assets/images/menu/button_quit.png"
ASSET_MENU_BUTTON_CALIBRATE = "assets/images/menu/button_calibrate.png"
ASSET_MENU_BUTTON_SWAP_CAMERA = "assets/images/menu/button_swap_camera.png"
ASSET_MENU_BUTTON_TOGGLE_FULLSCREEN = "assets/images/menu/button_toggle_fullscreen.png"
ASSET_MENU_BUTTON_RECONNECT_BOARD = "assets/images/menu/button_reconnect_board.png"

ASSET_CALIBRATION_STEP_ZERO = "assets/images/calibration.s0.png"
ASSET_CALIBRATION_STEP_ONE = "assets/images/calibration.s1.png"
ASSET_CALIBRATION_STEP_TWO = "assets/images/calibration.s2.png"
ASSET_CALIBRATION_STEP_TWO_ALT = "assets/images/calibration.s2.alt.png"
ASSET_CALIBRATION_STEP_THREE = "assets/images/calibration.s3.png"
ASSET_CALIBRATION_STEP_THREE_ALT = "assets/images/calibration.s3.alt.png"
ASSET_CALIBRATION_STEP_FOUR = "assets/images/calibration.s4.png"
ASSET_CALIBRATION_STEP_FOUR_ALT = "assets/images/calibration.s4.alt.png"
ASSET_CALIBRATION_STEP_FIVE = "assets/images/calibration.s5.png"
ASSET_CALIBRATION_STEP_FIVE_ALT = "assets/images/calibration.s5.alt.png"
ASSET_CALIBRATION_CIRCLE = "assets/images/calibration_circle.png"
ASSET_CALIBRATION_CIRCLE_OBJ = "assets/images/calibration_circle_obj.png"

ASSET_APP_BORDER = "assets/images/zone_border_l.png"
ASSET_APP_BORDER_CORNER = "assets/images/zone_border_c.png"

ASSET_CAMERA_INVALID_OVERLAY = "assets/images/camera_invalid_overlay.png"
ASSET_CAMERA_LOADING_OVERLAY = "assets/images/camera_loading_overlay.png"
ASSET_MODEL_INVALID_OVERLAY = "assets/images/model_invalid_overlay.png"
ASSET_MODEL_LOADING_OVERLAY = "assets/images/model_loading_overlay.png"
ASSET_BOARD_INVALID_OVERLAY = "assets/images/board_invalid_overlay.png"

ASSET_ZONE_BORDER = "assets/images/zone_border_l.png"
ASSET_ZONE_BORDER_CORNER = "assets/images/zone_border_c.png"
ASSET_ZONE_BORDER_SEL = "assets/images/zone_border_l_sel.png"
ASSET_ZONE_BORDER_CORNER_SEL = "assets/images/zone_border_c_sel.png"

ASSET_STAR = "assets/images/obj_star.png"
ASSET_SQUARE = "assets/images/obj_square.png"
ASSET_CIRCLE = "assets/images/obj_circle.png"
ASSET_TRIANGLE = "assets/images/obj_triangle.png"
ASSET_STAR_DARK = "assets/images/obj_star_dark.png"
ASSET_SQUARE_DARK = "assets/images/obj_square_dark.png"
ASSET_CIRCLE_DARK = "assets/images/obj_circle_dark.png"
ASSET_TRIANGLE_DARK = "assets/images/obj_triangle_dark.png"
ASSET_PLAYBACK = "assets/images/playback.png"

ASSET_SAWTOOTH_WAVE = "assets/images/wave_sawtooth.png"
ASSET_SQUARE_WAVE = "assets/images/wave_square.png"
ASSET_SINE_WAVE = "assets/images/wave_sine.png"
ASSET_TRIANGLE_WAVE = "assets/images/wave_triangle.png"

pygame.font.init()

asset_small_font = pygame.font.Font("assets/fonts/arial.ttf", 16)
asset_tiny_font = pygame.font.Font("assets/fonts/arial.ttf", 9)

asset_menu_bar = pygame.image.load(ASSET_MENU_BAR)
asset_menu_bar_hover = pygame.image.load(ASSET_MENU_BAR_STATE_HOVER)
asset_menu_bar_mouse = pygame.image.load(ASSET_MENU_BAR_STATE_MOUSE)
asset_menu_popup_container = pygame.image.load(ASSET_MENU_POPUP_CONTAINER)
asset_menu_popup_item_hover = pygame.image.load(ASSET_MENU_POPUP_ITEM_HOVER)
asset_menu_popup_item_mouse = pygame.image.load(ASSET_MENU_POPUP_ITEM_MOUSE)
asset_menu_button_hide = pygame.image.load(ASSET_MENU_BUTTON_HIDE)
asset_menu_button_quit = pygame.image.load(ASSET_MENU_BUTTON_QUIT)
asset_menu_button_calibrate = pygame.image.load(ASSET_MENU_BUTTON_CALIBRATE)
asset_menu_button_toggle_fullscreen = pygame.image.load(
    ASSET_MENU_BUTTON_TOGGLE_FULLSCREEN
)
asset_menu_button_swap_camera = pygame.image.load(ASSET_MENU_BUTTON_SWAP_CAMERA)
asset_menu_button_reconnect_board = pygame.image.load(ASSET_MENU_BUTTON_RECONNECT_BOARD)

asset_calibration_step_zero = pygame.image.load(ASSET_CALIBRATION_STEP_ZERO)
asset_calibration_step_one = pygame.image.load(ASSET_CALIBRATION_STEP_ONE)
asset_calibration_step_two = pygame.image.load(ASSET_CALIBRATION_STEP_TWO)
asset_calibration_step_two_alt = pygame.image.load(ASSET_CALIBRATION_STEP_TWO_ALT)
asset_calibration_step_three = pygame.image.load(ASSET_CALIBRATION_STEP_THREE)
asset_calibration_step_three_alt = pygame.image.load(ASSET_CALIBRATION_STEP_THREE_ALT)
asset_calibration_step_four = pygame.image.load(ASSET_CALIBRATION_STEP_FOUR)
asset_calibration_step_four_alt = pygame.image.load(ASSET_CALIBRATION_STEP_FOUR_ALT)
asset_calibration_step_five = pygame.image.load(ASSET_CALIBRATION_STEP_FIVE)
asset_calibration_step_five_alt = pygame.image.load(ASSET_CALIBRATION_STEP_FIVE_ALT)

asset_calibration_circle = pygame.image.load(ASSET_CALIBRATION_CIRCLE)
asset_calibration_circle_obj = pygame.image.load(ASSET_CALIBRATION_CIRCLE_OBJ)

asset_app_border_l = pygame.image.load(ASSET_APP_BORDER)
asset_app_border_t = pygame.transform.rotate(asset_app_border_l, 90)
asset_app_border_corner_tl = pygame.image.load(ASSET_APP_BORDER_CORNER)
asset_app_border_corner_tr = pygame.transform.rotate(asset_app_border_corner_tl, -90)
asset_app_border_corner_br = pygame.transform.rotate(asset_app_border_corner_tr, -90)
asset_app_border_corner_bl = pygame.transform.rotate(asset_app_border_corner_br, -90)

asset_invalid_camera_overlay = pygame.image.load(ASSET_CAMERA_INVALID_OVERLAY)
asset_loading_camera_overlay = pygame.image.load(ASSET_CAMERA_LOADING_OVERLAY)
asset_invalid_model_overlay = pygame.image.load(ASSET_MODEL_INVALID_OVERLAY)
asset_loading_model_overlay = pygame.image.load(ASSET_MODEL_LOADING_OVERLAY)
asset_invalid_board_overlay = pygame.image.load(ASSET_BOARD_INVALID_OVERLAY)

asset_objimg_star = pygame.image.load(ASSET_STAR)
asset_objimg_square = pygame.image.load(ASSET_SQUARE)
asset_objimg_circle = pygame.image.load(ASSET_CIRCLE)
asset_objimg_triangle = pygame.image.load(ASSET_TRIANGLE)
asset_objimg_star_dark = pygame.image.load(ASSET_STAR_DARK)
asset_objimg_square_dark = pygame.image.load(ASSET_SQUARE_DARK)
asset_objimg_circle_dark = pygame.image.load(ASSET_CIRCLE_DARK)
asset_objimg_triangle_dark = pygame.image.load(ASSET_TRIANGLE_DARK)

asset_playback = pygame.image.load(ASSET_PLAYBACK)

asset_waveimg_sine = pygame.image.load(ASSET_SINE_WAVE)
asset_waveimg_square = pygame.image.load(ASSET_SQUARE_WAVE)
asset_waveimg_triangle = pygame.image.load(ASSET_TRIANGLE_WAVE)
asset_waveimg_sawtooth = pygame.image.load(ASSET_SAWTOOTH_WAVE)

asset_zone_border_l = pygame.image.load(ASSET_ZONE_BORDER)
asset_zone_border_t = pygame.transform.rotate(asset_zone_border_l, 90)
asset_zone_border_corner_tl = pygame.image.load(ASSET_ZONE_BORDER_CORNER)
asset_zone_border_corner_tr = pygame.transform.rotate(asset_zone_border_corner_tl, -90)
asset_zone_border_corner_br = pygame.transform.rotate(asset_zone_border_corner_tr, -90)
asset_zone_border_corner_bl = pygame.transform.rotate(asset_zone_border_corner_br, -90)

asset_zone_border_l_sel = pygame.image.load(ASSET_ZONE_BORDER_SEL)
asset_zone_border_t_sel = pygame.transform.rotate(asset_zone_border_l_sel, 90)
asset_zone_border_corner_tl_sel = pygame.image.load(ASSET_ZONE_BORDER_CORNER_SEL)
asset_zone_border_corner_tr_sel = pygame.transform.rotate(
    asset_zone_border_corner_tl_sel, -90
)
asset_zone_border_corner_br_sel = pygame.transform.rotate(
    asset_zone_border_corner_tr_sel, -90
)
asset_zone_border_corner_bl_sel = pygame.transform.rotate(
    asset_zone_border_corner_br_sel, -90
)
