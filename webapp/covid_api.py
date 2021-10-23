import requests
from webapp import log


# получает данные о случаях (/cases) по АПИ
def get_covid_data(country_arr):
    url = "https://covid-api.mmediagroup.fr/v1/cases"
    params = {
        "ab": country_arr
    }
    try:
        result = requests.get(url, params=params)

    # обработка сетевых ошибок
    except(requests.RequestException):
        log.logging.info(f'Network Error while get_covid_data, country code {country_arr}')
        return None

    covid_info_from_api = result.json()

    # проверка получения данных по стране, а не по всему миру
    if 'All' not in covid_info_from_api:
        log.logging.info(f'Covid data is not exist, country code {country_arr}')
        return {}
    cathegories_exist = set(covid_info_from_api['All'])
    cathegories_needed = set(['population', 'confirmed', 'deaths'])

    # проверка, что множество cathegories_needed полностью входит в множество cathegories_exist:
    if cathegories_needed.issubset(cathegories_exist):
        return parse_covid_data(covid_info_from_api)
    else:
        log.logging.info(f'Covid data is not complete, country code {country_arr}')
        return {}


def parse_covid_data(covid_info_from_api):
    covid_data = {}
    covid_data['population'] = int(covid_info_from_api['All']['population'])
    covid_data['confirmed'] = int(covid_info_from_api['All']['confirmed'])
    covid_data['deaths'] = int(covid_info_from_api['All']['deaths'])
    health_index = 100 - int(100 * (covid_data['confirmed']) / (covid_data['population']))
    if health_index == 100:
        covid_data['health index text'] = '>99'
    else:
        covid_data['health index'] = health_index
    return covid_data
