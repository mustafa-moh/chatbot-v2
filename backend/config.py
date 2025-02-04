import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_assistant")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_TERMINATE_STATUS = ["completed", "cancelled", "expired", "failed"]
    REQUIRE_ACTION_STATUS = "requires_action"
