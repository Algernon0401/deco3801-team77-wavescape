import cv2 as cv  # Import the OpenCV library with the alias "cv"

# Initialize webcam capture. Change the argument (0) if you have multiple cameras.
cap = cv.VideoCapture(0)

# Enter a loop to continuously capture and display frames from the webcam
while cap.isOpened():
    # Read the next frame from the webcam. 'ret' indicates success, 'frame' holds the image data.
    ret, frame = cap.read()

    # Display the captured frame in a window titled "webcam"
    cv.imshow("webcam", frame)

    # Wait for a key press for 1 millisecond and check if the key is 'q' (quit)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break  # Exit the loop if 'q' is pressed

# Release the webcam and free up system resources
cap.release()

# Close all OpenCV windows
cv.destroyAllWindows()
