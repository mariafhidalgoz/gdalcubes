FROM mafehiza/gdalcubepy-10
MAINTAINER Maria Hidalgo <mhidalgo@uni-muenster.de>

RUN pip install kafka-python

WORKDIR /app
COPY producer.py /app/producer.py

ENV PATH="/opt/gdalcubes/.venv/bin:$PATH"

CMD python -u ./producer.py --source="/opt/gdalcubes/Python/L8_Amazon_mini" --size="112"
