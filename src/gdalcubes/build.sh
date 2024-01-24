#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-4 . -f DockerfilePython
docker push mafehiza/gdalcubepy-4