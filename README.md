# Avlan

Avlan is a VLAN monitoring and setup tool.

## Installation
As this project is intended to be self-contained, please build, download (3rdparty images) or import following images prior to first execution:

- **mysql**:
```console
$ docker-compose pull mysql
  or
$ docker-compose build mysql
```

- **nginx**:
```console
$ docker-compose build nginx-proxy
```

- **avlan**:
hint: it is required to place avlan framework repository under avlan/config/repositories/avlan
```console
$ docker-compose build avlan
```

### Permanent installation (Linux only)
  - Place docker-compose.yml in an installation directory (reffered later on as INSTALL_DIR):
```console
$ mkdir -p INSTALL_DIR
$ cp docker-compose.yml INSTALL_DIR/
```
  - Configure and install service environment file pointing to execution directory:
```
$ sed -e "s#WORKING_DIRECTORY=#WORKING_DIRECTORY=INSTALL_DIR#g" -i systemd/avlan.conf
$ cp systemd/avlan.conf /etc/sysconfig/ 
```
  - Install service files: 
```console
$ cp systemd/docker-*.service /etc/systemd/system/
$ systemctl enable docker-avlan.service
$ systemctl enable docker-mysql.service
$ systemctl enable docker-nginx.service
```
Final layout should look like this:
```console
INSTALL_DIR
├── avlan
├── docker-compose.yml
├── mysql
└── nginx-proxy
```

## Usage

### Testing 
Run using docker-compose:

* start a avlan container + its dependencies (mysql database, nginx-proxy)

```console
$ docker-compose up
```

## Production (Linux only)
Run using systemd service:
```console
$ systemctl start docker-nginx-proxy.service
``` 
