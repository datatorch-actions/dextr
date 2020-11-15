import requests


url = "http://localhost:8000"

requests.post(
    url,
    json={
        "image_path": "./image.jpg",
        "points": [[10, 20], [30, 40], [50, 60], [60, 70]],
    },
)
