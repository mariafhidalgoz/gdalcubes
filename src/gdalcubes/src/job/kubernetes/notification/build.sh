#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-notification . -f Dockerfile
docker push mafehiza/gdalcubepy-notification