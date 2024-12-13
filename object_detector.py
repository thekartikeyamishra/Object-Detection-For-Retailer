import torch
from PIL import Image
import numpy as np
import cv2

model = torch.hub.load("models/yolov5s.pt", "yolo5s", pretrained=True)


def detect_objects(image_path):
    image = Image.open(image_path)
    results = model(image)

    # convert image to Numpy array
    result_image = np.array(image)
    for *box, conf, cls, in results.xyxy[0].numpy():
        x1, y1, x2, y2 = map(int, box)
        label = f"{model.names[int(cls)]}{conf : .2f}"
        cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(result_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return result_image
