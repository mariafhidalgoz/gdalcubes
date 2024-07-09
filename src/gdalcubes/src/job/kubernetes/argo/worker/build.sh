#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-argo-chunks . -f Dockerfile
docker push mafehiza/gdalcubepy-argo-chunks