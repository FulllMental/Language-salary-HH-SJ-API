import requests


def get_all_vacancies(programming_language):
    page = 0
    pages_number = 1
    total_vacancies = []
    while page < pages_number:
        page_response = get_api_response(programming_language, page)
        total_found = page_response['found']
        if total_found > 99:
            pages_number = page_response['pages']
            for vacancies in page_response['items']:
                total_vacancies.append(vacancies)
            page += 1
        else: break
    return get_average_info_hh(programming_language, total_vacancies, total_found)


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


def get_average_info_hh(programming_language, total_vacancies, total_found):
    language_vacancies = {}
    if total_found > 99:
        average_salary = [predict_rub_salary(vacancy) for vacancy in total_vacancies if vacancy['salary']['currency'] == 'RUR']
        vacancies_processed = len(average_salary)
        language_vacancies.update(
            {
                programming_language: {
                    'vacancies_found': total_found,
                    'vacancies_processed': vacancies_processed,
                    'average_salary': int(sum(average_salary)/vacancies_processed)
                }
            }
        )
    return language_vacancies


def predict_rub_salary(vacancy):

    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']

    if salary_to and salary_from:
        return salary_from + salary_to / 2
    elif salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2
    else: None


if __name__ == '__main__':
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

    hh_table = {}
    for programming_language in programming_languages:
        hh_table.update(get_all_vacancies(programming_language))
    print(hh_table)
