from ultralytics import YOLO
from PIL import Image

# Load a pretrained YOLOv8n model
model = YOLO(r"shapes_dataset\y8\med_shapes_updated4\weights\best.pt")

# Run inference on an image
results = model(
    r"C:\vscode\DECO3801\deco3801-team77\test-spaces\nigel\shapes_dataset\dataset2\valid\images\Screenshot-2023-10-10-17-41-12_png.rf.065dbde197dc62578aa16b5c06efa8bc.jpg"
)  # results list

# View results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save("results.jpg")  # save image
