# DECO3801 - The WaveScape
Design & Developed by Students at UQ (DECO3801):
Samuel Sticklen, Chia (Nigel) Yunhan, Luke Pierce, Yiqing (Samson) Zhang, Miles Gardiner, William Redmond

## How to Run the Software
### Via App-Launcher
For your convencience, an AppLauncher.exe has been provided. 
This launcher is coded with the .NET framework, in which you may be prompted to install it.
Afterwards, the app should run, otherwise attempt a manual (python) launch.

### Requirements
Run all of the following commands to install the requirements IN ORDER
```
python -m pip install opencv-python==4.8.0.76
python -m pip install pygame
python -m pip install pygame-ce --upgrade
python -m pip install -r https://raw.githubusercontent.com/ultralytics/ultralytics/main/requirements.txt
python -m pip install numpy numba scipy 
python -m pip install pyserial
```

In order for all functionality, you must 
- Have a working webcam
- Have the original board developed with the app (Board Error might occur otherwise)
- Have a suitable surface to project on, and a suitable mount for both projector and camera
You may require a camera setting app, such as Logitech Camera Settings to adjust settings for the camera to make
the detection more compatible.

### App Options
```
Flag            | Description
-np               Removes the need for a plus object to be placed on the checkbox next to a zone (arrangement cannot be used)
-feed             Displays a semi-transparent view of what the model sees (non-toggleable).
                  Only applicable with -test.
-test             Adds the test control, which allows for placement of objects, keys z for undo, b for button.
-nodark           Removes the black and white filter, which may work better for some environments.
-nocameraerror    Removes the status display for the camera error
-nomodelerror     Removes the status display for the model error
-noboarderror     Removes the status display for the board error
```
# Issues that may occur
If you an error like the following: 
```
Cannot find serial.Serial
```
Uninstall pyserial and serial, and reinstall pyserial on the correct python.
Other issues and fixes include:
```
- Board Status Error - reconnect board and check you are using the correct board (only one exists with our group)
- Camera Status Error - reconnect camera and either restart the app or attempt the swap camera button in the menu
- Model Status Error - ensure model.pt exists in the assets folder and that it is the correct model
- Cannot find 'assets/...' - you must run app.py using the app folder as the current working directory.
```
=======
