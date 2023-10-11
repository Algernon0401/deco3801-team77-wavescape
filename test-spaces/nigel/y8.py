import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(r"shapes_dataset\y8\med_shapes_updated4\weights\best.pt")

# Open the video file
video_path = r"C:\Users\Forge-15 PRO\Videos\2023-10-10 17-43-49.mkv"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
