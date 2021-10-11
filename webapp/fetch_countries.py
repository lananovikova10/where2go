import requests


continents_list = ["Европа", "Азия", "Океания", "Африка", "Америка", "Антарктика"]

def fetch_country_data():
    countries = {}
    list_of_countries = []
    for continent in continents_list:
        country_api_url = "http://htmlweb.ru/geo/api.php"
        params = {
            "location": continent,
            "json": "",
            "api_key": "0e66cfa42c9efb166e263f5d918f11a7"
        }
        get_request_result = requests.get(country_api_url, params = params)
        get_request_result.raise_for_status()
        countries_fetch_result = get_request_result.json()
        countries.update(countries_fetch_result)
        for value in countries.values():
            list_of_countries.append(value)
    return list_of_countries
