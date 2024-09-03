import pytest
from src.vacancy import Vacancies


def test_get_salary():
    vac1 = {"salary": None}
    vac2 = {"salary": {"from": 50000, "to": None}}
    vac3 = {"salary": {"from": None, "to": 70000}}
    vac4 = {"salary": {"from": 50000, "to": 70000}}

    assert Vacancies.get_salary(vac1) == 0
    assert Vacancies.get_salary(vac2) == 50000
    assert Vacancies.get_salary(vac3) == 70000
    assert Vacancies.get_salary(vac4) == 60000


def test_validate_salary():
    assert Vacancies._validate_salary(50000) == 50000
    assert Vacancies._validate_salary("50000") == 0


def test_validate_name():
    assert Vacancies._validate_name("Python Developer") == "Python Developer"
    assert Vacancies._validate_name(123) == ""


def test_validate_description():
    assert Vacancies._validate_description(
        "Responsible for developing Python applications") == "Responsible for developing Python applications"
    assert Vacancies._validate_description(123) == "0"


def test_is_valid_url():
    assert Vacancies._is_valid_url(
        "https://example.com/job/python-developer") == "https://example.com/job/python-developer"
    assert Vacancies._is_valid_url(123) == "0"


def test_create_vacancies():
    data_vac = [
        {"id": "1", "salary": {"from": 50000, "to": 70000}, "name": "Python Developer",
         "url": "https://example.com/job/python-developer",
         "snippet": {"responsibility": "Responsible for developing Python applications"}},
        {"id": "2", "salary": {"from": None, "to": 80000}, "name": "Senior Python Developer",
         "url": "https://example.com/job/senior-python-developer",
         "snippet": {"responsibility": "Lead a team of Python developers"}},
        {"id": "3", "salary": None, "name": 123, "url": "https://example.com/job/junior-python-developer",
         "snippet": {"responsibility": "Assist senior developers in Python projects"}}
    ]

    vacancies = Vacancies.creat(data_vac)
    assert len(vacancies) == 3
    assert vacancies[0].id_ == "1"
    assert vacancies[0].salary == 60000
    assert vacancies[0].name == "Python Developer"
    assert vacancies[0].url == "https://example.com/job/python-developer"
    assert vacancies[0].description == "Responsible for developing Python applications"
    assert vacancies[1].id_ == "2"
    assert vacancies[1].salary == 80000
    assert vacancies[1].name == "Senior Python Developer"
    assert vacancies[1].url == "https://example.com/job/senior-python-developer"
    assert vacancies[1].description == "Lead a team of Python developers"


if __name__ == "__main__":
    pytest.main()
