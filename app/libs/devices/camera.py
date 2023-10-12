# Import OpenCV, Pygame, Numpy and Pytorch
import datetime
import cv2 as cv
import pygame
import numpy as np

# import torch
import threading
import os
from ..object import *
import time
from multiprocessing import Process, Queue, Manager
from ultralytics import YOLO
from collections import defaultdict
from ..mp import Message

ASSET_TRAINED_MODEL = os.path.abspath("assets/model.pt")
MODEL_CONFIDENCE_THRESHOLD = 0.5
CAMERA_UPDATE_DELAY = 0.1  # Number of seconds until camera is allowed to update again.
MAX_ITEMS_IN_MP_QUEUE = (
    3  # Number of items that can be queued until results are forcibly popped.
)

MP_MSG_YOLO_ERROR = 0
MP_MSG_YOLO_MODEL_LOADED = 1

MP_MSG_QUIT = 100


class CameraQueueManager:
    """
    Wrapper for the four camera/yolo queues.
    """

    def __init__(self):
        """
        Initialises the four camera/yolo queues.
        """
        self.camera_feed_queue = Manager().Queue(1)  # Sending camera feed to YOLO
        self.object_detection_queue = Manager().Queue(
            5
        )  # Sending object results to main process
        self.message_camera_queue = Manager().Queue(5)  # From camera to yolo
        self.message_yolo_queue = Manager().Queue(5)  # From yolo to camera


queues = None


