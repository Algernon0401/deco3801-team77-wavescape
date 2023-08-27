import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch


yolov5s = torch.hub.load("ultralytics/yolov5", "yolov5s")
# yolov5l = torch.hub.load("ultralytics/yolov5", "yolov5l")


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    results = trained_model(frame)
    cv2.imshow("webcam", np.squeeze(results.render()))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# !cd yolov5 && python train.py --batch 16 --epochs 3 --data config.yaml --weights yolov5s.pt --workers 2

trained_model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=r"\yolov5\runs\train\exp2\weights\last.pt",
    force_reload=True
)

import os
img = os.path.join('data', 'images', 'train', 'earbuds12.jpg')
results = trained_model(img)

%matplotlib inline
plt.imshow(np.squeeze(results.render()))
plt.show()


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        
find("last.pt",r"C:\vscode")
