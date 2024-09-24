#!/usr/bin/env bash

LOGFILE="/tmp/docker_dinkey.log"
CONTAINER_NAME="django_app-django-app-1"

echo "USB event: $1 $2 $3 $4" >> "$LOGFILE"

if [! -z "$(docker ps -qf name=$CONTAINER_NAME)" ]; then
  if [ "$1" == "added" ]; then
    docker exec -u 0 $CONTAINER_NAME mknod $2 c $3 $4
    docker exec -u 0 $CONTAINER_NAME chmod 666 $2
    echo "Adding $2to docker" >> "$LOGFILE"
  elif [ "$1" == "removed" ]; then
    docker exec -u 0 $CONTAINER_NAME rm $2
    echo "Removing $2 from docker" >> "$LOGFILE"
  fi
fi