def load_yolo_model(path):
    """
    Loads the YOLOv8 trained model into runtime.

    If self.has_model is set to False, then the
    path is ignored and YOLOv8n is loaded.

    Arguments:
        path -- the path that contains the trained model.
    """
    global queues
    try:
        print("YOLOv8 Model Initialising...")

        # Load the model from a file
        model = None
        if path is not None:
            model = YOLO(ASSET_TRAINED_MODEL)
        else:
            model = YOLO("yolov8n.pt")

        print("YOLOv8 Model Initialised.")

        # Tell main process that yolo was successfully initialised
        queues.message_yolo_queue.put(Message(MP_MSG_YOLO_MODEL_LOADED))

        camera_feed = None
        # Repeatedly get object detection results in this thread
        while True:
            # Process messages from main thread
            while queues.message_camera_queue.qsize() > 0:
                msg = queues.message_camera_queue.get()
                if msg.type == MP_MSG_QUIT:
                    return

            # Get feed from main thread
            if queues.camera_feed_queue.qsize() > 0:
                camera_feed = queues.camera_feed_queue.get()

            # Process feed
            if camera_feed is not None:
                if queues.object_detection_queue.qsize() >= MAX_ITEMS_IN_MP_QUEUE:
                    queues.object_detection_queue.get()

                # Send new model results to queue
                queues.object_detection_queue.put(
                    model.track(camera_feed, verbose=False, persist=True)[0]
                )
            time.sleep(0.05)  # Ensure model attempts to run less than 20x a second
    except Exception as e:
        print("Error with YOLOv8 Model: " + str(e))
        queues.message_yolo_queue.put(Message(MP_MSG_YOLO_ERROR, None))


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
        global queues
        try:
            queues = CameraQueueManager()
            self.active = True
            self.loading = True
            self.valid = False
            self.model = None
            self.model_loading = True
            self.refresh_ready = True
            self.model_results = None
            self.object_results = []
            self.camera_no = 0
            
            # X and Y offsets for center object (as perc of screen)
            self.offset_x = 0 
            self.offset_y = 0
            # X and Y resizing for every object (perc of object)
            self.scale_x = 1 
            self.scale_y = 1
            # X and Y skewing (perc of half-screen)
            # e.g. a Y top skew of 1, means that the difference from the
            # center to the top is doubled in offset.
            self.skew_top = 0
            self.skew_bottom = 0
            self.skew_left = 0
            self.skew_right = 0
            
            self.has_model = os.path.isfile(ASSET_TRAINED_MODEL)
            self.last_time_updated = datetime.datetime.now()
            self.current_update = 0  # Alternates between 0 and 1
            self.w = 1920
            self.h = 1080

            # Create thread for opening camera (debug and calibration use only)
            threading.Thread(target=self.open_camera, args=[]).start()

            # Create sub-process for processing camera via YOLO.
            Process(target=self.load_default_model, args=(queues,)).start()

            # Create thread for transferring camera feed to yolo model
            threading.Thread(target=self.feed_camera_to_yolo, args=[]).start()

            # Create thread for object conversion from yolo results
            threading.Thread(target=self.object_conversion, args=[]).start()

        except:
            print("Error creating thread (camera thread and/or YOLO thread)")
            self.valid = False
            self.loading = False

    def feed_camera_to_yolo(self):
        """
        Feeds the camera data to the YOLO sub-process.
        """
        global queues
        if queues.camera_feed_queue.qsize() == 0:
            queues.camera_feed_queue.put(self.capture_video())

    def load_default_model(self, cross_process_queues):
        """
        Loads the default trained model if it exists.

        Arguments:
            path -- the path that contains the trained model.
        """
        global queues
        queues = cross_process_queues
        model_path = ASSET_TRAINED_MODEL
        if not self.has_model:
            model_path = None
        load_yolo_model(model_path)
        return
        try:
            print("YOLOv8 Model Initialising...")
            if self.has_model:
                # self.model = YOLO(ASSET_TRAINED_MODEL)
                self.model = YOLO("yolov8n.pt")
            else:
                self.model = YOLO("yolov8n.pt")

            print("YOLOv8 Model Initialised.")
            self.model_loading = False
            # Repeatedly get object detection results in this thread
            while self.model is not None:
                if self.valid:
                    # Update model results
                    self.model_results = self.model.track(
                        self.capture_video(), verbose=0, persist=True
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
            self.valid = self.video is None or self.video.isOpened()
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
            self.valid = self.video is None or self.video.isOpened()
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

    def old_object_conversion(self):
        """
        Continuously converts model results into usable camera objects.
        (to be run in another thread - see __init__)
        """

        registered_results = {}
        all_track_ids = []

        while self.active:
            time.sleep(0.1)  # Only update 50ms or so to prevent computer lag

            if not self.valid or self.model is None:
                # Set objects to empty list
                self.object_results = []
                continue  # Continue to next iteration

            objects = []
            old_results = self.object_results
            cvframe = self.capture_video()

            # Get width and height of cvframe
            if self.video is None:
                return

            camera_x = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
            camera_y = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)

            if camera_x <= 0 and camera_y <= 0:
                return

            # Get scale of camera to screen
            (screen_x, screen_y) = (self.w, self.h)
            (scale_x, scale_y) = (screen_x / camera_x, screen_y / camera_y)

            # Check to make sure feed is valid
            if cvframe is None:
                # Set objects to empty list
                self.object_results = []
                return

            # Extract model results from queue
            if queues.object_detection_queue.qsize() > 0:
                self.model_results = queues.object_detection_queue.get()
                self.model_loading = False

            # Convert Object Detection results from model
            if self.model_results is not None:
                # loop over the detections
                try:
                    track_ids = self.model_results.boxes.id.int().cpu().tolist()
                    for data, track_id in zip(
                        self.model_results.boxes.data.tolist(), track_ids
                    ):
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
                        old_object_found = False
                        if track_id in all_track_ids:
                            # Keep old object with new object
                            obj = registered_results[track_id]
                            obj.x = screen_xmin
                            old_object_found = True
                            obj.y = screen_ymin
                            obj.w = screen_xmax - screen_xmin
                            obj.h = screen_ymax - screen_ymin
                            obj.date_last_included = datetime.datetime.now()
                            objects.append(obj)
                            break

                        if not old_object_found:
                            # Create new object with track_id
                            new_object = CamObject(
                                tag,
                                (
                                    screen_xmin,
                                    screen_ymin,
                                    screen_xmax - screen_xmin,
                                    screen_ymax - screen_ymin,
                                ),
                                track_id,
                            )

                            registered_results[track_id] = new_object
                            all_track_ids.append(track_id)

                            objects.append(new_object)
                except:
                    print("Error;303 camera.py")

            self.object_results = objects
            self.refresh_ready = True

    def object_conversion(self):
        """
        nigel test object_conversion
        """
        global queues
        # Initialize the dictionaries
        track_histories = defaultdict(list)
        track_averages = defaultdict(list)
        registered_results = {}

        while self.active:
            time.sleep(0.1)  # Only update 50ms or so to prevent computer lag

            if not self.valid or self.model is None:
                # Set objects to empty list
                self.object_results = []
                continue  # Continue to next iteration

            objects = []
            old_results = self.object_results
            cvframe = self.capture_video()

            # Get width and height of cvframe
            if self.video is None:
                continue

            camera_x = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
            camera_y = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)

            if camera_x <= 0 and camera_y <= 0:
                continue

            # Get scale of camera to screen
            (screen_x, screen_y) = (self.w, self.h)
            (scale_x, scale_y) = (screen_x / camera_x, screen_y / camera_y)

            # Check to make sure feed is valid
            if cvframe is None:
                # Set objects to empty list
                self.object_results = []
                continue

            # Extract model results from queue
            if queues.object_detection_queue.qsize() > 0:
                self.model_results = queues.object_detection_queue.get()

            # Convert Object Detection results from model
            if self.model_results is not None:
                # loop over the detections
                try:
                    results = self.model_results.boxes.data.tolist()

                    for data in results:
                        confidence = data[5]
                        # filter out weak detections by ensuring the
                        # confidence is greater than the minimum confidence
                        if float(confidence) < MODEL_CONFIDENCE_THRESHOLD:
                            continue

                        # if the confidence is greater than the minimum confidence,
                        # assign track_id
                        track_id = int(data[4])

                        # draw the bounding box on the frame
                        xmin = int(data[0])
                        ymin = int(data[1])
                        xmax = int(data[2])
                        ymax = int(data[3])
                        tag = self.model_results.names[int(data[6])]

                        # Adjust for scale
                        xmin *= scale_x
                        xmax *= scale_x
                        ymin *= scale_y
                        ymax *= scale_y

                        
                        # Apply calibration settings (center offset)
                        adj_x = screen_x * self.offset_x
                        adj_y = screen_y * self.offset_y
                        xmin += adj_x
                        ymin += adj_y
                        xmax += adj_x
                        ymax += adj_y
                        
                        # Apply calibration settings (resize)
                        obj_w = xmax - xmin
                        obj_h = ymax - ymin
                        
                        new_w = obj_w * self.scale_x
                        new_h = obj_h * self.scale_y
                        
                        diff_w = new_w - obj_w
                        diff_h = new_h - obj_h
                        xmin -= diff_w / 2
                        ymin -= diff_h / 2
                        xmax += diff_w / 2
                        ymax += diff_h / 2
                        
                        # Apply calibration settings (skew)
                        center_x = (xmin + xmax) / 2
                        center_y = (ymin + ymax) / 2
                        offset_x = 0
                        offset_y = 0
                        if center_x + 8 < screen_x / 2:
                            offset_x -= self.skew_left * (center_x - screen_x / 2)
                        if center_x - 8 > screen_x / 2:
                            offset_x += self.skew_right * (screen_x - center_x)
                        if center_y + 8 < screen_y / 2:
                            offset_y -= self.skew_top * (center_y - screen_y / 2)
                        if center_y - 8 > screen_y / 2:
                            offset_y += self.skew_bottom * (screen_y - center_y)
                        xmin += offset_x
                        xmax += offset_x
                        ymin += offset_y
                        ymax += offset_y

                        width = xmax - xmin
                        height = ymax - ymin

                        # create key with track_id in track_histories,
                        # to store bottom left(BL) coords associated with the track_id
                        track_hist = track_histories[track_id]
                        track_hist.append(
                            (float(xmin), float(ymin), float(width), float(height))
                        )

                        # stores the latest 30 coords, removes earliest entry
                        if len(track_hist) > 5:
                            track_hist.pop(0)

                        # Create Camera Object
                        old_object_found = False
                        if track_id in list(registered_results.keys()):
                            # Keep old object with new object
                            old_object_found = True
                            obj = registered_results[track_id]
                            latest_average = track_averages[track_id][-1]
                            obj.x = latest_average[0]
                            obj.y = latest_average[1]
                            obj.w = latest_average[
                                2
                            ]  # not sure what to assign, average it as well?
                            obj.h = latest_average[
                                3
                            ]  # not sure what to assign, average it as well?
                            obj.date_last_included = datetime.datetime.now()
                            objects.append(obj)
                            continue

                        if not old_object_found:
                            # Create new object with track_id
                            new_object = CamObject(
                                tag,
                                (
                                    xmin,
                                    ymin,
                                    xmax - xmin,
                                    ymax - ymin,
                                ),
                                track_id,
                            )

                            registered_results[track_id] = new_object

                            objects.append(new_object)

                        # loop over all store bottom left(BL) coords for track_id
                    for track_id, track in track_histories.items():
                        total_x = sum(coord[0] for coord in track)
                        total_y = sum(coord[1] for coord in track)
                        total_width = sum(coord[2] for coord in track)
                        total_height = sum(coord[3] for coord in track)

                        avg_x = total_x / len(track_histories[track_id])
                        avg_y = total_y / len(track_histories[track_id])
                        avg_width = total_width / len(track_histories[track_id])
                        avg_height = total_height / len(track_histories[track_id])

                        # create key with track_id in track_average, to store
                        # the average bottom left(BL) coord associated with the track_id
                        track_avg = track_averages[track_id]
                        track_avg.append(
                            (
                                float(avg_x),
                                float(avg_y),
                                float(avg_width),
                                float(avg_height),
                            )
                        )

                        # stores the latest 10 average coord
                        # removes earliest entry
                        if len(track_avg) > 10:
                            track_avg.pop(0)

                        # to be implemented:
                        # comparison of current track_avg to newest entry
                        # if  difference is +-10% then swap to new average
                        # to combat jitteryness
                except:
                    print("Error;303 camera.py")

            self.object_results = objects
            self.refresh_ready = True

    def update(self, controller):
        """
        Updates by detecting the objects from the frame, outputting
        to the controller's object list.
        """
        global queues
        # Check to make sure camera and model is initialized.
        time_passed = (datetime.datetime.now() - self.last_time_updated).total_seconds()
        (self.w, self.h) = controller.get_screen_size()

        # Process YOLO message events
        while queues.message_yolo_queue.qsize() > 0:
            msg = queues.message_yolo_queue.get()
            if msg.type == MP_MSG_YOLO_ERROR:
                self.model = None
                self.model_loading = False
            elif msg.type == MP_MSG_YOLO_MODEL_LOADED:
                self.model = msg.data
                self.model_loading = False

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

        self.feed_camera_to_yolo()

        # Update camera objects to given results from conversion thread.
        if self.object_results is not None:
            controller.set_cam_objects(self.object_results.copy())

    def destroy(self):
        """
        Releases the video capture reference and YOLO model
        """
        global queues
        self.active = False
        if self.valid:
            self.video.release()
        self.model = None
        self.valid = False
        queues.message_camera_queue.put(Message(MP_MSG_QUIT, 0))
