import subprocess

command = [
    "python",
    "train.py",
    "--batch",
    "16",
    "--epochs",
    "5",
    "--data",
    "config.yaml",
    "--weights",
    "yolov5s.pt",
    "--workers",
    "2",
]

# Change the working directory to yolov5_fork
subprocess.run(["cd", "yolov5_fork"], shell=True)

# Run the actual command
subprocess.run(command)
