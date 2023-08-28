import subprocess
import os

# Change the working directory to yolov5_fork
os.chdir("yolov5_fork")

command = [
    "python",
    "train.py",
    "--batch",
    "16",
    "--epochs",
    "500",  # stop operations once desired results achieved
    "--data",
    "config.yaml",
    "--weights",
    "yolov5s.pt",
    "--workers",
    "2",
]

# Run the actual command
subprocess.run(command)
