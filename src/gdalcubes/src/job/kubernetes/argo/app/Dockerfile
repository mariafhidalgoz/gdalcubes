FROM mafehiza/gdalcubepy-10
RUN pip install redis

WORKDIR /app
COPY main.py /app/main.py

#COPY ./new_image_collection_from_file.db /app/new_image_collection_from_file.db
#COPY ../../file_list.txt /app/file_list.txt

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

#CMD python main.py
CMD python -u ./main.py --source="/opt/gdalcubes/Python/L8_Amazon_mini" --size="96"
