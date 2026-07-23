import requests

BASE_URL = "http://127.0.0.1:8000"


class APIClient:

    @staticmethod
    def get(endpoint):

        response = requests.get(
            f"{BASE_URL}{endpoint}"
        )

        response.raise_for_status()

        return response.json()