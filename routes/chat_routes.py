from email import message

from flask import Blueprint, request, jsonify
from controllers.chat_controller import ChatController

chat_bp = Blueprint('chat', __name__)
controller = ChatController()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message is required"}), 400

    response = controller.handle_message(message)
    return jsonify({"response": response})

@chat_bp.route('/chat/history', methods=['GET'])
def history():
    return jsonify(controller.history())