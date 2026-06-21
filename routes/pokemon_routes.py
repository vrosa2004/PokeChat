from flask import Blueprint, jsonify
from controllers.pokemon_controller import PokemonController

pokemon_bp = Blueprint(
    "pokemon",
    __name__
)

controller = PokemonController()

@pokemon_bp.route("/pokemon/<name>")
def get_pokemon(name):
    pokemon = controller.get_pokemon(name)

    if not pokemon:
        return jsonify({
            "error": "Pokemon não encontrado"
        }), 404

    pokemon.pop("_id", None)
    return jsonify(pokemon)