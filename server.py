from dextr.model import DextrModel

from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import time
import torch
import os

from imantics import Mask

device = os.getenv("DEVICE", "cpu")
torch_device = torch.device(device)

app = Flask(__name__)
model = DextrModel.pascalvoc_resunet101()
model.eval()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        start = time.time()
        content = request.json

        path = content["path"]
        points = np.array(content["points"])

        print(f"Processing Image: {path}")
        image = Image.open(path)
        print(f"Image Size: {image.size}", flush=True)

        # points come in [x,y] order; this must be flipped
        points = points[:, ::-1]
        mask = model.predict([image], [points])[0]
        mask_bin = mask >= 0.5
        polygons = Mask(mask_bin).polygons().points
        polygons = [polygon.tolist() for polygon in polygons if len(polygon) > 2]
        print(f"Result: {polygons}", flush=True)

        end = time.time()
        process_time = end - start
        print(f"Process Time: {process_time:9.3} seconds", flush=True)

        return jsonify({"polygons": polygons})
    return "<h4>DEXTR Action is running.</h4>"


if __name__ == "__main__":
    app.run()
