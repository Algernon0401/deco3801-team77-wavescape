from ultralytics import YOLO
from sklearn.model_selection import KFold

# if __name__ == "__main__":
#     # Load a model
#     model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
#     # Use the model
#     model.info()
#     results = model.train(
#         data="config.yaml",
#         imgsz=640,
#         optimizer="Adam",
#         batch=-1,
#         epochs=500,
#         device=0,
#         project="y8",
#         name="nano2",
#         exist_ok=True,
#     )

#     # model = YOLO(r"y8\large\weights\best.pt")
#     # results = model.train(resume=True)

if __name__ == "__main__":
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    # Use the model

    ksplit = 5
    kf = KFold(
        n_splits=ksplit, shuffle=True, random_state=20
    )  # setting random_state for repeatable results
    ds_yamls = [
        r"datasets\full\2023-09-06_5-Fold_Cross-val\split_1\split_1_dataset.yaml",
        r"datasets\full\2023-09-06_5-Fold_Cross-val\split_2\split_2_dataset.yaml",
        r"datasets\full\2023-09-06_5-Fold_Cross-val\split_3\split_3_dataset.yaml",
        r"datasets\full\2023-09-06_5-Fold_Cross-val\split_4\split_4_dataset.yaml",
        r"datasets\full\2023-09-06_5-Fold_Cross-val\split_5\split_5_dataset.yaml",
    ]

    model.info()
    results = {}
    for k in range(ksplit):
        dataset_yaml = ds_yamls[k]
        model.train(
            data=dataset_yaml,
            imgsz=640,
            optimizer="Adam",
            batch=-1,
            epochs=200,
            patience=30,
            device=0,
            project="y8",
            name="nano_w_kfold",
            exist_ok=True,
        )  # Include any training arguments
        results[k] = model.metrics  # save output metrics for further analysis
