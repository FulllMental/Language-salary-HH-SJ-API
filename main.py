import requests


def get_hh_vacancies():
    payload = {
        'text': f'программист',
    }

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response


if __name__ == '__main__':
    print(get_hh_vacancies().json())
