#!/usr/bin/env bash
python3 manage.py migrate
gunicorn simoneMartinotta.wsgi:application --bind 0.0.0.0:$PORT
