from ultralytics import YOLO
import os

if __name__ == "__main__":
    # Use the model
    split_1_yaml = os.path.abspath(
        r"datasets/dataset/dataset_5_Fold_Cross_val/split_1/split_1_dataset.yaml"
    )
    split_2_yaml = os.path.abspath(
        r"datasets/dataset/dataset_5_Fold_Cross_val/split_2/split_2_dataset.yaml"
    )
    split_3_yaml = os.path.abspath(
        r"datasets/dataset/dataset_5_Fold_Cross_val/split_3/split_3_dataset.yaml"
    )
    split_4_yaml = os.path.abspath(
        r"datasets/dataset/dataset_5_Fold_Cross_val/split_4/split_4_dataset.yaml"
    )
    split_5_yaml = os.path.abspath(
        r"datasets/dataset/dataset_5_Fold_Cross_val/split_5/split_5_dataset.yaml"
    )

    ksplit = range(5)
    ds_yamls = [split_1_yaml, split_2_yaml, split_3_yaml, split_4_yaml, split_5_yaml]

    results = {}
    for k in range(ksplit):
        dataset_yaml = ds_yamls[k]
        # Load a model
        model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
        model.train(
            data=dataset_yaml,
            imgsz=640,
            optimizer="Adam",
            batch=-1,
            epochs=500,
            patience=50,
            device=0,
            project="y8_nano_kfold",
            name=f"{k} fold",
            exist_ok=True,
        )  # Include any training arguments
        results[k] = model.metrics  # save output metrics for further analysis
