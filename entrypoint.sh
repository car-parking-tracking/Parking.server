#!/bin/sh
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn parking_backend.wsgi:application --bind 0.0.0.0:8000
exec "$@"