import cv2
import numpy as np
from collections import defaultdict

from ultralytics import YOLO

# Load the YOLOv8 model
# model = YOLO(r"shapes_dataset\nano_shapes\weights\best.pt")
model = YOLO("yolov8n.pt")

# Open the video file
video_path = r"C:\Users\Forge-15 PRO\OneDrive\Pictures\Camera Roll\test.mp4"
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

print(cv2.__version__)

# Store the track history
track_histories = defaultdict(list)
track_averages = defaultdict(list)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
