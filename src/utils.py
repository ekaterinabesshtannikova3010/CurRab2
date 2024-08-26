# from abc import ABC, abstractmethod
# import requests
# import requests
# #
#
# clas.py Parser:
#     """
#     Родительский класс для работы с API различных сайтов с вакансиями
#     """
#
#     def __init__(self, file_worker):
#         self.file_worker = file_worker
#
#     def load_vacancies(self, keyword):
#         """
#         Метод для загрузки вакансий по ключевому слову
#         """
#         raise NotImplementedError
#
#     def save_vacancies(self, vacancies):
#         """
#         Метод для сохранения вакансий в файл
#         """
#         self.file_worker.save_vacancies(vacancies)
#
#     def load_vacancies_from_file(self):
#         """
#         Метод для загрузки вакансий из файла
#         """
#         return self.file_worker.load_vacancies()
#
#
# clas.py HH(Parser):
#     """
#     Класс для работы с API HeadHunter
#     Класс Parser является родительским классом, который вам необходимо реализовать
#     """
#
#     def __init__(self, file_worker):
#         self.url = 'https://api.hh.ru/vacancies'
#         self.headers = {'User-Agent': 'HH-User-Agent'}
#         self.params = {'text': '', 'page': 0, 'per_page': 100}
#         self.vacancies = []
#         super().__init__(file_worker)
#
#     def load_vacancies(self, keyword):
#         self.params['text'] = keyword
#         while self.params.get('page') != 20:
#             response = requests.get(self.url, headers=self.headers, params=self.params)
#             vacancies = response.json()['items']
#             self.vacancies.extend(vacancies)
#             self.params['page'] += 1
#
#
# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HH()
#
# # Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.get_vacancies("Python")
#
# # Преобразование набора данных из JSON в список объектов
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
#
# # Пример работы контструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
#                   "Требования: опыт работы от 3 лет...")
#
# # Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)
#
#
# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HH"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
#
#
# if __name__ == "__main__":
#     user_interaction()
# #
# clas.py VacancyAPIClient(ABC):
#     @abstractmethod
#     def get_vacancies(self, query: str) -> list:
#         pass
#
#     @abstractmethod
#     def get_vacancy_details(self, vacancy_id: str) -> dict:
#         pass
#
#
#
# #
# clas.py HHVacancyAPIClient(VacancyAPIClient):
#     def __init__(self, area_id: int = 113):
#         self.area_id = area_id
#         self.base_url = "https://api.hh.ru/vacancies"
#
#     def get_vacancies(self, query: str) -> list:
#         params = {
#             "text": query,
#             "area": self.area_id,
#             "per_page": 100,
#         }
#         response = requests.get(self.base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return data["items"]
#
#     def get_vacancy_details(self, vacancy_id: str) -> dict:
#         url = f"{self.base_url}/{vacancy_id}"
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#
#
# from dataclasses import dataclass, field
# from typing import Optional
# #
# @dataclass(order=True)
# clas.py Vacancy:
#     title: str
#     url: str
#     salary: Optional[int] = field(default=0)
#     description: str = ""
#
#     def __post_init__(self):
#         if self.salary is None:
#             self.salary = 0
# #
# #
# from abc import ABC, abstractmethod
#
# clas.py VacancyStorage(ABC):
#     @abstractmethod
#     def save_vacancies(self, vacancies: list[Vacancy]) -> None:
#         pass
#
#     @abstractmethod
#     def load_vacancies(self, query: str) -> list[Vacancy]:
#         pass
#
#     @abstractmethod
#     def delete_vacancy(self, vacancy: Vacancy) -> None:
#         pass
#
#
# import json
# from pathlib import Path
#
# clas.py JSONVacancyStorage(VacancyStorage):
#     def __init__(self, file_path: str = "vacancies.json"):
#         self.file_path = Path(file_path)
#
#     def save_vacancies(self, vacancies: list[Vacancy]) -> None:
#         data = [vars(v) for v in vacancies]
#         with self.file_path.open("w") as f:
#             json.dump(data, f, indent=2)
#
#     def load_vacancies(self, query: str) -> list[Vacancy]:
#         if self.file_path.exists():
#             with self.file_path.open("r") as f:
#                 data = json.load(f)
#             return [Vacancy(**item) for item in data if query.lower() in item["title"].lower()]
#         return []
#
#     def delete_vacancy(self, vacancy: Vacancy) -> None:
#         if self.file_path.exists():
#             with self.file_path.open("r") as f:
#                 data = json.load(f)
#             data = [item for item in data if item["url"] != vacancy.url]
#             with self.file_path.open("w") as f:
#                 json.dump(data, f, indent=2)
# #
#
# def main():
#     api_client = HHVacancyAPIClient()
#     storage = JSONVacancyStorage()
#
#     while True:
#         print("Что вы хотите выбрать?")
#         print("1. Поиск вакансий")
#         print("2. Получить N лучших вакансий по зарплате")
#         print("3. Получить вакансии с ключевым словом в описании")
#         print("4. Выход")
#
#         choice = input("Введите свой вариант(1-4): ")
#
#         if choice == "1":
#             query = input("Введите поисковый запрос: ")
#             vacancies = api_client.get_vacancies(query)
#             for vacancy in vacancies:
#                 details = api_client.get_vacancy_details(vacancy["id"])
#                 v = Vacancy(
#                     title=details["name"],
#                     url=details["alternate_url"],
#                     salary=details["salary"]["from"] or details["salary"]["to"],
#                     description=details["snippet"]["responsibility"],
#                 )
#                 storage.save_vacancies([v])
#             print(f"{len(vacancies)} vacancies saved.")
#
#         elif choice == "2":
#             n = int(input("Введите количество лучших вакансий, которые вы хотите получить: "))
#             vacancies = storage.load_vacancies("")
#             vacancies.sort(reverse=True)
#             for v in vacancies[:n]:
#                 print(f"{v.title} - {v.salary}")
#
#         elif choice == "3":
#             keyword = input("Введите ключевое слово: ")
#             vacancies = storage.load_vacancies(keyword)
#             for v in vacancies:
#                 print(f"{v.title} - {v.url}")
#
#         elif choice == "4":
#             print("Досвидания!")
#             break
#
#         else:
#             print("Invalid choice. Please try again.")
#
# if __name__ == "__main__":
#     main()



