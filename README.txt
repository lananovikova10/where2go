1. Запуск проекта: 
Linux и Mac: export FLASK_APP=webapp && export FLASK_ENV=development && flask run
Windows: set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

2. Не забываем фризить зависимости из корневой папки командой python -m pip freeze > requirements.txt и ставить их себе в venv при продолжении работы над проектом с помощью pip install -r requirements.txt

3. Локально в папке проекта создать файл config.py и в нем класс class Config(object): и переменные:
    SECRET_KEY = "секретный ключ приложения для авторизации"
    SQLALCHEMY_DATABASE_URI = "ссылка на облачную бд, начиная с postgresql://"
    SQLALCHEMY_TRACK_MODIFICATIONS = Fals
    COUNTRY_API_KEY = "ключ к апи со странами"
Он должен быть в .gitignore

4. При изменениях структуры БД делаем миграцию flask db migrate -m "коммент что сделали", чтобы получить изменения перед началом работы делаем flask db upgrade

5. Чтобы заполнит базу со странами, добавьте в Config COUNTRY_API_KEY и запустите скрипт get_countries.py.