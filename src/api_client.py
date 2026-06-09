from typing import Any, Dict, List, cast
import requests


class HHAPIClient:
    BASE_URL = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def get_vacancies_by_employer(self, employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/vacancies"
        params = {"employer_id": employer_id, "per_page": per_page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        return cast(List[Dict[str, Any]], items)
pass