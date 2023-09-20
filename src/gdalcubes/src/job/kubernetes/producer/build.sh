#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-producer . -f Dockerfile
docker push mafehiza/gdalcubepy-producer