from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    # Use the model
    model.info()
    results = model.train(
        data="config.yaml",
        imgsz=640,
        optimizer="Adam",
        batch=-1,
        epochs=500,
        device=0,
        project="y8",
        name="nano",
        exist_ok=True,
    )
