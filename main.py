import os
import requests
from terminaltables import SingleTable
from dotenv import load_dotenv


def get_hh_api_response(language, page):
    payload = {
        'text': f'Программист {language}',
        'area': '1',
        'period': '30',
        'only_with_salary': True,
        'per_page': 100,
        'page': {page},
    }
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def get_superjob_api_response(language, sj_api_key, page):
    headers = {
        'X-Api-App-Id': sj_api_key,
    }
    payload = {
        'page': page,
        'count': 100,
        'town': 4,
        'keyword': f'Программист {language}',
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def get_all_hh_vacancies(programming_language, page, pages_number, total_vacancies):
    while page < pages_number:
        page_response = get_hh_api_response(programming_language, page)
        page_items = page_response['items']
        for vacancies in page_items:
            total_vacancies.append(vacancies)
        page += 1
    return total_vacancies


def get_average_info_hh(programming_language, total_vacancies, total_found):
    average_salary_list = [predict_rub_salary_for_hh(vacancy) for vacancy in total_vacancies if vacancy['salary']['currency'] == 'RUR']
    vacancies_processed = len(average_salary_list)
    language_hh_vacancies.append(
        [
            programming_language,
            total_found,
            vacancies_processed,
            int(safe_division(sum(average_salary_list), vacancies_processed))
        ]
    )
    return language_hh_vacancies


def get_average_info_sj(programming_language, total_vacancies, total_found):
    average_salary_list = []
    for vacancy in total_vacancies:
        if vacancy['currency'] == 'rub':
            avg_salary = perdict_rub_salary_for_superjob(vacancy)
            if avg_salary:
                average_salary_list.append(avg_salary)
    vacancies_processed = len(average_salary_list)
    language_sj_vacancies.append(
        [
            programming_language,
            total_found,
            vacancies_processed,
            int(safe_division(sum(average_salary_list), vacancies_processed))
        ]
    )
    return language_sj_vacancies


def predict_rub_salary(salary_from, salary_to):
    if salary_to and salary_from:
        return salary_from + salary_to / 2
    elif salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def predict_rub_salary_for_hh(vacancy):
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    return predict_rub_salary(salary_from, salary_to)


def perdict_rub_salary_for_superjob(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    return predict_rub_salary(salary_from, salary_to)


def safe_division(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return 0


def format_table(data, title):
    table_instance = SingleTable(data, title)
    table_instance.justify_columns[4] = 'right'
    print(table_instance.table)
    print()


if __name__ == '__main__':
    load_dotenv()
    sj_api_key = os.getenv('SECRET_KEY')
    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'C++',
        'C#',
        'C',
        'Go',
        'Objective-C',
        'Scala',
        'Swift',
        'TypeScript'
    ]

    language_hh_vacancies = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    language_sj_vacancies = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language in programming_languages:
        page = 0
        first_sj_page = get_superjob_api_response(language, sj_api_key, page)
        first_hh_page = get_hh_api_response(language, page)
        total_hh_found = first_hh_page['found']
        total_sj_found = first_sj_page['total']
        if total_hh_found > 99:
            pages_number = first_hh_page['pages']
            total_hh_vacancies = [vacancies for vacancies in first_hh_page['items']]
            get_all_hh_vacancies(language, page + 1, pages_number, total_hh_vacancies)
            get_average_info_hh(language, total_hh_vacancies, total_hh_found)
        if total_sj_found > 100:
            page_numbers = (total_sj_found - 1) // 100 + 1
            while page_numbers > page:
                total_sj_vacancies = get_superjob_api_response(language, sj_api_key, page)['objects']
                get_average_info_sj(language, total_sj_vacancies, total_sj_found)
                page += 1
        else:
            get_average_info_sj(language, first_sj_page['objects'], total_sj_found)
    format_table(language_hh_vacancies, title=' HeadHunter Moscow ')
    format_table(language_sj_vacancies, title=' SuperJob Moscow ')
