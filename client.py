from typing import List, Tuple, cast
import os
import grpc
from grpc import Channel
import dextr_pb2
import dextr_pb2_grpc
import numpy as np

Point = Tuple[float, float]


def points_to_segmentation(points: List[Point]) -> List[float]:
    """
    Converts from:
        [[[x1,y1], [x2,y2], ...]]
    to:
        [[x1,y1,x2,y2...]]
    """
    return np.array(points).flatten().tolist()


def segmentation_to_points(points: List[float]) -> List[Point]:
    """
    Converts from:
        [[x1,y1], [x2,y2], ...]
    to:
        [[x1,y1,x2,y2...]]
    """
    return np.reshape(points, (-1, 2)).tolist()


def send_request(channel: Channel, image_path: str, segmentation: List[float]):
    stub = dextr_pb2_grpc.RouteStub(channel)
    points_grpc = dextr_pb2.Points(points=segmentation)
    request = dextr_pb2.Request(image=os.path.abspath(image_path), points=points_grpc)
    return stub.Predict(request)


def call_dextr(image_path: str, points: List[Point], port="50052") -> List[Point]:
    segmentation = points_to_segmentation(points)
    path_abs = os.path.abspath(image_path)
    address = f"localhost:{port}"

    print(f"Sending request to '{address}' (grpc)")
    print(f"Image Path = {path_abs}")
    print(f"Points = {segmentation}")

    with grpc.insecure_channel(address) as channel:
        response = send_request(channel, path_abs, segmentation)

    return segmentation_to_points(response.points)
