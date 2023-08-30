import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

trained_model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="yolov5_fork/runs/train/exp18/weights/last.pt",  # exp4 holds latest training sequence.
    force_reload=True,
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    results = trained_model(frame)
    cv2.imshow("webcam", np.squeeze(results.render()))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ----to do list----
# remove coins... done
# removee card?
# add more gear, star, angle, triangle
# add more variety of wallet
# run longer
# more variety of earbuds
# more watches
# add more individual keys?
