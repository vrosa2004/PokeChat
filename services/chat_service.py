import os
import json
import google.generativeai as genai
from services.pokemon_service import PokemonService

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ChatService:
    TYPE_TRANSLATIONS = {
        "fire": "fogo", "water": "água", "grass": "planta", "electric": "elétrico",
        "ice": "gelo", "fighting": "lutador", "poison": "veneno", "ground": "terra",
        "flying": "voador", "psychic": "psíquico", "bug": "inseto", "rock": "pedra",
        "ghost": "fantasma", "dragon": "dragão", "dark": "sombrio", "steel": "aço",
        "fairy": "fada", "normal": "normal"
    }

    TYPE_NAMES_PT = {
        "fogo": "fire", "água": "water", "agua": "water", "planta": "grass",
        "elétrico": "electric", "eletrico": "electric", "gelo": "ice",
        "lutador": "fighting", "veneno": "poison", "terra": "ground",
        "voador": "flying", "psíquico": "psychic", "psiquico": "psychic",
        "inseto": "bug", "pedra": "rock", "fantasma": "ghost",
        "dragão": "dragon", "dragao": "dragon", "sombrio": "dark",
        "aço": "steel", "aco": "steel", "fada": "fairy", "normal": "normal"
    }

    def __init__(self):
        self.pokemon_service = PokemonService()
        self.client = self.pokemon_service.client
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _extract_intent(self, message: str) -> dict:
        prompt = f"""
Você é um assistente que extrai intenções de perguntas sobre Pokémon.
Analise a mensagem e responda APENAS com um JSON, sem texto adicional, sem markdown.

Intenções possíveis:
- "fraqueza": o que é forte/superefetivo CONTRA o pokémon
- "ataque": o que o pokémon ataca bem / é forte contra
- "tipo_pokemon": qual o tipo de um pokémon
- "fraqueza_tipo": fraqueza de um tipo específico
- "desconhecido": não é sobre pokémon

Exemplos:
"qual a fraqueza do pikachu?" -> {{"intent": "fraqueza", "pokemon": "pikachu", "type": null}}
"pikachu é forte contra que tipo?" -> {{"intent": "ataque", "pokemon": "pikachu", "type": null}}
"qual o tipo do charizard?" -> {{"intent": "tipo_pokemon", "pokemon": "charizard", "type": null}}
"que tipo vence pokémons de água?" -> {{"intent": "fraqueza_tipo", "pokemon": null, "type": "water"}}
"qual o tipo do tipo fogo?" -> {{"intent": "fraqueza_tipo", "pokemon": null, "type": "fire"}}

Mensagem: "{message}"
"""
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(text)
        except Exception:
            return {"intent": "desconhecido", "pokemon": None, "type": None}

    def get_pokemon_types(self, name: str):
        pokemon = self.pokemon_service.get_pokemon(name)
        return pokemon["types"] if pokemon else None

    def get_super_effective_against(self, pokemon_name: str) -> str:
        types = self.get_pokemon_types(pokemon_name)
        if not types:
            return f"Não encontrei o Pokémon '{pokemon_name}'."

        weaknesses = set()
        for type_name in types:
            res = self.client.get_type(type_name)
            if not res:
                continue
            for t in res["damage_relations"]["double_damage_from"]:
                weaknesses.add(t["name"])

        if not weaknesses:
            return f"Não consegui buscar as fraquezas de {pokemon_name.capitalize()}."

        translated = [self.TYPE_TRANSLATIONS.get(w, w) for w in weaknesses]
        return f"Use tipos {', '.join(translated)} para ser superefetivo contra {pokemon_name.capitalize()}."

    def get_pokemon_strong_against(self, pokemon_name: str) -> str:
        types = self.get_pokemon_types(pokemon_name)
        if not types:
            return f"Não encontrei o Pokémon '{pokemon_name}'."

        strong_against = set()
        for type_name in types:
            res = self.client.get_type(type_name)
            if not res:
                continue
            for t in res["damage_relations"]["double_damage_to"]:
                strong_against.add(t["name"])

        translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in strong_against]
        return f"{pokemon_name.capitalize()} é superefetivo contra tipos: {', '.join(translated)}."

    def get_super_effective_against_type(self, type_en: str) -> str:
        res = self.client.get_type(type_en)
        if not res:
            return f"Não consegui buscar informações sobre esse tipo."

        counters = [t["name"] for t in res["damage_relations"]["double_damage_from"]]
        type_pt = next((k for k, v in self.TYPE_NAMES_PT.items() if v == type_en), type_en)
        translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in counters]
        return f"Pokémons do tipo {type_pt} são fracos contra: {', '.join(translated)}."

    def get_pokemon_type_info(self, pokemon_name: str) -> str:
        types = self.get_pokemon_types(pokemon_name)
        if not types:
            return f"Não encontrei o Pokémon '{pokemon_name}'."
        translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in types]
        return f"{pokemon_name.capitalize()} é do tipo: {', '.join(translated)}."

    def process_message(self, message: str) -> str:
        intent_data = self._extract_intent(message)
        intent = intent_data.get("intent")
        pokemon = intent_data.get("pokemon")
        type_en = intent_data.get("type")

        if intent == "fraqueza" and pokemon:
            return self.get_super_effective_against(pokemon)

        if intent == "ataque" and pokemon:
            return self.get_pokemon_strong_against(pokemon)

        if intent == "tipo_pokemon" and pokemon:
            return self.get_pokemon_type_info(pokemon)

        if intent == "fraqueza_tipo" and type_en:
            return self.get_super_effective_against_type(type_en)

        return "Não entendi sua pergunta. Tente perguntar sobre fraquezas ou tipos, ex: 'Qual a fraqueza do Charizard?'"