from src.hh_api import HHVacancyAPIClient
from src.clas import Vacancies

def user_interaction():
    client = HHVacancyAPIClient()
    vacancies = client.get_vacancies("python",0,5)

    vacancies = Vacancies.creat(vacancies)
    for vac in vacancies:
        print(vac)
    # print(vacancies)
    # search_query = input("Введите поисковый запрос: ")
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
    #
    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


# """
# Метод для получения списка вакансий с hh.ru.
# Принимает произвольные параметры для фильтрации, например:
# - text - текст для поиска
# - area - ID региона
# - experience - требуемый опыт работы
# - salary - диапазон зарплаты
# Возвращает список словарей, представляющих вакансии.
# """

if __name__ == "__main__":
    user_interaction()
