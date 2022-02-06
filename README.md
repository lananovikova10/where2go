# Веб-сервис об ограничениях для международных туристов

Веб-сервис выводит по запросу туриста инфомрацию об ограничениях в стране назначения в связи с пандемией COVID-19.

Сведения выводятся на основании опубликованных данных [Ростуризма](https://city.russia.travel/safety/kakie_strany_otkryty/).

## Для локального запуска
Склонировать репозиторий, создать в этой директории виртуальное окружение, установить зависимости  pip install -r requirements.txt. 
Получить у автора файл config.py, поместить его в папку webapp

1. запуск: 
* Linux и Mac: `export FLASK_APP=webapp && export FLASK_ENV=development && flask run`
    либо запуск (env) machine-name~/where2go$ `./run.sh`
    http://127.0.0.1:5000/
* Windows: `set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run`
    либо запуск (env) machine-name\where2go>`run`
    http://127.0.0.1:5000/

2. После установки внешних модулей обновлять зависимости в корневой папке командой `python -m pip freeze > requirements.txt` и ставить их себе в venv при продолжении работы над проектом с помощью `pip install -r requirements.txt`.

3. Локально в папке проекта создать файл config.py и в нем класс class Config(object): и переменные:
    * SECRET_KEY = "секретный ключ приложения для авторизации"
    * SQLALCHEMY_DATABASE_URI = "ссылка на облачную бд, начиная с postgresql://"
    * SQLALCHEMY_TRACK_MODIFICATIONS = False
    * COUNTRY_API_KEY = "ключ API" для скрипта fetch_countries.py
    
    Файл config.py должен быть в .gitignore

4. При изменениях структуры БД делаем миграцию `flask db migrate -m "коммент что сделали"`, чтобы получить изменения перед началом работы делаем `flask db upgrade`

5. Чтобы заполнить базу со странами, добавьте в Config COUNTRY_API_KEY, запустите скрипт clear_countries.py, а затем - get_countries.py.