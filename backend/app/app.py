from flask import Flask, request, jsonify

from app.models import save_chat_log
from app.services.assistant_service import AssistantService
from app.services.factories.ai_factory import AIFactory
from app.services.factories.search_factory import SearchFactory
from app.utils.session_manager import get_session_id, get_current_session_id
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize services using factories
ai_service = AIFactory.create_ai_service(Config.OPENAI_DRIVER)
search_service = SearchFactory.create_search_service("google")
assistant_service = AssistantService(ai_service, search_service)


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
    save_chat_log(session_id=get_current_session_id(), thread_id=thread_id, prompt=prompt, ai_response=ai_response)

    return jsonify({
        "response": ai_response,
        "session_id": get_current_session_id()
    })
