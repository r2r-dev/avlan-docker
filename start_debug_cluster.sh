#!/bin/bash

# Script requirements.
export DOLLAR='$'
export COMPOSE_CONFIG="./docker/docker-compose-debug.yml"
export INSTALL_DIR="$(pwd)"

# Docker-specific variables.
export DOCKERHOST="$(ip route get 1.1.1.1 | awk 'NR==1 {print $NF}')"

# MYSQL-specific variables.
export MYSQL_ROOT_PASSWORD="avlan"
export MYSQL_USER="avlan"
export MYSQL_PASSWORD="avlan"
export MYSQL_DATABASE="avlan"
export MYSQL_PORT="3306"

# Redis-specific variables.
export REDIS_PORT="6379"

# Nginx-specific variables.
export NGINX_HTTP_PORT="8888"
export NGINX_HTTPS_PORT="443"
export NGINX_HOSTNAME="avlan.local"

# Host-side application specific variables.
export APP_HOST="${DOCKERHOST}"
export APP_PORT=8000

cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - stop
cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - rm --force -v
cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - build
cat ${COMPOSE_CONFIG} | envsubst | docker-compose -f - up
