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
        results = model.track(frame, iou=0.1, verbose=False, persist=True)

        # Get the boxes and track IDs
        data_output = results[0].boxes.data.tolist()
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track_history = track_histories[track_id]
            track_history.append((float(x), float(y)))  # x, y center point
            if len(track_history) > 10:
                track_history.pop(0)

        for track_id, track in track_histories.items():
            total_x = sum(coord[0] for coord in track)
            total_y = sum(coord[1] for coord in track)
            avg_center_x = total_x / len(track_histories[track_id])
            avg_center_y = total_y / len(track_histories[track_id])

            # create key with track_id in track_average,
            # to store the average center coord associated with the track_id
            track_avg = track_averages[track_id]
            track_avg.append((float(avg_center_x), float(avg_center_y)))

            # stores only the latest 10 average coord
            # removes previous entry
            if len(track_avg) > 5:
                track_avg.pop(0)

            # Draw the tracking lines
            points = np.hstack(track_avg).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(
                annotated_frame,
                [points],
                isClosed=False,
                color=(230, 230, 230),
                thickness=10,
            )

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
