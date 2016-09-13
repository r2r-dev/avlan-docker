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
$ docker-compose pull mysql
  or
$ docker-compose build mysql
  or
$ cat mysql.tgz | docker import - mysql:5.7
```

- **nginx**:
```console
$ docker-compose pull nginx
  or
$ docker-compose build
  or
$ cat nginx.tgz | docker import - nginx:1.11
```

- **avlan**:
hint: it is required to place avlan framework repository under avlan/config/repositories/avlan
```console
$ docker-compose build avlan
  or
$ cat avlan.tgz | docker import - avlan:latest
```

## Usage

### Testing 
Run using docker-compose:

* start a avlan container + its dependencies (mysql database, nginx proxy)

```console
$ docker-compose run --service-ports --rm nginx
```

### Production
