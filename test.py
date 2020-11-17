from dextr.model import DextrModel

from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

from imantics import Mask


app = Flask(__name__)
model = DextrModel.pascalvoc_resunet101()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        content = request.json
        image = Image.open(content["path"])
        points = np.array(content["points"])
        mask = model.predict([image], [points])[0]
        return jsonify({"segmentaiton": Mask(mask).polygons().segmentation})
    return "<h4>DEXTR Action is running.</h4>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", threaded=True, debug=True)
