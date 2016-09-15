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
```
Final layout should look like this:
```console
/opt/dockerapps/avlan/
├── avlan
├── docker-compose.yml
├── mysql
└── nginx-proxy
```

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

## Usage

### Testing 
Run using docker-compose:

* start a avlan container + its dependencies (mysql database, nginx-proxy)

```console
$ cd /opt/dockerapps/avlan
$ docker-compose up nginx-proxy
```

### Production
