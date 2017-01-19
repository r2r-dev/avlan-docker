#!/bin/bash
cd $APPDIR

set -e
set -x

# Install default settings
cp /etc/default/avlan-config.py src/conf/settings.py

# Install dependencies
cd ${APPDIR}/netmiko
/venv/bin/python setup.py install

cd ${APPDIR}
# Save webroot dir for later re-mounting
mv webroot webroot.bak
