#!/bin/bash -x
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py add_data_moscow
exec "$@"