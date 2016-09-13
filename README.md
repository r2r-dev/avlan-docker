# Avlan in Docker

A Docker container of Avlan.

## Installation
 - Place docker-compose.yml in /opt/dockerapps/avlan/ and install service files
 - Copy nginx.tmpl (from nginx/nginx.tmpl) into /opt/dockerapps/avlan/nginx

As this project is intended to be self-contained, please build, download (3rdparty images) or import following images prior to first execution:
- mysql:
```console
$ docker pull mysql:5.7
```
or
```console
$ cd mysql
$ docker build -t mysql:5.7 .
```
or
```console
$ cd mysql
$ cat mysql.tgz | docker import - mysql:5.7
```

-nginx:
```console
$ docker pull nginx:1.11
```
or
```console
$ cd nginx
$ docker build -t nginx:1.11 .
```
or
```console
$ cd nginx
$ cat nginx.tgz | docker import - nginx:1.11
```

- avlan
```console
$ cd avlan
$ docker build -t avlan:latest .
```
or
```console
$ cd avlan
$ cat avlan.tgz | docker import - avlan:latest
```

## Usage

Run using docker-compose:

* start a avlan container + its dependencies (mysql database, nginx proxy)

```console
$ docker-compose run --service-ports --rm avlan
```
