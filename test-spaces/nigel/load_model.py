import torch

trained_model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=r"yolov5_fork\runs\train\exp5\weights\best.pt",
    force_reload=True,
)
