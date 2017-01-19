#!/bin/bash
set -e

export DOLLAR='$'
export EPOCH="$(date +%s%3N)"
export TEMP_CONFIG="$(mktemp)"

function run_debug_cluster() {
  source ./conf/debug_cluster.conf
  prepare_config
  build_cluster
  run_cluster
}

function run_production_cluster() {
  source ./conf/production_cluster.conf
  prepare_production_cluster
  run_cluster
}

function install_production_cluster() {
  source ./conf/install_cluster.conf
  prepare_production_cluster

  cat ./systemd/templates/docker-avlan.tmpl | envsubst > /etc/systemd/docker-avlan.service
  cat ./systemd/templates/docker-avlan-nginx.tmpl | envsubst > /etc/systemd/docker-avlan-nginx.service
  cat ./systemd/templates/docker-avlan-mysql.tmpl | envsubst > /etc/systemd/docker-avlan-mysql.service
  cat ./systemd/templates/docker-avlan-redis.tmpl | envsubst > /etc/systemd/docker-avlan-redis.service

  mkdir -p "${INSTALL_DIR}"
  cp "${TEMP_CONFIG}" "${INSTALL_DIR}/docker-compose.yml"

  systemctl enable docker-avlan.service
  systemctl enable docker-avlan-mysql.service
  systemctl enable docker-avlan-redis.service
  systemctl enable docker-avlan-nginx.service
  systemctl daemon-reload
}

function prepare_config() {
  cat "${COMPOSE_CONFIG}" | envsubst > "${TEMP_CONFIG}"
}

function prepare_production_cluster() {
  prepare_config

  rm -rf ./docker/avlan/app
  rm -rf ./docker/avlan/Dockerfile

  # Install latest version of the app
  cat ./docker/avlan/Dockerfile.tmpl | envsubst > ./docker/avlan/Dockerfile
  cp -r ./app ./docker/avlan/app

  build_cluster
  rm -rf ./docker/avlan/app
  rm ./docker/avlan/Dockerfile
}

function build_cluster() {
  docker-compose -f "${TEMP_CONFIG}" stop
  docker rm avlan avlan-mysql avlan-nginx avlan-redis || true
  docker-compose -f "${TEMP_CONFIG}" rm --force -v
  docker-compose -f "${TEMP_CONFIG}" build
}

function run_cluster() {
  docker-compose -f "${TEMP_CONFIG}" up
}

function cleanup() {
  source ./conf/production_cluster.conf
  prepare_config
  docker-compose -f "${TEMP_CONFIG}" --rmi all
}

function print_help() {
  echo "Available options:" >&2
  echo "-p start production cluster" >&2
  echo "-d start debug cluster" >&2
  echo "-i install cluster as systemd service" >&2
  echo "-c stop containers and removes containers, networks, volumes, and images" >&2
  exit 1
}

if [[ ! $@ =~ ^\-.+ ]]
then
  print_help
fi

while getopts ":pid" opt; do
  case $opt in
    p)
      run_production_cluster 
      ;;
    d)
      run_debug_cluster 
      ;;
    i)
      install_production_cluster
      ;;
    c)
      cleanup
      ;;
     *)
      print_help
     ;;
  esac
done

rm "${TEMP_CONFIG}"
