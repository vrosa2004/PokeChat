from services.pokemon_service import PokemonService


class ChatService:
    BASE_URL = "https://pokeapi.co/api/v2"

    TYPE_TRANSLATIONS = {
        "fire": "fogo", "water": "água", "grass": "planta", "electric": "elétrico",
        "ice": "gelo", "fighting": "lutador", "poison": "veneno", "ground": "terra",
        "flying": "voador", "psychic": "psíquico", "bug": "inseto", "rock": "pedra",
        "ghost": "fantasma", "dragon": "dragão", "dark": "sombrio", "steel": "aço",
        "fairy": "fada", "normal": "normal"
    }

    def __init__(self):
        self.pokemon_service = PokemonService()
        self.client = self.pokemon_service.client

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

    TYPE_NAMES_PT = {
        "fogo": "fire", "água": "water", "agua": "water", "planta": "grass",
        "elétrico": "electric", "eletrico": "electric", "gelo": "ice",
        "lutador": "fighting", "veneno": "poison", "terra": "ground",
        "voador": "flying", "psíquico": "psychic", "psiquico": "psychic",
        "inseto": "bug", "pedra": "rock", "fantasma": "ghost",
        "dragão": "dragon", "dragao": "dragon", "sombrio": "dark",
        "aço": "steel", "aco": "steel", "fada": "fairy", "normal": "normal"
    }

    def get_pokemon_strong_against(self, pokemon_name: str) -> str:
        types = self.get_pokemon_types(pokemon_name)
        if not types:
            return f"Não encontrei o Pokémon '{pokemon_name}'."

        strong_against = set()
        for type_name in types:
            res = self.client.get_type(type_name)
            if not res:
                continue
            for t in res["damage_relations"]["double_damage_to"]:  # "to" em vez de "from"
                strong_against.add(t["name"])

        translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in strong_against]
        return f"{pokemon_name.capitalize()} é superefetivo contra tipos: {', '.join(translated)}."

    def get_super_effective_against_type(self, type_pt: str) -> str:
        type_en = self.TYPE_NAMES_PT.get(type_pt.lower())
        if not type_en:
            return f"Não reconheci o tipo '{type_pt}'."

        res = self.client.get_type(type_en)
        if not res:
            return f"Não consegui buscar informações sobre o tipo '{type_pt}'."

        counters = [t["name"] for t in res["damage_relations"]["double_damage_from"]]
        translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in counters]
        return f"Pokémons do tipo {type_pt} são fracos contra: {', '.join(translated)}."

    def process_message(self, message: str) -> str:
        message_lower = message.lower()

        if any(w in message_lower for w in
               ["forte", "fraqueza", "fraco", "superefetivo", "super efetivo", "vence", "bate"]):

            # "forte contra tipo terra" → fraquezas do tipo
            if "tipo" in message_lower:
                words = message_lower.replace("?", "").split()
                if "tipo" in words:
                    tipo_idx = words.index("tipo") + 1
                    if tipo_idx < len(words):
                        type_name = words[tipo_idx]
                        return self.get_super_effective_against_type(type_name)

            pokemon_name = self._extract_pokemon_name(message_lower)
            if not pokemon_name:
                return "Não entendi qual Pokémon. Tente: 'Qual a fraqueza do Pikachu?'"

            # "[pokemon] é forte/superefetivo contra" → o que ele ataca bem
            if any(f"{pokemon_name} é {w}" in message_lower or f"{pokemon_name} e {w}" in message_lower
                   for w in ["forte", "superefetivo", "super efetivo"]):
                return self.get_pokemon_strong_against(pokemon_name)

            # "fraco/fraqueza/forte contra [pokemon]" → o que é forte contra ele
            return self.get_super_effective_against(pokemon_name)

        if "tipo" in message_lower:
            pokemon_name = self._extract_pokemon_name(message_lower)
            if not pokemon_name:
                return "Não entendi qual Pokémon. Tente: 'Qual o tipo do Pikachu?'"
            types = self.get_pokemon_types(pokemon_name)
            if not types:
                return f"Não encontrei o Pokémon '{pokemon_name}'."
            translated = [self.TYPE_TRANSLATIONS.get(t, t) for t in types]
            return f"{pokemon_name.capitalize()} é do tipo: {', '.join(translated)}."

        return "Não entendi. Tente perguntar sobre fraquezas ou tipos, ex: 'Qual a fraqueza do Charizard?'"

    def _extract_pokemon_name(self, message: str) -> str | None:
        stop_words = {"qual", "quais", "é", "são", "superefetivo", "super", "efetivo",
                      "contra", "o", "a", "fraqueza", "fraco", "forte", "vence", "bate",
                      "de", "do", "da", "pokemon", "pokémon", "tipo", "?", "que", "sobre"}
        words = message.replace("?", "").split()
        candidates = [w for w in words if w not in stop_words and len(w) > 2]
        return candidates[-1] if candidates else None