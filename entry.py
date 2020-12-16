from datatorch import get_input, agent, set_output
from datatorch.api.api import ApiClient
from datatorch.api.entity.sources.image import Segmentations
from datatorch.api.entity.sources import Source
from datatorch.api.scripts.utils.simplify import simplify_points

import requests
import docker
import time
import os

from typing import List, Tuple
from docker.models.resource import Model
from urllib.parse import urlparse


Point = Tuple[float, float]


directory = os.path.dirname(os.path.abspath(__file__))

agent_dir = agent.directories().root
points = get_input("points")
image_path = get_input("imagePath")
address = urlparse(get_input("url"))
image = get_input("image")
annotation = get_input("annotation")
annotation_id = get_input("annotation.id")
simplify = get_input("simplify")

# [[10,20],[30, 40],[50,60],[70,80]]
# points: List[Point] = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0), (70.0, 80.0)]
# image_path = "/home/desktop/.config/datatorch/agent/temp/download-file/20201025_102443 (17th copy).jpg"


CONTAINER_NAME = "datatorch-dextr-action"


def valid_image_path():
    if not image_path.startswith(agent_dir):
        print(f"Directory must be inside the agent folder ({agent_dir}).")
        exit(1)

    if not os.path.isfile(image_path):
        print(f"Image path must be a file ({image_path}).")
        exit(1)


def start_server(port: int):
    docker_client = docker.from_env()
    print(f"Creating DEXTR container on port {port}.")
    print(f"Downloading {image} docker image. This may take a few mins.", flush=True)
    container = docker_client.containers.run(
        image,
        detach=True,
        ports={"8000/tcp": port},
        restart_policy={"Name": "always"},
        volumes={agent_dir: {"bind": "/agent", "mode": "rw"}},
    )
    if isinstance(container, Model):
        print(f"Created DEXTR Container ({container.short_id}).")


def call_dextr(path: str, points: List[Point], address: str) -> List[List[Point]]:
    agent_folder = agent.directories().root
    container_path = path.replace(agent_folder, "/agent")

    print(f"Sending request to '{address}' (POST)")
    print(f"Image Path = {path}")
    print(f"Container Path = {container_path}")
    print(f"Points = {points}")

    response = requests.post(address, json={"path": container_path, "points": points})
    json = response.json()
    print(f"Response = {json}")
    return json["polygons"]


def send_request():
    attempts = 0

    while True:
        try:
            attempts += 1
            print(f"Attempt {attempts}: Request to DEXTR Server")
            seg = call_dextr(image_path, points, address.geturl())
            output_seg = (
                seg
                if simplify == 0
                else [
                    simplify_points(polygon, tolerance=simplify, highestQuality=False)
                    for polygon in seg
                ]
            )
            set_output("polygons", output_seg)
            print(annotation_id)
            existing_segmentation = next(x for x in annotation.sources if x.type = "segmentation")
            if existing_segmentation
                print(f"Updating segmentation for annotation {annotation_id}")
                existing_segmentation.path_data = output_seg + existing_segmentation.path_data 
                existing_segmentation.update(ApiClient(), id)
            else if annotation_id is not None:
                print(f"Creating segmentation source for annotation {annotation_id}")
                s = Segmentations()
                s.annotation_id = annotation_id
                s.path_data = output_seg
                s.create(ApiClient())
            exit(0)
        except Exception as ex:
            if attempts > 5:
                print(ex)
                break
            print(f"Attempt {attempts}: Could not connect to dextr.")
            start_server(address.port or 80)
            time.sleep(5)

    print("Could not send request.")
    exit(1)


if __name__ == "__main__":
    valid_image_path()
    send_request()
