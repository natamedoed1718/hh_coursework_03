import requests
from typing import List, Dict, Any


class HHAPIClient:
    """Клиент для работы с API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> Dict[str, Any]:
        """Получить информацию о работодателе."""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies_by_employer(
        self, employer_id: int, per_page: int = 100
    ) -> List[Dict]:
        """Получить вакансии компании."""
        url = f"{self.BASE_URL}/vacancies"
        params = {"employer_id": employer_id, "per_page": per_page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
