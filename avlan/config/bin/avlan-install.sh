#!/bin/bash
cd $APPDIR

set -e

# TODO: figure out better way of handling remote repositories
cp -r /repositories/avlan/* /repositories/avlan/.??* . && \

# Install default settings
# TODO: these should be imported from default dir
cp /etc/default/avlan-config.py src/conf/settings.py

PYTHON=/venv/bin/python
PIP=/venv/bin/pip

$PIP install -U \
    --allow-external bzr --allow-unverified bzr \
    -r $APPDIR/scripts/requirements.txt

chown -R py $APPDIR

# temporarily append self-signed certificate
# cat /root/server-chain.crt >> /venv/lib/python2.7/site-packages/requests/cacert.pem
