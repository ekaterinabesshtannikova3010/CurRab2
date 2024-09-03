from src.vacancy import Vacancies
from abc import ABC, abstractmethod
import json
from typing import List
from dataclasses import dataclass


@dataclass
class Vacancies:
    id_: str
    salary: int
    name: str
    url: str
    description: str

    def __str__(self):
        return (f"Id: {self.id_}, зарплата: {self.salary} название: {self.name}, url: {self.url},"
                f" описание: {self.description}.")


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
        self.vacancies: List[Vacancies] = self.load_vacancies()

    def load_vacancies(self) -> List[Vacancies]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Vacancies(**vac) for vac in data]
        except FileNotFoundError:
            return []

    def add_vacancy(self, vacancy: Vacancies) -> None:
        if vacancy not in self.vacancies:
            self.vacancies.append(vacancy)

    def get_vacancies(self, **kwargs) -> List[Vacancies]:
        return self.vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        self.vacancies = [v for v in self.vacancies if v.id_ != vacancy_id]

    def save_vacancies(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([v.__dict__ for v in self.vacancies], f, ensure_ascii=False, indent=4)
