#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-producer-112 . -f Dockerfile
docker push mafehiza/gdalcubepy-producer-112