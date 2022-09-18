import requests


def get_api_response(programming_language):
    payload = {
        'text': f'программист {programming_language}',
        'area': '1',
        'period': '30',
        'only_with_salary': True,
    }

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response


def count_vacancies(programming_languages):
    language_vacancies = {}
    for language in programming_languages:
        found = get_api_response(language).json()["found"]
        if found > 99:
            language_vacancies.update({language: found})
    return language_vacancies


def predict_rub_salary(vacancy):
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']

    if vacancy['salary']['currency'] == 'RUR':
        if salary_to and salary_from:
            return salary_from + salary_to / 2
        elif salary_to:
            return salary_to * 0.8
        elif salary_from:
            return salary_from * 1.2
    else:
        return None


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

    for vacancy in get_api_response('Python').json()['items']:
        print(predict_rub_salary(vacancy))
