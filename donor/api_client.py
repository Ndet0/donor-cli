import requests

class WemaAPI:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, path):
        res = requests.get(
            f"{self.base_url}{path}",
            headers=self.headers()
        )
        res.raise_for_status()
        return res.json()

    def post(self, path, data):
        res = requests.post(
            f"{self.base_url}{path}",
            json=data,
            headers=self.headers()
        )
        res.raise_for_status()
        return res.json()
