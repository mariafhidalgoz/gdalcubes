#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-notification-10 . -f Dockerfile
docker push mafehiza/gdalcubepy-notification-10