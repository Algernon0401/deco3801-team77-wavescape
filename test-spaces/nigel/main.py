import cv2
import matplotlib.pyplot as plt
import numpy as np
import joblib


yolov5s = r"yolov5s.joblib"
yolov5l = r"yolov5l.joblib"
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# joblib.dump(model, filename)
loaded_model = joblib.load(yolov5l)


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    results = loaded_model(frame)
    cv2.imshow("webcam", np.squeeze(results.render()))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
