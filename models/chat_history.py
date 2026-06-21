from datetime import datetime

class ChatHistory:
    def __init__(self, user_message: str, bot_response: str):
        self.user_message = user_message
        self.bot_response = bot_response
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "timestamp": self.timestamp
        }