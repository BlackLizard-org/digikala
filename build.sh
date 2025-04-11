#!/bin/bash
set -o errexit

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=ali@ali.com
export DJANGO_SUPERUSER_PASSWORD=ali137580

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic --noinput
