# Import OpenCV, Pygame, Numpy and Pytorch
import cv2 as cv
import pygame
import numpy as np
import torch
import threading
import os
from ..object import *
import time
from ultralytics import YOLO

ASSET_TRAINED_MODEL = os.path.abspath("assets/model.pt")
MODEL_CONFIDENCE_THRESHOLD = 0.5

class Camera:
    """
    This class represents the camera device that we will be using.
    At this point in time, this camera class only supports webcam
    feed (no depth camera).

    This class also handles object detection and recognition.

    OpenCV is required, and Torch is required for object recognition.
    """

    def __init__(self):
        """
        Creates a new camera device reference,
        which opens the camera for opencv and pygame use,
        and loads the given YOLOv5 model.
        """
        try:
            self.loading = True
            self.valid = False
            self.model = None
            self.model_loading = True
            self.model_results = None
            self.camera_no = 0
            self.has_model = os.path.isfile(ASSET_TRAINED_MODEL)
            # Create thread for opening camera and YOLO object detection
            threading.Thread(target=self.open_camera, args=[]).start()
            threading.Thread(target=self.load_default_model, args=[]).start()
        except:
            print("Error creating thread (camera thread/yolo thread)")
            self.valid = False
            self.loading = False

    def load_default_model(self):
        """
        Loads the default trained model if it exists.
        """
        self.load_yolo_model(ASSET_TRAINED_MODEL)

    def load_yolo_model(self, path):
        """
        Loads the YOLOv5 trained model into runtime.

        If self.has_model is set to False, then the
        path is ignored and YOLOv5s is loaded.

        Arguments:
            path -- the path that contains the trained model.
        """
        try:
            print("YOLOv8 Model Initialising...")
            if self.has_model:
                self.model = YOLO(ASSET_TRAINED_MODEL)
            else:
                self.model = YOLO("yolov8n.pt")

            print("YOLOv8 Model Initialised.")
            self.model_loading = False
            # Repeatedly get object detection results in this thread
            while self.model is not None:
                if self.valid:
                    # Update model results
                    self.model_results = self.model(
                        self.capture_video(), verbose=False
                    )[0]
                time.sleep(0.05)  # Ensure this does not clog up machine
        except Exception as e:
            print("Error with YOLOv5 Model.")
            self.model = None
            self.model_loading = False

    def open_camera(self):
        try:
            print("Camera initializing...")
            self.video = cv.VideoCapture(self.camera_no)
            # Ensure video camera is opened.
            self.valid = self.video.isOpened()
            print("Camera initialized.")
            self.loading = False
        except:
            print("Error initializing camera")
            self.valid = False
            self.loading = False

    def init_next_camera(self):
        """
        Creates a new thread to swap the next camera
        """
        self.valid = False
        self.loading = True
        self.video.release()
        self.video = None
        threading.Thread(target=self.next_camera, args=[]).start()
        

    def next_camera(self):
        """
        Initialises a new video feed from the next camera if possible, else
        resets to the first camera.
        """
        try:
            self.loading = True
            while self.valid:
                pass # Wait until main thread catches up
            self.camera_no += 1
            self.video = cv.VideoCapture(self.camera_no)

            # Ensure video camera is opened.
            self.valid = self.video.isOpened()
            self.loading = False
            if not self.valid:
                # Open initial camera
                self.open_camera()
        except:
            print("Error swapping camera")
            self.camera_no = 0 # Reset to first camera
            self.loading = False
            self.valid = False
            # Open initial camera
            self.open_camera()

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
        # Check to make sure camera and model is initialized.

        if not self.valid or self.model is None:
            # Set objects to empty list
            controller.set_cam_objects([])
            return

        objects = []

        cvframe = self.capture_video()

        # Get width and height of cvframe
        camera_x = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        camera_y = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)

        # Get scale of camera to screen
        (screen_x, screen_y) = controller.get_screen_size()
        (scale_x, scale_y) = (screen_x / camera_x, screen_y / camera_y)

        # Check to make sure feed is valid
        if cvframe is None:
            # Set objects to empty list
            controller.set_cam_objects([])
            return

        # Convert Object Detection results from model
        if self.model_results is not None:
            # loop over the detections
            for data in self.model_results.boxes.data.tolist():
                # extract the confidence (i.e., probability) associated with the detection
                confidence = data[4]

                # filter out weak detections by ensuring the
                # confidence is greater than the minimum confidence
                if float(confidence) < MODEL_CONFIDENCE_THRESHOLD:
                    continue

                # if the confidence is greater than the minimum confidence,
                # draw the bounding box on the frame
                screen_xmin = int(data[0])
                screen_xmax = int(data[2])
                screen_ymin = int(data[1])
                screen_ymax = int(data[3])
                tag = self.model_results.names[int(data[5])]

                # Adjust for scale
                screen_xmin *= scale_x
                screen_xmax *= scale_x
                screen_ymin *= scale_y
                screen_ymax *= scale_y

                # Create Camera Object
                objects.append(
                    CamObject(
                        tag,
                        (
                            screen_xmin,
                            screen_ymin,
                            screen_xmax - screen_xmin,
                            screen_ymax - screen_ymin,
                        ),
                    )
                )

        controller.set_cam_objects(objects)

    def destroy(self):
        """
        Releases the video capture reference and YOLO model
        """
        if self.valid:
            self.video.release()
        self.model = None
        self.valid = False
