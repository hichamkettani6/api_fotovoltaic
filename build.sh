#!/bin/bash

if [ ! -e "$PWD/.env" ]; then
  echo ".env file does not exist!"
  exit 0
fi

source .env
docker build --rm -f Dockerfile . --build-arg TZ=$TZ --network host -t api_grafici_fotovoltaico:latest
docker build --rm -f worker_Dockerfile . --build-arg TZ=$TZ --network host -t celery:latest