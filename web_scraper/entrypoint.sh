#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
echo 'from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username="admin"); u.set_password("1"); u.save()' | python manage.py shell
python manage.py runserver 0:8000 &
python manage.py async_parse_hub_and_fill_bd