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


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return None


def parse_conditions_rosturizm(html, country_arr):
    soup = BeautifulSoup(html, 'html.parser')
    all_published_country = soup.findAll('div', class_='t336__title t-title t-title_md', field="title")
    #log.logging.debug(all_published_country)
    for item in all_published_country:
        if item.text == country_arr:
            info_block = item.find_next('div', class_='t-text t-text_md')
            return get_conditions(info_block)
    return {}


def get_conditions(info_block):
    country_conditions = {}
    conditions_info = info_block.findAll('strong')
    log.logging.debug(type(conditions_info))
    log.logging.info(conditions_info)
    for i in range(len(conditions_info)):
        if conditions_info[i].text.startswith('Транспортное'):
            country_conditions['transportation'] = info_block.text.split(
                                                    'Транспортное сообщение')[1].split('Виза')[0].strip(string.punctuation).strip()
        elif conditions_info[i].text.startswith('Прямое'):
            country_conditions['transportation'] = conditions_info[i].text.strip(string.punctuation).strip()
        elif conditions_info[i].text == 'Авиасообщение с пересадками':
            country_conditions['transportation'] = conditions_info[i].text.strip(string.punctuation).strip()
        elif conditions_info[i].text.startswith('Что открыто'):
            if conditions_info[i + 1].text.startswith('Ограничения'):
                country_conditions['open_objects'] = info_block.text.split(
                                                        'Что открыто')[1].split('Ограничения')[0].strip(string.punctuation).strip()
                country_conditions['restrictions'] = info_block.text.split(
                                                      'Ограничения')[1].split('Полезные телефоны')[0].strip(string.punctuation).strip()
            else:
                country_conditions['open_objects'] = info_block.text.split(
                                                        'Что открыто')[1].split('Полезные телефоны')[0].strip(string.punctuation).strip()
                country_conditions['restrictions'] = 'Нет данных'
                log.logging.info('Блок Ограничения не найден')

        country_conditions['visa'] = info_block.text.split(
                                      'Виза')[1].split('Условия въезда')[0].strip(string.punctuation).strip()
        country_conditions['vaccine'] = info_block.text.split(
                                         'Какие вакцины признаются')[1].split('Что открыто')[0].strip(string.punctuation).strip()
        country_conditions['conditions'] = info_block.text.split(
                                            'Условия въезда')[1].split('Какие вакцины признаются')[0].strip(string.punctuation).strip()
    return country_conditions
