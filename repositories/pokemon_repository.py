from config.database import db
import os

class PokemonRepository:
    def __init__(self):
        self.collection_name = os.getenv("COLLECTION_POKEMON")
        self.collection = db[self.collection_name]

    def find_by_name(self, name):
        return self.collection.find_one(
            { "name": name.lower() }
        )

    def save(self, pokemon):
        result = self.collection.insert_one(pokemon)
        return result.inserted_id

    def find_all(self):
        return list(self.collection.find())

    def delete_by_name(self, name):
        return self.collection.delete_one({
            "name": name.lower()
        })

    def exists(self, name):
        return self.collection.find_one({
            "name": name.lower()
        }) is not None