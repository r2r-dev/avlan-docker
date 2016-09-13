#!/bin/bash
cd $APPDIR

set -e

# TODO: figure out better way of handling remote repositories
cp -r /repositories/avlan/* /repositories/avlan/.??* . && \

PYTHON=/venv/bin/python
PIP=/venv/bin/pip

$PIP install -U \
    --allow-external bzr --allow-unverified bzr \
    -r $APPDIR/requirements.txt

cd $APPDIR && /venv/bin/python setup.py develop

cd $APPDIR/avlan
chown -R py $APPDIR

ln -s /app/avlan/weebroot /app/webroot/

# temporarily append self-signed certificate
# cat /root/server-chain.crt >> /venv/lib/python2.7/site-packages/requests/cacert.pem
