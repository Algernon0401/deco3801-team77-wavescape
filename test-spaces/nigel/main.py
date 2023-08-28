import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch

cap = cv2.VideoCapture(0)

trained_model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=r"yolov5_fork\runs\train\exp5\weights\best.pt",
    force_reload=True,
)

while cap.isOpened():
    ret, frame = cap.read()

    results = trained_model(frame)
    cv2.imshow("webcam", np.squeeze(results.render()))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
