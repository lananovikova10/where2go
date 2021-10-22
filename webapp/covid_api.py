import requests
from webapp import log


# получает данные о случаях (/cases) по АПИ
def covid_by_country(country_arr):
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    params = {
        "ab": country_arr
    }
    try:
        result = requests.get(url, params=params)
        covid = result.json()
        fetching_info_exist = [True for elem in ['population', 'confirmed', 'deaths'] if elem in covid['All']]
        if all(fetching_info_exist):
            return parse_covid_data(covid)
        else:
            return None

    # обработка сетевых ошибок
    except(requests.RequestException, ValueError, KeyError):
        log.logging.info('Jшибка при получении инфо о COVID')
        return None


def parse_covid_data(covid):
    covid_data = {}
    covid_data['population'] = int(covid['All']['population'])
    covid_data['confirmed'] = int(covid['All']['confirmed'])
    covid_data['deaths'] = int(covid['All']['deaths'])
    health_index = 100 - int(100 * (covid_data['confirmed']) / (covid_data['population']))
    if health_index == 100:
        health_index = '>99'
    covid_data['health index'] = health_index
    return covid_data
