#!/bin/bash -x
cd /app
/venv/bin/gunicorn -b 0.0.0.0:8000 __init__:application
