import requests, string
from bs4 import BeautifulSoup
from webapp import log


def get_info_rosturizm(country_arr):
    url = "https://city.russia.travel/safety/kakie_strany_otkryty/"
    html = get_html(url)
    if html:
        data = parse_conditions_rosturizm(html, country_arr)
        return data
    else:
        return None


def get_countries_rosturizm():
    url = "https://city.russia.travel/safety/kakie_strany_otkryty/"
    html = get_html(url)
    if html:
        data = get_accepted_countries(html)
        return data
    else:
        return None


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return None


def get_accepted_countries(html):
    all_published_countries = []
    open_countries = []
    soup = BeautifulSoup(html, 'html.parser')
    all_published_countries = soup.findAll('div', class_='t537__persname t-name t-name_lg t537__bottommargin_sm')
    for country_object in all_published_countries:
        open_countries.append(country_object.text)
        open_countries.sort()
    return open_countries


def parse_conditions_rosturizm(html, country_arr):
    soup = BeautifulSoup(html, 'html.parser')
    all_published_country = soup.findAll('div', class_='t336__title t-title t-title_md', field="title")
    for item in all_published_country:
        if item.text == country_arr:
            info_block = item.find_next('div', class_='t-text t-text_md')
            return get_conditions(info_block), filter_set_of_headers(info_block)
    return {}


def get_strong_headers(info_block):
    conditions_info_dirty = info_block.findAll('strong')
    return [i.text.strip().strip(string.punctuation) for i in conditions_info_dirty]


def get_conditions(info_block):
    country_conditions = {}
    no_data = 'Нет данных'
    conditions_info = get_strong_headers(info_block)
    def get_transportation():
        for i in conditions_info:
            if i.startswith('Транспортное'):
                return info_block.text.split('Транспортное сообщение')[1].split('Виза')[0].strip(string.punctuation).strip()
            elif i.startswith('Прямое') or i.startswith('Авиасообщение с пересадками'):
                return i
            return no_data

    def get_open_objects_and_restrictions():
        if 'Ограничения' in conditions_info and 'Что открыто' in conditions_info:
            return info_block.text.split('Что открыто')[1].split('Ограничения')[0].strip(string.punctuation).strip(), \
                    info_block.text.split('Ограничения')[1].split('Полезные телефоны')[0].strip(string.punctuation).strip()
        elif 'Что открыто' in conditions_info:
            return info_block.text.split('Что открыто')[1].split('Полезные телефоны')[0].strip(string.punctuation).strip(), \
                    no_data

    def get_visa():
        if 'Виза' in info_block.text and 'Условия въезда' in info_block.text:
            return info_block.text.split('Виза')[1].split('Условия въезда')[0].strip(string.punctuation).strip()
        return no_data

    def get_vaccine():
        if 'Какие вакцины признаются' in info_block.text and 'Что открыто' in info_block.text:
            return info_block.text.split('Какие вакцины признаются')[1].split('Что открыто')[0].strip(string.punctuation).strip()
        return no_data

    def get_conditions():
        if 'Условия въезда' in info_block.text and 'Какие вакцины признаются' in info_block.text:
            return info_block.text.split('Условия въезда')[1].split('Какие вакцины признаются')[0].strip(string.punctuation).strip()
        return no_data

    country_conditions['transportation'] = get_transportation()
    country_conditions['open_objects'] = get_open_objects_and_restrictions()[0]
    country_conditions['restrictions'] = get_open_objects_and_restrictions()[1]
    country_conditions['visa'] = get_visa()
    country_conditions['vaccine'] = get_vaccine() 
    country_conditions['conditions'] = get_conditions()
    return country_conditions


def filter_set_of_headers(info_block):
    headers_for_country = set(get_strong_headers(info_block))
    headers_pattern = ('Прямое авиасообщение', 'Транспортное сообщение', 'Авиасообщение с пересадками',
               'Виза', 'Условия въезда', 'Какие вакцины признаются', 'Что открыто', 'Ограничения', 'Полезные телефоны')
    if headers_for_country.issubset(headers_pattern):
        return False
    else:
        return True
