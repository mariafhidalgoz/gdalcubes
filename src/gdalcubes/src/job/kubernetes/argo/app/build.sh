#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-argo-cube . -f Dockerfile
docker push mafehiza/gdalcubepy-argo-cube