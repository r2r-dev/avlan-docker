#!/bin/bash -x

# Install static assets
rm -rf /app/webroot/* && cp -r /resources/avlan/webroot/* /app/webroot/ 

cd /app
/venv/bin/python manage.py syncdb --dump resources/bootstrap.sql && \
/venv/bin/gunicorn -b 0.0.0.0:8000 --workers 3 --timeout 360 __init__:application
