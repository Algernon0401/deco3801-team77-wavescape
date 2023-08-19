# Import OpenCV
# import cv2 as cv

class Camera():
    """
        This class represents the camera device that we will be using.
        At this point in time, this camera class only supports webcam
        feed (no depth camera).
        
        OpenCV is required.
    """
    
    def __init__(self):
        """
            Creates a new camera device reference.
        """
        
