#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-consumer-3 . -f Dockerfile
docker push mafehiza/gdalcubepy-consumer-3