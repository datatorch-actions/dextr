from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

# from imantics import Mask

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        content = request.json
        image = Image.open(content["path"])
        print(image.width)
        points = np.array(content["points"])
        print(points)

        # { "segmentaiton": Mask(result).polygons().segmentation }
        return jsonify({"hello": True})
    return "<h4>DEXTR Action is running.</h4>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", threaded=True, debug=True)
