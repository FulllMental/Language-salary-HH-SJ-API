import requests


def get_hh_vacancies(programming_language):
    payload = {
        'text': f'программист {programming_language}',
        'area': '1',
        'period': '30',
    }

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response


def count_vacancies(programming_languages):
    language_vacancies = {}
    for language in programming_languages:
        found = get_hh_vacancies(language).json()["found"]
        if found > 99:
            language_vacancies.update({language: found})
    return language_vacancies


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
    print(count_vacancies(programming_languages))

