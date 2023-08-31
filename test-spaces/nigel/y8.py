from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

if __name__ == "__main__":
    # Use the model
    results = model.train(data="coco128.yaml", epochs=50, device=0)  # train the model
