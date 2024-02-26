#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-process-chunks . -f Dockerfile
docker push mafehiza/gdalcubepy-process-chunks