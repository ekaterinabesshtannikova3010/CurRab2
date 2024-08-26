from abc import ABC, abstractmethod
import requests
import requests


class Parser:
    """
    Родительский класс для работы с API различных сайтов с вакансиями
    """

    def __init__(self, file_worker):
        self.file_worker = file_worker

    def load_vacancies(self, keyword):
        """
        Метод для загрузки вакансий по ключевому слову
        """
        raise NotImplementedError

    def save_vacancies(self, vacancies):
        """
        Метод для сохранения вакансий в файл
        """
        self.file_worker.save_vacancies(vacancies)

    def load_vacancies_from_file(self):
        """
        Метод для загрузки вакансий из файла
        """
        return self.file_worker.load_vacancies()


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HH()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# Пример работы контструктора класса с одной вакансией
vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
                  "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HH"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

class VacancyAPIClient(ABC):
    @abstractmethod
    def get_vacancies(self, query: str) -> list:
        pass

    @abstractmethod
    def get_vacancy_details(self, vacancy_id: str) -> dict:
        pass




class HHVacancyAPIClient(VacancyAPIClient):
    def __init__(self, area_id: int = 113):
        self.area_id = area_id
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str) -> list:
        params = {
            "text": query,
            "area": self.area_id,
            "per_page": 100,
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["items"]

    def get_vacancy_details(self, vacancy_id: str) -> dict:
        url = f"{self.base_url}/{vacancy_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Vacancy:
    title: str
    url: str
    salary: Optional[int] = field(default=0)
    description: str = ""

    def __post_init__(self):
        if self.salary is None:
            self.salary = 0


from abc import ABC, abstractmethod

class VacancyStorage(ABC):
    @abstractmethod
    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        pass

    @abstractmethod
    def load_vacancies(self, query: str) -> list[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


import json
from pathlib import Path

class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path: str = "vacancies.json"):
        self.file_path = Path(file_path)

    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        data = [vars(v) for v in vacancies]
        with self.file_path.open("w") as f:
            json.dump(data, f, indent=2)

    def load_vacancies(self, query: str) -> list[Vacancy]:
        if self.file_path.exists():
            with self.file_path.open("r") as f:
                data = json.load(f)
            return [Vacancy(**item) for item in data if query.lower() in item["title"].lower()]
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        if self.file_path.exists():
            with self.file_path.open("r") as f:
                data = json.load(f)
            data = [item for item in data if item["url"] != vacancy.url]
            with self.file_path.open("w") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()