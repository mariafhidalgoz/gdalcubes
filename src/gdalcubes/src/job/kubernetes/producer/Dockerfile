FROM mafehiza/gdalcubepy
#FROM python:3.10
#MAINTAINER Maria Hidalgo <mhidalgo@uni-muenster.de>

RUN pip install kafka-python

WORKDIR /app
COPY producer.py /app/producer.py

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python producer.py
