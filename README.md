# Avlan

Avlan is a VLAN monitoring and setup tool.

## Installation
  - Place docker-compose.yml in /opt/dockerapps/avlan:
```console
$ mkdir -p /opt/dockerapps/avlan
$ cp docker-compose.yml /opt/dockerapps/avlan
```
  - Install service files: 
```console
$ cp **/docker-*.service /etc/systemd/system/
$ systemctl enable docker-avlan.service
$ systemctl enable docker-mysql.service
$ systemctl enable docker-nginx.service
```
  - Copy nginx configuration template:
```console
$ mkdir /opt/dockerapps/nginx
$ cp nginx/nginx.tmpl /opt/dockerapps/nginx
```

As this project is intended to be self-contained, please build, download (3rdparty images) or import following images prior to first execution:

- **mysql**:
```console
$ docker pull mysql:5.7
  or
$ cd mysql
$ docker build -t mysql:5.7 .
  or
$ cd mysql
$ cat mysql.tgz | docker import - mysql:5.7
```

- **nginx**:
```console
$ docker pull nginx:1.11
  or
$ cd nginx
$ docker build -t nginx:1.11 .
  or
$ cd nginx
$ cat nginx.tgz | docker import - nginx:1.11
```

- **avlan**
```console
$ cd avlan
$ docker build -t avlan:latest .
  or
$ cd avlan
$ cat avlan.tgz | docker import - avlan:latest
```

## Usage

Run using docker-compose:

* start a avlan container + its dependencies (mysql database, nginx proxy)

```console
$ docker-compose run --service-ports --rm avlan
```
