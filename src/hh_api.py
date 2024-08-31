from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class VacancyAPIClient(ABC):
    """Абстрактный базовый класс для работы с API сервиса вакансий"""

    @abstractmethod
    def get_vacancies(self, keyword, page, per_page):
        """
        Метод для получения списка вакансий.
        """
        pass


class HHVacancyAPIClient(VacancyAPIClient):
    """Класс для работы с API hh.ru"""

    def __init__(self):
        self.__api_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": "0", "per_page": "100", "only_with_salary": True}
        self.__vacancies = []

    def __get_response(self, keyword, page, per_page):
        self.__params["text"] = keyword
        self.__params["page"] = page
        self.__params["per_page"] = per_page
        response = requests.get(self.__api_url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error fetching data. Status code: {response.status_code}")

    def get_vacancies(self, keyword, page, per_page) -> List[Dict]:
        response = self.__get_response(keyword, page, per_page)
        return response.json()["items"]
