import pytest
import json
from src.vacancy import Vacancies
from src.work_with_files import JsonVacancyStorage


@pytest.fixture
def temp_file(tmpdir):
    return tmpdir.join("test_vacancy.json")


def test_add_vacancy(temp_file):
    storage = JsonVacancyStorage(str(temp_file))
    vacancy = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
    storage.add_vacancy(vacancy)
    storage.save_vacancies()

    with open(str(temp_file), "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]['id_'] == "1"
    assert data[0]['salary'] == 50000


def test_get_vacancies(temp_file):
    storage = JsonVacancyStorage(str(temp_file))
    vacancy = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
    storage.add_vacancy(vacancy)
    storage.save_vacancies()

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].id_ == "1"
    assert vacancies[0].salary == 50000


def test_delete_vacancy(temp_file):
    storage = JsonVacancyStorage(str(temp_file))
    vacancy = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
    storage.add_vacancy(vacancy)
    storage.save_vacancies()

    storage.delete_vacancy("1")
    storage.save_vacancies()

    with open(str(temp_file), "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 0


def test_save_vacancies(temp_file):
    storage = JsonVacancyStorage(str(temp_file))
    vacancy = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
    storage.add_vacancy(vacancy)
    storage.save_vacancies()

    with open(str(temp_file), "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]['id_'] == "1"


def test_load_vacancies(temp_file):
    vacancy = Vacancies("1", 50000, "Python Developer", "https://example.com/vacancy1", "Develop Python applications")
    with open(str(temp_file), "w", encoding="utf-8") as f:
        json.dump([vacancy.__dict__], f, ensure_ascii=False, indent=4)

    storage = JsonVacancyStorage(str(temp_file))
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 1
    assert vacancies[0].id_ == "1"
    assert vacancies[0].salary == 50000


if __name__ == "__main__":
    pytest.main()
