#!/bin/bash -x
cd $APPDIR

# Restore webroot directory
mv webroot.bak/* webroot/
rm -rf webroot.bak

/venv/bin/python manage.py syncdb --dump resources/bootstrap.sql && \
/venv/bin/gunicorn -b 0.0.0.0:8000 --workers 3 --timeout 3600 __init__:application
