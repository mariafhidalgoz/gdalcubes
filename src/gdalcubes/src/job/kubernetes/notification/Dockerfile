FROM mafehiza/gdalcubepy
RUN pip install kafka-python

WORKDIR /app
COPY notification.py /app/notification.py

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python notification.py
