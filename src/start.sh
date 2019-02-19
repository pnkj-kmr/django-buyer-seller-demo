#!/bin/sh


source $(pwd)/../venv/bin/activate

start()
{
$(pwd)/../venv/bin/python manage.py runserver 0.0.0.0:80  --noreload
}

start