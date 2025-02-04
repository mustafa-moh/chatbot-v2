from abc import ABC, abstractmethod

class SearchService(ABC):
    @abstractmethod
    def search(self, query: str) -> str:
        pass