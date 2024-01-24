FROM python:3.10
MAINTAINER Maria Hidalgo <mhidalgo@uni-muenster.de>

RUN pip install kafka-python

WORKDIR /app
COPY notification.py /app/notification.py

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python notification.py
