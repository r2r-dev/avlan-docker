#!/bin/bash
cd $APPDIR

set -e

# TODO: figure out better way of handling remote repositories
cp -r /resources/avlan/* /resources/avlan/.??* .

# Install default settings
cp /etc/default/avlan-config.py src/conf/settings.py

# Install dependencies
PYTHON=/venv/bin/python
PIP=/venv/bin/pip

$PIP install -U \
    --allow-external bzr --allow-unverified bzr \
    -r $APPDIR/resources/requirements.txt

$PYTHON /resources/netmiko/setup.py install

# Create persistent storage directory
mkdir $APPDIR/storage
chown -R py $APPDIR
