import subprocess
import os

# import comet_ml

# export comet_ml.COMET_API_KEY="upZUpr8CUHd8eKdCb5eoPXjdp"  # 2. paste API key

# Change the working directory to yolov5_fork
os.chdir("yolov5_fork")

# can exit training by trashing terminal
command = [
    "python",
    "train.py",
    "--batch",
    "8",
    "--epochs",
    "100",
    "--data",
    "config.yaml",
    "--weights",
    "yolov5n.pt",
]

# resume training if previously stopped. continues from latest file update
resume_command = ["python", "train.py", "--resume"]

# Run the actual command
subprocess.run(resume_command)
