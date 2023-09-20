FROM mafehiza/gdalcubepy
RUN pip install kafka-python

WORKDIR /app
COPY producer.py /app/producer.py

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python producer.py
