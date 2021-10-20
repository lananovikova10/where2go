import requests
import pprint
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
        fetching_info_exist = [True for elem in ['population',
                                                 'confirmed', 'deaths'] if elem in covid['All']]

        if all(fetching_info_exist):
            return parse_covid_data(covid)
        else:
            return None

    # обработка сетевых ошибок
    except(requests.RequestException, ValueError):
        log.logging.info('Сетевая ошибка при получении инфо о COVID')
        return None


def parse_covid_data(covid):
    covid_data = {}
    covid_data['population'] = int(covid['All']['population'])
    covid_data['confirmed'] = int(covid['All']['confirmed'])
    covid_data['deaths'] = int(covid['All']['deaths'])
    covid_data['health index'] = 100 - int(100 * (covid_data['confirmed']) / (covid_data['population']))
    return covid_data


if __name__ == "__main__":
    cov = covid_by_country("HU")

    pprint.pprint(cov)
