from flask import Flask, request, jsonify
from pymongo import MongoClient

from app.services.assistant_service import AssistantService
from app.services.factories.ai_factory import AIFactory
from app.services.factories.search_factory import SearchFactory
from app.utils.session_manager import get_session_id, get_session_thread, get_current_session_id, set_session_thread
from config import Config
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize services using factories
ai_service = AIFactory.create_ai_service("openai")
search_service = SearchFactory.create_search_service("google")
assistant_service = AssistantService(ai_service, search_service)

# Initialize MongoDB
#client = MongoClient(Config.MONGO_URI)
#db = client.get_database()
#chat_logs = db.chat_logs


@app.before_request
def ensure_session_id():
    if request.is_json:
        session_id = get_session_id(request)
        request.session_id = session_id


@app.route("/api/chat", methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')

    if not prompt or not prompt.strip():
        return jsonify({"error": "Prompt is required and cannot be empty."}), 422

    # Retrieve conversation history from session manager
    thread_id = assistant_service.create_or_retrieve_thread()
    assistant_service.create_message(thread_id=thread_id, prompt=prompt)
    run_id = assistant_service.run_thread(thread_id=thread_id)
    ai_response = assistant_service.get_response(thread_id=thread_id, run_id=run_id)

    # Log conversation to MongoDB
    # chat_logs.insert_one({
    #     "session_id": get_current_session_id(),
    #     "timestamp": datetime.now(),
    #     "user_message": prompt,
    #     "ai_response": response_txt
    # })

    return jsonify({
        "response": ai_response,
        "session_id": get_current_session_id()
    })
