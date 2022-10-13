import os
import requests
from dotenv import load_dotenv


def get_api_response(language, page):
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


def get_all_vacancies(programming_language, page, pages_number, total_vacancies):
    while page < pages_number:
        page_response = get_api_response(programming_language, page)
        page_items = page_response['items']
        for vacancies in page_items:
            total_vacancies.append(vacancies)
        page += 1
    return total_vacancies


def get_average_info_hh(programming_language, total_vacancies, total_found):
    average_salary = [predict_rub_salary_for_hh(vacancy) for vacancy in total_vacancies if vacancy['salary']['currency'] == 'RUR']
    vacancies_processed = len(average_salary)
    language_vacancies.update(
        {
            programming_language: {
                'vacancies_found': total_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': int(sum(average_salary) / vacancies_processed)
            }
        }
    )
    return language_vacancies


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


def get_superjob_api_response(sj_api_key, language):
    headers = {
        'X-Api-App-Id': sj_api_key,
    }
    payload = {
        'page': 0,
        'count': 100,
        'town': 4,
        'keyword': f'Программист {language}',
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    # programming_languages = [
    #     'JavaScript',
    #     'Java',
    #     'Python',
    #     'Ruby',
    #     'C++',
    #     'C#',
    #     'C',
    #     'Go',
    #     'Objective-C',
    #     'Scala',
    #     'Swift',
    #     'TypeScript'
    # ]
    #
    language_vacancies = {}
    # for language in programming_languages:
    #     page = 0
    #     first_page = get_api_response(language, page)
    #     total_found = first_page['found']
    #
    #     if total_found > 99:
    #         pages_number = first_page['pages']
    #         total_vacancies = [vacancies for vacancies in first_page['items']]
    #         get_all_vacancies(language, page + 1, pages_number, total_vacancies)
    #         get_average_info_hh(language, total_vacancies, total_found)
    #     else:
    #         continue
    #
    # print(language_vacancies)
    language = 'Python'
    load_dotenv()
    sj_api_key = os.getenv('SECRET_KEY')
    sj_response = get_superjob_api_response(sj_api_key, language)['objects']
    for vacancy in sj_response:
        print(f'{vacancy["profession"]}, {vacancy["town"]["title"]}, {perdict_rub_salary_for_superjob(vacancy)}')
