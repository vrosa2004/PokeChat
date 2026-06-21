from services.chat_service import ChatService
from repositories.history_repository import HistoryRepository
from models.chat_history import ChatHistory

class ChatController:
    def __init__(self):
        self.service = ChatService()
        self.history = HistoryRepository()

    def handle_message(self, message: str) -> str:
        response = self.service.process_message(message)
        history = ChatHistory(user_message=message, bot_response=response)
        self.history.save(history)
        return response

    def get_history(self):
        return self.history.find_all()