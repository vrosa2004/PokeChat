from config.database import db
from models.chat_history import ChatHistory

class HistoryRepository:
    def __init__(self):
        self.collection = db["chat_history"]

    def save(self, history: ChatHistory):
        return self.collection.insert_one(history.to_dict())

    def find_all(self):
        history = list(self.collection.find())
        for h in history:
            h.pop("_id", None)
        return history