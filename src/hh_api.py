from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class VacancyAPIClient(ABC):
    """Абстрактный базовый класс для работы с API сервиса вакансий"""


    @abstractmethod
    def get_vacancies(self, keyword: str, page: int, per_page: int) -> List[Dict]:
        """
        Метод для получения списка вакансий.
        """
        pass


class HHVacancyAPIClient(VacancyAPIClient):
    """Класс для работы с API hh.ru"""


    def __init__(self):
        self.__api_url: str = "https://api.hh.ru/vacancies"
        self.__headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.__params: Dict[str, str] = {"text": "", "page": "0", "per_page": "100", "only_with_salary": "true"}
        self.__vacancies: List[Dict] = []

    def __get_response(self, keyword, page, per_page):
        self.__params["text"] = keyword
        self.__params["page"] = str(page)
        self.__params["per_page"] = str(per_page)
        response = requests.get(self.__api_url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error fetching data. Status code: {response.status_code}")


    def get_vacancies(self, keyword: str, page: int, per_page: int) -> List[Dict]:
        response: requests.Response = self.__get_response(keyword, page, per_page)
        return response.json()["items"]
