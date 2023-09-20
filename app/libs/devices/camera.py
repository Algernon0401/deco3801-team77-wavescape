# Import OpenCV, Pygame, Numpy and Pytorch
import datetime
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
CAMERA_UPDATE_DELAY = 0.1  # Number of seconds until camera is allowed to update again.


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
            self.active = True
            self.loading = True
            self.valid = False
            self.model = None
            self.model_loading = True
            self.refresh_ready = False
            self.model_results = None
            self.object_results = None
            self.camera_no = 0
            self.offset_x = 0  # To be calibrated
            self.offset_y = 0  # To be calibrated
            self.scale_x = 1  # To be calibrated
            self.scale_y = 1  # To be calibrated
            self.has_model = os.path.isfile(ASSET_TRAINED_MODEL)
            self.last_time_updated = datetime.datetime.now()
            self.current_update = 0  # Alternates between 0 and 1
            # Create thread for opening camera and YOLO object detection
            threading.Thread(target=self.open_camera, args=[]).start()
            threading.Thread(target=self.load_default_model, args=[]).start()
            # Create thread for object conversion
            threading.Thread(target=self.object_conversion, args=[]).start()
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
                    self.model_results = self.model.track(
                        self.capture_video(), verbose=False, persist=True
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
        self.object_results = None
        if self.video is not None:
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
                pass  # Wait until main thread catches up
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
            self.camera_no = 0  # Reset to first camera
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

    def display_to_screen(self, controller, screen: pygame.Surface):
        """
        Displays the camera to the screen (full-screen), with the given
        calibration settings.
        """

        frame = self.capture_video_pygame()
        (screen_w, screen_h) = controller.get_screen_size()
        if frame is not None:
            # Find camera dimensions and offset
            camera_w = screen_w * self.scale_x
            camera_h = screen_h * self.scale_y

            camera_x = screen_w / 2 - (camera_w * (1 - self.offset_x) / 2)
            camera_y = screen_h / 2 - (camera_h * (1 - self.offset_y) / 2)

            screen.blit(
                pygame.transform.scale(frame, (camera_w, camera_h)),
                (camera_x, camera_y),
            )

    def object_conversion(self):
        """
        Continuously converts model results into usable camera objects.
        (to be run in another thread - see __init__)
        """

        while self.active:
            time.sleep(0.1)  # Only update 50ms or so to prevent computer lag

            if not self.valid or self.model is None:
                # Set objects to empty list
                self.object_results = []
                continue  # Continue to next iteration

            objects = []

            # NOTE Sam to Nigel - copy your code here (update objects)

            # Uncomment below line when implemented.
            # self.object_results = objects
            self.refresh_ready = True

    def update(self, controller):
        """
        Updates by detecting the objects from the frame, outputting
        to the controller's object list.
        """
        # Check to make sure camera and model is initialized.
        time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        if (
            not self.refresh_ready or time_passed < CAMERA_UPDATE_DELAY
        ):  # Only update every 100ms
            # Ensure that we do not continuously lag the python app
            # when the video feed has not updated.
            if self.object_results is not None:
                controller.set_cam_objects(self.object_results.copy())
            return

        self.last_time_updated = datetime.datetime.now()
        self.refresh_ready = False
        self.current_update = 1 - self.current_update

        # Update camera objects to given results from conversion thread.
        if self.object_results is not None:
            controller.set_cam_objects(self.object_results.copy())

        # NOTE from Sam to Nigel -- I'm not too sure of your changes to this class, so
        # I'm going to leave you to change self.object_results to the correct value (objects).
        # Please move code from update to object_conversion which is run in another thread
        # for optimization.

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

        self.object_results = objects

    def destroy(self):
        """
        Releases the video capture reference and YOLO model
        """
        self.active = False
        if self.valid:
            self.video.release()
        self.model = None
        self.valid = False
