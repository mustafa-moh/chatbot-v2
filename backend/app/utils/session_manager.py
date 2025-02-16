from config import Config
from flask import request
import redis
import uuid
from redis.sentinel import Sentinel

if Config.REDIS_DRIVER == "sentinel":
    sentinel = Sentinel([(Config.REDIS_SENTINEL_HOST, 26379)], socket_timeout=0.1)
    redis_client = sentinel.master_for('mymaster', socket_timeout=0.1)
else:
    redis_client = redis.from_url(Config.REDIS_URL)

def get_session_id(request):
    data = request.json
    if not data.get('session_id'):
        return str(uuid.uuid4())
    return data.get('session_id')


def get_session_thread():
    conversation_key = f"thread:{request.session_id}"
    value = redis_client.get(conversation_key)
    if value:
        value = value.decode('utf-8')
    return value


def set_session_thread(content):
    conversation_key = f"thread:{request.session_id}"
    redis_client.setex(conversation_key, 3600, str(content))


def get_current_session_id():
    return request.session_id
