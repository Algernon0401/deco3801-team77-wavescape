import cv2
import matplotlib.pyplot as plt
import numpy as np
import joblib
import torch


yolov5s = torch.hub.load("ultralytics/yolov5", "yolov5s")
yolov5l = torch.hub.load("ultralytics/yolov5", "yolov5l")


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    results = yolov5l(frame)
    cv2.imshow("webcam", np.squeeze(results.render()))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
