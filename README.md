## Parking backend

### Project folder structure:
```
parking_server/                  <- project root
├── parking_backend/              <- Django root
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── README.md
├── users/
├── static/
├── media/
└── templates/
```

Чтобы запустить проект в Dev режиме необходимо:

- В директории `parking_server/` нужно создать виртуальное окружение:

`python -m venv venv`

- Активировать виртуальное окружение:

`venv\Scripts\activate`

- Установить зависимости:

`pip install -r requirements.txt`

- Создаём базу данных:

`python manage.py migrate`

- Загрузить данные парковок в базу данных:

`python manage.py add_data_moscow`

- Создать .env файл (за основу взять .env.example) в директории Parking.server/infra

- Запустить сервер:

`python manage.py runserver`

- Перейдите в браузере по адресу:

    [http://127.0.0.1:8000/api/v1/]([http://127.0.0.1:8000/api/v1/])

- Чтобы собрать и развернуть в контейнерах:

`docker-compose up -d --build`

- Наполните базу данных ингредиентами:

`docker-compose exec backend python manage.py import_csv`