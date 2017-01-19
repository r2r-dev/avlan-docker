#!/bin/bash
cd $APPDIR

set -e

# Install default settings
cp /etc/default/avlan-config.py src/conf/settings.py

# Install dependencies
PIP=/venv/bin/pip

$PIP install -U \
    --allow-external bzr --allow-unverified bzr \
    -r requirements.txt

$PIP install ./netmiko

# Save webroot dir for later re-mounting
mv webroot webroot.bak
