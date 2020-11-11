import datatorch
import subprocess
import time
import sys
import os

from typing import List, cast
from client import call_dextr, Point


directory = os.path.dirname(os.path.abspath(__file__))
server_py = os.path.join(directory, "server.py")
print(server_py)


points = cast(List[Point], datatorch.get_inputs("points"))
image_path = cast(str, datatorch.get_inputs("imagePath"))
port = cast(str, datatorch.get_inputs("port"))

points: List[Point] = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0), (70.0, 80.0)]
image_path = "./"
port = "50052"


def valid_image_path():
    pass


def start_server():
    print("Spinning an instance up and trying again.")
    print("This may take a few seconds.")
    print(sys.executable)
    subprocess.Popen([sys.executable, server_py])
    time.sleep(5)


def send_request():
    attempts = 0

    while True:
        try:
            attempts += 1
            call_dextr(image_path, points, port=port)
            return
        except Exception as ex:
            if attempts > 5:
                print(ex)
                break
            print(f"Attemp: {attempts}")
            print("Could not connect to dextr.")
            start_server()

    print("Could not send request.")
    exit(1)


if __name__ == "__main__":
    valid_image_path()
    send_request()
