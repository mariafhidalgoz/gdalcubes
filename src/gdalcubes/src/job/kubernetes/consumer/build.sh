#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-consumer-10 . -f Dockerfile
docker push mafehiza/gdalcubepy-consumer-10