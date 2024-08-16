from abc import ABC, abstractmethod
import requests

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


def main():
    api_client = HHVacancyAPIClient()
    storage = JSONVacancyStorage()

    while True:
        print("Что вы хотите выбрать?")
        print("1. Поиск вакансий")
        print("2. Получить N лучших вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Выход")

        choice = input("Введите свой вариант(1-4): ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = api_client.get_vacancies(query)
            for vacancy in vacancies:
                details = api_client.get_vacancy_details(vacancy["id"])
                v = Vacancy(
                    title=details["name"],
                    url=details["alternate_url"],
                    salary=details["salary"]["from"] or details["salary"]["to"],
                    description=details["snippet"]["responsibility"],
                )
                storage.save_vacancies([v])
            print(f"{len(vacancies)} vacancies saved.")

        elif choice == "2":
            n = int(input("Введите количество лучших вакансий, которые вы хотите получить: "))
            vacancies = storage.load_vacancies("")
            vacancies.sort(reverse=True)
            for v in vacancies[:n]:
                print(f"{v.title} - {v.salary}")

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            vacancies = storage.load_vacancies(keyword)
            for v in vacancies:
                print(f"{v.title} - {v.url}")

        elif choice == "4":
            print("Досвидания!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()