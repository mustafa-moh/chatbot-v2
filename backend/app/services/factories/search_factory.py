from app.services.abstract.search_service import SearchService
from app.services.google_search_service import GoogleSearchService


class SearchFactory:
    @staticmethod
    def create_search_service(service_name: str) -> SearchService:
        if service_name == "google":
            return GoogleSearchService()
        raise ValueError(f"Unsupported search service: {service_name}")
