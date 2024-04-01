#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-send-chunks-size-96 . -f Dockerfile
docker push mafehiza/gdalcubepy-send-chunks-size-96