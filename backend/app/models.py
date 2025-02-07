from pymongo import MongoClient
from config import Config
from datetime import datetime

client = MongoClient(Config.MONGO_URI)
db = client.get_database()
chat_logs = db.chatbot_assistant_logs


def save_chat_log(session_id, prompt, ai_response, thread_id):
    chat_logs.insert_one({
        "session_id": session_id,
        "timestamp": datetime.now(),
        "user_message": prompt,
        "ai_response": ai_response,
        "thread_id": thread_id
    })
