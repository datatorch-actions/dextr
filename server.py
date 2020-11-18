from dextr.model import DextrModel

from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import time

from imantics import Mask


app = Flask(__name__)
model = DextrModel.pascalvoc_resunet101()


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

        mask = model.predict([image], [points])[0]
        polygons = Mask(mask).polygons().points
        polygons = [polygon.tolist() for polygon in polygons if len(polygon) > 2]
        print(f"Result: {polygons}", flush=True)

        end = time.time()
        process_time = end - start
        print(f"Process Time: {process_time:9.3} seconds", flush=True)

        return jsonify({"polygons": polygons})
    return "<h4>DEXTR Action is running.</h4>"


if __name__ == "__main__":
    app.run()
