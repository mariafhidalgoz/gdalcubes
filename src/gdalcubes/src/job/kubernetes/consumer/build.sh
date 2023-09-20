#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-consumer . -f Dockerfile
docker push mafehiza/gdalcubepy-consumer