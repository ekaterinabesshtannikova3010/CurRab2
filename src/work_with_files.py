from abc import ABC, abstractmethod
import json
from typing import List, Dict
from src.vacancy import Vacancies

class VacancyStorage(ABC):
    """Абстрактный базовый класс для хранения информации о вакансиях"""

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancies') -> None:
        """
        Метод для добавления информации о вакансии в хранилище.
        """
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs) -> List['Vacancies']:
        """
        Метод для получения информации о вакансиях из хранилища по указанным критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Метод для удаления информации о вакансии из хранилища.
        """
        pass

    @abstractmethod
    def save_vacancies(self) -> None:
        """
        Метод для сохранения всех вакансий в хранилище.
        """
        pass


class JsonVacancyStorage(VacancyStorage):
    """Класс для хранения информации о вакансиях в JSON-файле"""

    def __init__(self, file_path: str = "vacancy.json"):
        self.file_path = file_path
        self.vacancies = []
#
    def add_vacancy(self, vacancy: 'Vacancies') -> None:
        self.vacancies.append(vacancy)
#
    def get_vacancies(self, **kwargs) -> List['Vacancies']:
        """Реализация поиска вакансий по указанным критериям."""
        return self.vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Реализация удаления вакансии по ID"""
        self.vacancies = [v for v in self.vacancies if v.id_ != vacancy_id]

    def save_vacancies(self) -> None:
        """Сохранение всех вакансий в JSON-файл"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([v.__dict__ for v in self.vacancies], f, ensure_ascii=False, indent=4)


# Пример использования
vacancy_storage = JsonVacancyStorage("vacancy.json")

# Добавление вакансий
vacancy1 = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
vacancy2 = Vacancies("2", 60000, "Senior Python Developer", "https://example.com/vacancy2",
                     "Lead Python development team")
vacancy_storage.add_vacancy(vacancy1)
vacancy_storage.add_vacancy(vacancy2)

# Сохранение вакансий в файл
vacancy_storage.save_vacancies()

# Получение вакансий
all_vacancies = vacancy_storage.get_vacancies()
for vacancy in all_vacancies:
    print(vacancy)

# Удаление вакансии
vacancy_storage.delete_vacancy("1")
vacancy_storage.save_vacancies()
