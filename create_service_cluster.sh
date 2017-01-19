#!/bin/bash

# Prepare images and configuration for service installation.

# Install latest version of the app
rm -rf ./docker/avlan/config/app
cp -r ./app ./docker/avlan/config/

# Script requirements.
export INSTALL_DIR="/opt/avlan"

export DOLLAR='$'
export COMPOSE_CONFIG="./docker/docker-compose-production.yml"
export SERVICE_CONFIG="./docker/docker-compose.yml"

# MYSQL-specific variables.
export MYSQL_ROOT_PASSWORD="avlan"
export MYSQL_USER="avlan"
export MYSQL_PASSWORD="avlan"
export MYSQL_DATABASE="avlan"
export MYSQL_PORT=3306

# Redis-specific variables.
export REDIS_PORT=6379

# Nginx-specific variables.
export NGINX_HTTP_PORT=8888
export NGINX_HTTPS_PORT=443
export NGINX_HOSTNAME="avlan.local"

# Host-side application specific variables.
export APP_PORT=8000

#cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - stop
#cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - rm --force -v
#cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - build

cat ${COMPOSE_CONFIG} | envsubst > "${SERVICE_CONFIG}"
echo "WORKING_DIRECTORY=${INSTALL_DIR}" > ./docker/systemd/avlan.conf 
