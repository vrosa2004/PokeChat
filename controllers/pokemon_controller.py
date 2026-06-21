from services.pokemon_service import PokemonService

class PokemonController:
    def __init__(self):
        self.service = PokemonService()

    def get_pokemon(self, name):
        return self.service.get_pokemon(name)