# from abc import ABC, abstractmethod
#
# clas.py Parser(ABC):
#     """
#     Абстрактный класс для работы с API сервиса с вакансиями
#     """
#     def __init__(self, file_worker):
#         self.file_worker = file_worker
#
#     @abstractmethod
#     def load_vacancies(self, keyword):
#         """
#         Метод для получения вакансий с сервиса
#         """
#         pass
#
#     @abstractmethod
#     def get_vacancies(self):
#         """
#         Метод для получения списка вакансий
#         """
#         pass
# Теперь реализуем класс для работы с API hh.ru:

import requests

class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        # super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

    def get_vacancies(self):
        return self.vacancies
# Теперь создадим класс для работы с вакансиями:

# clas.py Vacancy:
#     def __init__(self, title, url, salary, description):
#         self.title = title
#         self.url = url
#         self.salary = self.validate_salary(salary)
#         self.description = description
#
#     def validate_salary(self, salary):
#         if salary:
#             return salary
#         else:
#             return "Зарплата не указана"
#
#     def __lt__(self, other):
#         if self.salary == "Зарплата не указана" or other.salary == "Зарплата не указана":
#             return False
#         return int(self.salary.split("-")[0].replace(" ", "")) < int(other.salary.split("-")[0].replace(" ", ""))
#
#     def __eq__(self, other):
#         return self.title == other.title and self.url == other.url
# # Теперь реализуем абстрактный класс для работы с файлами:
#
# from abc import ABC, abstractmethod
#
# clas.py FileWorker(ABC):
#     @abstractmethod
#     def save_vacancies(self, vacancies):
#         """
#         Метод для сохранения вакансий в файл
#         """
#         pass
#
#     @abstractmethod
#     def load_vacancies(self):
#         """
#         Метод для загрузки вакансий из файла
#         """
#         pass
#
#     @abstractmethod
#     def delete_vacancy(self, vacancy):
#         """
#         Метод для удаления вакансии из файла
#         """
#         pass
# # И реализуем класс для работы с JSON-файлом:
#
# import json
#
# clas.py JSONSaver(FileWorker):
#     def __init__(self, file_path="vacancies.json"):
#         self.file_path = file_path
#
#     def save_vacancies(self, vacancies):
#         with open(self.file_path, "w", encoding="utf-8") as file:
#             json.dump([v.__dict__ for v in vacancies], file, ensure_ascii=False, indent=4)
#
#     def load_vacancies(self):
#         try:
#             with open(self.file_path, "r", encoding="utf-8") as file:
#                 data = json.load(file)
#                 return [Vacancy(**v) for v in data]
#         except FileNotFoundError:
#             return []
#
#     def delete_vacancy(self, vacancy):
#         vacancies = self.load_vacancies()
#         vacancies.remove(vacancy)
#         self.save_vacancies(vacancies)
# # Теперь напишем функцию для взаимодействия с пользователем:
#
# def user_interaction():
#     file_worker = JSONSaver()
#     hh_api = HH(file_worker)
#
#     search_query = input("Введите поисковый запрос: ")
#     hh_api.load_vacancies(search_query)
#     vacancies = hh_api.get_vacancies()
#
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#
#     filtered_vacancies = [v for v in vacancies if all(word.lower() in v["description"].lower() for word in filter_words)]
#     sorted_vacancies = sorted(filtered_vacancies, key=lambda x: int(x["salary"].split("-")[0].replace(" ", "")), reverse=True)
#     top_vacancies = sorted_vacancies[:top_n]
#
#     for vacancy in top_vacancies:
#         print(f"Название: {vacancy['title']}")
#         print(f"Ссылка: {vacancy['url']}")
#         print(f"Зарплата: {vacancy['salary']}")
#         print(f"Описание: {vacancy['description']}")
#         print()
#
# if __name__ == "__main__":
#     user_interaction()