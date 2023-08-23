import cv2
import matplotlib.pyplot as plt
import numpy as np
import joblib
from mypackage import thing1


yolov5s = r"yolov5s.joblib"
yolov5l = r"yolov5l.joblib"
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# joblib.dump(model, filename)
loaded_model = joblib.load(yolov5l)


img = "https://ultralytics.com/images/zidane.jpg"
result = loaded_model(img)
result.pandas().xyxy[0]

plt.imshow(np.squeeze(result.render()))
plt.show()
