from app.services.abstract.search_service import SearchService
from config import Config
import requests


class GoogleSearchService(SearchService):
    def __init__(self):
        self.api_key = Config.GOOGLE_SEARCH_API_KEY
        self.cx = Config.GOOGLE_SEARCH_CX

    def search(self, query: str) -> str:
        url = f"https://customsearch.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": 5,
        }

        response = requests.get(url, params=params)
        formatted_results = ""
        if response.status_code == 200:
            results = response.json().get("items", [])
            formatted_results = "\n\n".join(
                f"Title: {result['title']}\nSnippet: {result['snippet']}\nLink: {result['link']}" for result in results)

        return formatted_results
