#!/usr/bin/env bash
gunicorn simoneMartinotta.wsgi:application --bind 0.0.0.0:$PORT
