from app.services.abstract.ai_service import AIService
from app.services.abstract.search_service import SearchService
from app.utils.session_manager import set_session_thread, get_session_thread
from flask import current_app
from config import Config
import time
import json


class AssistantService:
    def __init__(self, ai_service: AIService, search_service: SearchService):
        self.ai_service = ai_service
        self.search_service = search_service

    def create_thread(self) -> str:
        thread_id = self.ai_service.create_thread()
        set_session_thread(thread_id)
        return thread_id

    def create_or_retrieve_thread(self) -> str:
        thread_id = get_session_thread()
        if not thread_id:
            thread_id = self.create_thread()
        return thread_id

    def create_message(self, thread_id: str, prompt: str):
        message = self.ai_service.create_message(thread_id=thread_id, content=prompt)
        return message

    def run_thread(self, thread_id: str):
        run_id = self.ai_service.run_thread(thread_id=thread_id)
        return run_id

    def get_response(self, thread_id: str, run_id: str):
        run = self.ai_service.get_thread_run(thread_id=thread_id, run_id=run_id)
        status = run.status
        while status not in Config.OPENAI_TERMINATE_STATUS:
            current_app.logger.info(f"Run status: {status}")
            if status == Config.REQUIRE_ACTION_STATUS:
                return self.handle_function_call(thread_id=thread_id, run=run)

            time.sleep(2)
            run = self.ai_service.get_thread_run(thread_id=thread_id, run_id=run_id)
            status = run.status

        messages = self.ai_service.get_thread_messages(thread_id=thread_id)
        data = json.loads(messages.model_dump_json(indent=2))
        response = data['data'][0]['content'][0]['text']['value']
        return response

    def handle_function_call(self, thread_id: str, run):
        tool_outputs = []
        # Loop through each tool in the required action section
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "search_internet":
                arguments = json.loads(tool.function.arguments)
                search_results = self.search_internet(arguments['query'])
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": search_results
                })

        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = self.ai_service.submit_tool_outputs(thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs)
            except Exception as e:
                current_app.logger.error(f"Failed to submit tool outputs: {e}")
        else:
            current_app.logger.error(f"No tool outputs to submit.")

        return self.get_response(thread_id=thread_id, run_id=run.id)

    def search_internet(self, query):
        result = "could not find search results."
        if query:
            current_app.logger.info(f"start internet search using query: {query}")
            result = self.search_service.search(query=query)
        return result
