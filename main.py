import requests


def get_api_response(language):
    payload = {
        'text': f'программист {language}',
        'area': '1',
        'period': '30',
        'only_with_salary': True,
    }

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response


def get_hh_vacancies(programming_languages):
    language_vacancies = {}

    for language in programming_languages:
        search_results = get_api_response(language).json()
        vacancies_found = search_results["found"]

        if vacancies_found > 99:
            average_salary = [predict_rub_salary(vacancy) for vacancy in search_results['items'] if
                              vacancy['salary']['currency'] == 'RUR']
            vacancies_processed = len(average_salary)
            language_vacancies.update(
                {
                    language: {
                        'vacancies_found': vacancies_found,
                        'vacancies_processed': vacancies_processed,
                        'average_salary': int(sum(average_salary) / vacancies_processed)
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

    print(get_hh_vacancies(programming_languages))
