from src.hh_api import HHVacancyAPIClient
from src.vacancy import Vacancies
import json


def user_interaction():
    api_client = HHVacancyAPIClient()

    while True:
        print("Добро пожаловать в инструмент поиска вакансий!")
        print("Пожалуйста, введите ключевое слово для поиска вакансий или введите слово 'выход', чтобы выйти.")
        keyword = input("Ключевое слово: ")

        if keyword.lower() == "выход":
            print("До свидания!")
            break

        try:
            page = 0
            per_page = 100
            vacancies = api_client.get_vacancies(keyword, page, per_page)
            vacancies_list = Vacancies.creat(vacancies)

            print(f"Найдено {len(vacancies_list)} вакансий по ключевому слову '{keyword}'.")

            top_n = int(input("Сколько топ-вакансий по зарплате вы хотели бы видеть? "))
            vacancies_list.sort(reverse=True)
            # Записываем вакансии в файл vacancy.json
            with open("vacancy.json", "w", encoding="utf-8") as f:
                json.dump([v.__dict__ for v in vacancies_list], f, ensure_ascii=False, indent=4)

            for i, vacancy in enumerate(vacancies_list[:top_n], start=1):
                print(f"{i}. {vacancy}")

            search_description = input("Реализовать поиск вакансий по определенному слову в описании?(да/нет) ")
            if search_description.lower() == "да":
                description_keyword = input("Введите ключевое слово: ")
                filtered_vacancies = [v for v in vacancies_list if description_keyword.lower() in
                                      v.description.lower()]
                print(
                    f"Найдено {len(filtered_vacancies)} вакансии с ключевым словом"
                    f" '{description_keyword}' в описании.")
                for i, vacancy in enumerate(filtered_vacancies, start=1):
                    print(f"{i}. {vacancy}")
                break
            elif search_description.lower() == "нет":
                print("Хорошо, пропустим поиск по описанию. До свидания!")
                break
            else:
                print("Неверный ответ, попробуйте ещё раз.")
        except Exception as e:
            print(f"Error: {e}")
