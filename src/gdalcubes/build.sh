#!/bin/bash

docker login
docker build --tag mafehiza/gdalcubepy-10 . -f DockerfilePython
docker push mafehiza/gdalcubepy-10