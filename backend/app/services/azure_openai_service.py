from app.services.abstract.ai_service import AIService
from openai import AzureOpenAI
from flask import current_app
from config import Config


class AzureOpenAIService(AIService):
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version="2024-08-01-preview",
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )

    def get_response(self, context) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=context
        )
        return response.choices[0].message.content

    def create_thread(self) -> str:
        thread = self.client.beta.threads.create()
        return thread.id

    def run_thread(self, thread_id: str) -> str:
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=Config.OPENAI_ASSISTANT_ID,
        )
        return run.id

    def get_thread_status(self, thread_id: str, run_id: str) -> str:
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run.status

    def get_thread_run(self, thread_id: str, run_id: str):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run

    def get_thread_messages(self, thread_id: str):
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return messages

    def create_message(self, thread_id: str, content: str):
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        return message

    def submit_tool_outputs(self, thread_id: str, run_id: str, tool_outputs):
        run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )
        return run
