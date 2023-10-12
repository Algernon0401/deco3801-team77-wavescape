import pygame

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

ASSET_CALIBRATION_STEP_ONE = 'assets/images/calibration.s1.png'
ASSET_CALIBRATION_STEP_TWO = 'assets/images/calibration.s2.png'
ASSET_CALIBRATION_CIRCLE = 'assets/images/calibration_circle.png'

ASSET_APP_BORDER = 'assets/images/zone_border_l.png'
ASSET_APP_BORDER_CORNER = 'assets/images/zone_border_c.png'

ASSET_CAMERA_INVALID_OVERLAY = 'assets/images/camera_invalid_overlay.png'
ASSET_CAMERA_LOADING_OVERLAY = 'assets/images/camera_loading_overlay.png'
ASSET_MODEL_INVALID_OVERLAY = 'assets/images/model_invalid_overlay.png'
ASSET_MODEL_LOADING_OVERLAY = 'assets/images/model_loading_overlay.png'
ASSET_BOARD_INVALID_OVERLAY = 'assets/images/board_invalid_overlay.png'

ASSET_ZONE_BORDER = "assets/images/zone_border_l.png"
ASSET_ZONE_BORDER_CORNER = "assets/images/zone_border_c.png"

ASSET_STAR = "assets/images/obj_star.png"
ASSET_SQUARE = "assets/images/obj_square.png"
ASSET_CIRCLE = "assets/images/obj_circle.png"
ASSET_TRIANGLE = "assets/images/obj_triangle.png"

ASSET_SAWTOOTH_WAVE = "assets/images/wave_sawtooth.png"
ASSET_SQUARE_WAVE = "assets/images/wave_square.png"
ASSET_SINE_WAVE = "assets/images/wave_sine.png"
ASSET_TRIANGLE_WAVE = "assets/images/wave_triangle.png"


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

asset_calibration_step_one = pygame.image.load(ASSET_CALIBRATION_STEP_ONE)
asset_calibration_step_two = pygame.image.load(ASSET_CALIBRATION_STEP_TWO)
asset_calibration_circle = pygame.image.load(ASSET_CALIBRATION_CIRCLE)


app_boarder_l = pygame.image.load(ASSET_APP_BORDER)
app_border_t = pygame.transform.rotate(app_boarder_l, 90)
app_boarder_corner_tl = pygame.image.load(ASSET_APP_BORDER_CORNER)
app_boarder_corner_tr = pygame.transform.rotate(app_boarder_corner_tl, -90)
app_boarder_corner_br = pygame.transform.rotate(app_boarder_corner_tr, -90)
app_boarder_corner_bl = pygame.transform.rotate(app_boarder_corner_br, -90)

invalid_camera_overlay = pygame.image.load(ASSET_CAMERA_INVALID_OVERLAY)
loading_camera_overlay = pygame.image.load(ASSET_CAMERA_LOADING_OVERLAY)
invalid_model_overlay = pygame.image.load(ASSET_MODEL_INVALID_OVERLAY)
loading_model_overlay = pygame.image.load(ASSET_MODEL_LOADING_OVERLAY)
invalid_board_overlay = pygame.image.load(ASSET_BOARD_INVALID_OVERLAY)

objimg_star = pygame.image.load(ASSET_STAR)
objimg_square = pygame.image.load(ASSET_SQUARE)
objimg_circle = pygame.image.load(ASSET_CIRCLE)
objimg_triangle = pygame.image.load(ASSET_TRIANGLE)

waveimg_sine = pygame.image.load(ASSET_SINE_WAVE)
waveimg_square = pygame.image.load(ASSET_SQUARE_WAVE)
waveimg_triangle = pygame.image.load(ASSET_TRIANGLE_WAVE)
waveimg_sawtooth = pygame.image.load(ASSET_SAWTOOTH_WAVE)

zone_border_l = pygame.image.load(ASSET_ZONE_BORDER)
zone_border_t = pygame.transform.rotate(zone_border_l, 90)
zone_border_corner_tl = pygame.image.load(ASSET_ZONE_BORDER_CORNER)
zone_border_corner_tr = pygame.transform.rotate(zone_border_corner_tl, -90)
zone_border_corner_br = pygame.transform.rotate(zone_border_corner_tr, -90)
zone_border_corner_bl = pygame.transform.rotate(zone_border_corner_br, -90)