#!/bin/bash -x
cd $APPDIR

# Restore webroot directory
mv webroot.bak/* webroot/
rm -rf webroot.bak

/venv/bin/python manage.py syncdb --dump resources/bootstrap.sql && \
/venv/bin/gunicorn -b 0.0.0.0:$APP_PORT --workers 3 --timeout 36000 __init__:application
