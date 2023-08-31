import subprocess
import os

# Change the working directory to yolov5_fork
os.chdir("yolov5_fork")

# can exit training by trashing terminal
train_command = [
    "python",
    "train.py",
    "--img",
    "640",
    "--batch",
    "4",
    "--epochs",
    "500",
    "--data",
    "config.yaml",
    "--weights",
    "yolov5s.pt",  # or path/to/last.pt
]

# resume training if previously stopped. continues from latest file update
resume_command = ["python", "train.py", "--resume"]

continue_command = ["python", "train.py", "--weights", ""]

test_command = [
    "python",
    "val.py",
    "--weights",
    r"runs\train\exp\weights\best.pt",
    "--data",
    "config.yaml",
]


# Run the actual command
subprocess.run(test_command)
