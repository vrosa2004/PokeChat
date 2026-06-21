import requests

class PokeApiClient:
    BASE_URL = "https://pokeapi.co/api/v2"

    def get_pokemon(self, name):
        response = requests.get(
            f"{self.BASE_URL}/pokemon/{name.lower()}",
        )

        if response.status_code == 200:
            return response.json()

        return None

    def get_type(self, type_name: str):
        response = requests.get(f"{self.BASE_URL}/type/{type_name}")

        if response.status_code == 200:
            return response.json()

        return None