from datatorch import agent
from typing import List, Tuple
import requests

Point = Tuple[float, float]


def call_dextr(path: str, points: List[Point], address: str) -> List[Point]:
    agent_folder = agent.directories().root
    container_path = path.replace(agent_folder, "/agent")

    print(f"Sending request to '{address}' (POST)")
    print(f"Image Path = {path}")
    print(f"Container Path = {container_path}")
    print(f"Points = {points}")

    response = requests.post(address, json={"path": container_path, "points": points})
    print(response)
    return []
