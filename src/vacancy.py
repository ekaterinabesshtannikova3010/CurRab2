from typing import Dict, Any, List


class Vacancies:
    def __init__(self, id_: str, salary: int, name: str, url: str, description: str):
        self.id_ = self._validate_id(id_)
        self.salary = salary
        self.name = self._validate_name(name)
        self.url = self._is_valid_url(url)
        self.description = self._validate_description(description)

    def _validate_id(self, id_: str) -> str:
        if not isinstance(id_, str):
            return "0"
        else:
            return id_

    @staticmethod
    def get_salary(vac: Dict[str, Any]) -> int:
        if vac["salary"] is None:
            return 0
        elif vac["salary"]["from"] and vac["salary"]["to"] is None:
            return vac["salary"]["from"]
        elif vac["salary"]["to"] and vac["salary"]["from"] is None:
            return vac["salary"]["to"]
        else:
            return (vac["salary"]["to"] + vac["salary"]["from"]) // 2

    @staticmethod
    def _validate_salary(salary: int) -> int:
        if not isinstance(salary, int):
            return 0
        else:
            return salary

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            return ""
        else:
            return name

    @staticmethod
    def _validate_description(description: str) -> str:
        if not isinstance(description, str):
            return "0"
        else:
            return description

    @staticmethod
    def _is_valid_url(url: str) -> str:
        if not isinstance(url, str):
            return "0"
        else:
            return url

    @classmethod
    def creat(cls, data_vac: List[Dict[str, Any]]) -> List['Vacancies']:
        list_vacancy = []
        for vac in data_vac:
            try:
                id_ = vac["id"]
                salary = cls.get_salary(vac)
                name = vac["name"]
                url = vac["url"]
                description = vac["snippet"]["responsibility"]
                obg = cls(id_, salary, name, url, description)
                list_vacancy.append(obg)
            except (TypeError, ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue
        return list_vacancy

    def __str__(self) -> str:
        return (f"Id: {self.id_}, зарплата: {self.salary} название: {self.name}, url: {self.url},"
                f" описание: {self.description}.")

    def __eq__(self, other: 'Vacancies') -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.salary == other.salary

    def __ne__(self, other: 'Vacancies') -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: 'Vacancies') -> bool:
        return self.salary < other.salary

    def __le__(self, other: 'Vacancies') -> bool:
        return self.salary <= other.salary

    def __gt__(self, other: 'Vacancies') -> bool:
        return self.salary > other.salary

    def __ge__(self, other: 'Vacancies') -> bool:
        return self.salary >= other.salary
