# Import OpenCV, Pygame, Numpy and Pytorch
import cv2 as cv
import pygame
import numpy as np
import torch
import threading
from ..object import *


class Camera:
    """
    This class represents the camera device that we will be using.
    At this point in time, this camera class only supports webcam
    feed (no depth camera).

    OpenCV is required.
    """

    def __init__(self):
        """
        Creates a new camera device reference,
        which opens the camera for opencv and pygame use.
        """
        try:
            self.loading = True
            self.valid = False

            # Create thread for opening camera
            threading.Thread(target=self.open_camera, args=[]).start()
        except:
            print("Error creating thread (camera thread)")
            self.valid = False
            self.loading = False

    def open_camera(self):
        try:
            print("Camera initializing...")
            self.video = cv.VideoCapture(0)
            # Ensure video camera is opened.
            self.valid = self.video.isOpened()
            print("Camera initialized.")
            self.loading = False
        except:
            print("Error initializing camera")
            self.valid = False
            self.loading = False

    def capture_video(self):
        """
        Captures the standard webcam footage.
        """
        if self.valid:
            ret, frame = self.video.read()  # Get frame

            if not ret:
                self.destroy()  # Video cam error (or ended)

            return frame
        return None

    def capture_video_pygame(self) -> pygame.image:
        """
        Captures the standard webcam footage, as a pygame
        compatible image.
        """
        if self.valid:
            frame = self.capture_video()
            if frame is not None:
                # Convert to pygame image (current shape is (height,width))
                #                         (required shape is (width,height))
                return pygame.image.frombuffer(
                    frame.tobytes(), frame.shape[1::-1], "BGR"
                )
        return None

    def update(self, controller):
        """
        Updates by detecting the objects from the frame, outputting
        to the controller's object list.
        """
        # Check to make sure camera is initialized.
        if self.valid:
            return
        
        objects = []
        cvframe = self.capture_video()

        # Check to make sure feed is valid
        if cvframe is None:
            return

        (screenX, screenY) = controller.get_screen_size()

        controller.set_cam_objects(objects)

    def destroy(self):
        """
        Releases the video capture reference.
        """
        if self.valid:
            self.video.release()

        self.valid = False
        self.valid = False
