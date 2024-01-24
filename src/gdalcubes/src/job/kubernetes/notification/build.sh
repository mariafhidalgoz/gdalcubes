#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-notification-3 . -f Dockerfile
docker push mafehiza/gdalcubepy-notification-3