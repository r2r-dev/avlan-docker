#!/bin/bash -x

# Install static assets
rm -rf /app/webroot/* && cp -r /repositories/avlan/webroot/* /app/webroot/ 

cd /app
/venv/bin/python manage.py syncdb --dump scripts/database.sql
/venv/bin/gunicorn -b 0.0.0.0:8000 __init__:application
