from repositories.pokemon_repository import PokemonRepository
from clients.pokeapi_client import PokeApiClient
from models.pokemon import Pokemon

class PokemonService:
    def __init__(self):
        self.repository = PokemonRepository()
        self.client = PokeApiClient()

    def get_pokemon(self, name):
        pokemon = self.repository.find_by_name(name)

        if pokemon:
            return pokemon

        data = self.client.get_pokemon(name)

        if not data:
            return None

        pokemon = Pokemon(
            name=data["name"],
            types=[t["type"]["name"] for t in data["types"]]
        )

        self.repository.save(pokemon.to_dict())
        return pokemon.to_dict()