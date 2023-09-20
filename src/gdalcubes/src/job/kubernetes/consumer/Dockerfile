FROM mafehiza/gdalcubepy
RUN pip install kafka-python

WORKDIR /app
COPY consumer.py /app/consumer.py

COPY ./file_list.txt /app/file_list.txt

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python consumer.py
