FROM mafehiza/gdalcubepy-10
RUN pip install redis

WORKDIR /app
COPY config.py /app/config.py
COPY redis_module.py /app/redis_module.py
COPY main.py /app/main.py

#COPY ./new_image_collection_from_file.db /app/new_image_collection_from_file.db
#COPY ../../file_list.txt /app/file_list.txt

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python main.py
