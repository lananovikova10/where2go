import requests
from bs4 import BeautifulSoup

def get_avia_rosturizm():
    url = "https://city.russia.travel/safety/kakie_strany_otkryty/"
    html = get_html(url)
    data = parsed_countries_avia(html)
    return data


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def parsed_countries_avia(html):
    soup = BeautifulSoup(html, 'html.parser')
    data_list = soup.findAll('div', class_='t537__wrapperleft')
    countries_avia = []
    avias = []
    for item in data_list:
        country = item.find('div', class_='t537__persname t-name t-name_lg t537__bottommargin_sm').find('a').text
        countries_avia.append(country)
        avia = item.find('div', class_='t537__persdescr t-descr t-descr_xxs t537__bottommargin_lg').text
        avias.append(avia)

    return dict(zip(countries_avia, avias)) 
