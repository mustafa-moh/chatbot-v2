from abc import ABC, abstractmethod


class AIService(ABC):
    @abstractmethod
    def get_response(self, context) -> str:
        pass

    @abstractmethod
    def create_thread(self) -> str:
        pass

    @abstractmethod
    def run_thread(self, thread_id: str) -> str:
        pass

    @abstractmethod
    def get_thread_status(self, thread_id: str, run_id: str) -> str:
        pass

    @abstractmethod
    def get_thread_run(self, thread_id: str, run_id: str):
        pass

    @abstractmethod
    def get_thread_messages(self, thread_id: str):
        pass

    @abstractmethod
    def create_message(self, thread_id: str, content: str):
        pass

    @abstractmethod
    def submit_tool_outputs(self, thread_id: str, run_id: str, tool_outputs):
        pass
