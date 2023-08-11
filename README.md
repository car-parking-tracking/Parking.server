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

- В директории `parking_server/` нужно создать файл .env:

```
SECRET_KEY='django-insecure-v86xt@@+44^@**$5mdno!sg=b-txu3fv7p6l75*6(!r5rsd6cm'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_PASSWORD='xrgcbyyhrjfeuyxb'
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL = 'parkonaft-noreply@gmail.com'
```

- далее создать виртуальное окружение

`python -m venv venv`

- Активировать виртуальное окружение:

`venv\Scripts\activate`

- Установить зависимости:

`pip install -r requirements.txt`

- Создаём базу данных:

`python manage.py migrate`

- Загрузить данные парковок в базу данных:

`python manage.py add_data_moscow`

- Запустить сервер:

`python manage.py runserver`

- Перейдите в браузере по адресу:

    [http://127.0.0.1:8000/api/v1/]([http://127.0.0.1:8000/api/v1/])