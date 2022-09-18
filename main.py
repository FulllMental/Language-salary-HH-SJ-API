import requests


def get_hh_vacancies():
    payload = {
        'text': f'программист',
        'area': '1',
    }

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response


if __name__ == '__main__':
    print(get_hh_vacancies().json())
