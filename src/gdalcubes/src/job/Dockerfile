FROM mafehiza/gdalcubepy
RUN pip install redis

WORKDIR /app
COPY ./worker.py /app/worker.py
COPY ./rediswq.py /app/rediswq.py

COPY ./new_image_collection_from_file.db /app/new_image_collection_from_file.db
COPY ./file_list.txt /app/file_list.txt

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python worker.py
