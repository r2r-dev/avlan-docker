#!/bin/bash -x
cd /app/avlan
/venv/bin/gunicorn -b 0.0.0.0:8000
