# AVLAN

Avlan is a VLAN monitoring and setup tool.

## Running application in production mode (full cluster)
To build container images and start AVLAN application cluster with default settings, execute:
```console
$ ./cluster.sh -p
```

## Running application in debug mode (partial cluster)
To build container images and start cluster without AVLAN application image, execute:
```console
$ ./cluster.sh -d
```
To run instance of AVLAN application on host system:
 * Ensure first that you have following system packages installed (Debian naming convention):
```console
python libxml2-dev libxslt1-dev expat libevent-dev wget python-dev
texlive texlive-latex-extra language-pack-en unzip git python-pip
zlib1g-dev lib32z1-dev libpq-dev gettext curl latex2html libmysqlclient-dev 
```
 * Install required python modules from application directory:
```console
$ cd app
$ pip install -r requirements.txt
$ pip install ./netmiko
```
 * Set application settings according to configuration specified in 'conf/debug_cluster.conf' file
```console
$ cd app
$ vi src/conf/settings.py
```
 * Create database structure and create default entries:
```console
$ cd app
$ python manage.py syncdb --dump resources/bootstrap.sql
```
 * Execute application using Gunicorn WSGI server, supplying the same application port as APP_PORT variable in 'conf/debug_cluster.conf' file:
```console
$ source conf/debug_cluster.conf
$ cd app
$ gunicorn -b 0.0.0.0:${APP_PORT} --workers 3 --timeout 3600 __init__:application

```

## Installation
To install cluster permanently as a set of systemd services:

* Set installation directory (INSTALL_DIR) variable in 'conf/install_cluster.conf' file
* As root, execute installation using 'cluster.sh' script:
```console
# cluster.sh -i
```

## Usage
Reboot system or run using systemd service manually:
```console
$ systemctl start docker-avlan-mysql.service
$ systemctl start docker-avlan-redis.service
$ systemctl start docker-avlan.service
$ systemctl start docker-avlan-nginx.service
``` 

### Troubleshooting
* stop containers and removes containers, networks, volumes, and images created by ```up```. 
```console
$ cluster.sh -c
```
