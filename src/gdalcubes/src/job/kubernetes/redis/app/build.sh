#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-send-chunks . -f Dockerfile
docker push mafehiza/gdalcubepy-send-chunks