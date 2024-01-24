# Creating the consumer to process the data
# Creating the producer to notify the status of the process
import json
import logging
import time
import datetime
from enum import Enum
from pathlib import Path

import gdalcubepy
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(level=logging.INFO)

GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC = "gdalcubespy-notifications"
GDALCUBESPY_CONSUMER_KAFKA_TOPIC = "write-netcdf"

producer = KafkaProducer(bootstrap_servers="kafka:9092")

consumer = KafkaConsumer(
    GDALCUBESPY_CONSUMER_KAFKA_TOPIC,
    bootstrap_servers="kafka:9092",
    group_id='blog_group'
)


class Producers(Enum):
    CREATE_IMAGE_COLLECTION = 1
    WRITE_CHUNKS = 2
    MERGE_CHUNKS = 3


if __name__ == '__main__':
    set_processed = dict()
    logging.info("Consumer | Started chunks processor...")
    while True:
        for message in consumer:
            logging.info(f"Consumer | Message {message}")
            consumed_message = json.loads(message.value.decode("utf-8"))
            task_id = consumed_message["task_id"]
            state = consumed_message["state"]

            logging.info(f"Consumer | State: {state}")

            # if state == Producers.CREATE_IMAGE_COLLECTION:
            if state == 1:
                logging.info("Consumer | Creating Image Collection...")
                create_cube = consumed_message["create_cube"]
                format_name = create_cube['format_name']
                chunks_name = create_cube['chunks_name']
                files_src = create_cube['files_src']
                files_dest = create_cube['files_dest']
                current_path = create_cube['current_path']
                logging.info(f"files_src {files_src}")
                logging.info(f"files_dest {files_dest}")
                logging.info(f"current_path {current_path}")
                logging.info(f"format_name {format_name}")

                # Create destination dir
                Path(files_dest).mkdir(parents=True, exist_ok=True)

                # Create Image Collection from file
                output_image_collection = f"{files_dest}/image_collection.db"
                # format_ic = f"{current_path}/formats/{format_name}.json"
                format_ic = f"{format_name}.json"
                logging.info("Consumer | Start creating Image Collection ...")
                start_time = time.time()
                start_dt = datetime.datetime.fromtimestamp(start_time)
                gdalcubepy.gdalcubes.create_image_collection(files_src, output_image_collection, format_ic)
                end_time = time.time()
                end_dt = datetime.datetime.fromtimestamp(end_time)
                logging.info(f"Consumer | --- Time start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                logging.info(f"Consumer | --- Time end: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                logging.info(f"Consumer | --- {end_time - start_time} seconds ---")
                # Paths kafka
                # gdalcubepy.gdalcubes.create_image_collection("file_list.txt", "new_image_collection.db", "L8_SR.json")
                logging.info("Consumer | Image Collection created (.db)")

                # Create cube
                logging.info(f"Consumer | Start creating Cube ...")
                start_time = time.time()
                start_dt = datetime.datetime.fromtimestamp(start_time)
                cube = gdalcubepy.gdalcubes.create_image_collection_cube(output_image_collection)
                end_time = time.time()
                end_dt = datetime.datetime.fromtimestamp(end_time)
                logging.info(f"Consumer | --- Time start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                logging.info(f"Consumer | --- Time end: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                logging.info(f"Consumer | --- {end_time - start_time} seconds ---")
                logging.info("Consumer | Cube created")

                # Chunks number of a cube
                total_chunks = gdalcubepy.gdalcubes.total_chunks(cube)
                logging.info(f"Consumer | Total chunks {total_chunks}")

                data = dict(
                    task_id=task_id,
                    state=2,
                    # state=Producers.WRITE_CHUNKS,
                    write_chunks=dict(
                        total_chunks=total_chunks,
                        # cube=cube,
                    )
                )

                # send messages to kafka topic
                producer.send(GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
                logging.info(f"Consumer | Done creating Image Collection ...{data}")

            # if  state == Producers.WRITE_CHUNKS:
            if state == 2:
                logging.info("Consumer | Writing chunks...")
                write_chunks = consumed_message["write_chunks"]

                chunk_id = write_chunks['chunk_id']
                # cube = write_chunks['cube']

                # Write single chunk netcdf
                is_chunk_empty = gdalcubepy.gdalcubes.is_chunk_empty(cube, chunk_id)
                logging.info(f"Consumer | Chunk Id {chunk_id} is empty {is_chunk_empty}.")
                if not is_chunk_empty:
                    output_chunk = f"{files_dest}/{chunks_name}{chunk_id}.nc"
                    logging.info(f"Consumer | Start processing Chunk Id {chunk_id} ...")
                    start_time = time.time()
                    start_dt = datetime.datetime.fromtimestamp(start_time)
                    gdalcubepy.gdalcubes.write_single_chunk_netcdf(cube, output_chunk, chunk_id)
                    end_time = time.time()
                    end_dt = datetime.datetime.fromtimestamp(end_time)
                    logging.info(f"Consumer | --- Time start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                    logging.info(f"Consumer | --- Time end: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
                    logging.info(f"Consumer | --- {end_time - start_time} seconds ---")
                    logging.info(f"Consumer | Chunk Id {chunk_id} processed")

                data = dict(
                    task_id=task_id,
                    state=3,
                    # state=Producers.MERGE_CHUNKS,
                    merge_chunks=dict(
                        chunk_id=chunk_id,
                    )
                )

                # send messages to kafka topic
                producer.send(GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
                logging.info(f"Consumer | Done writing chunk ...{data}")

            # if state == Producers.MERGE_CHUNKS:
            if state == 3:
                logging.info("Consumer S-3 | Merging chunks...")
                # # cube = gcp.create_image_collection_cube(
                # #     f"{os.getcwd()}/Python/results/new_image_collection_from_txt_file.db")
                # total_chunks = gdalcubepy.gdalcubes.total_chunks(cube)
                # logging.info(f"Consumer S-3  | Total chunks {total_chunks}")
                #
                # # output_merge = "Python/results/test3"
                # output_merge = f"{files_dest}"
                # logging.info(f"Consumer S-3  | Folder {output_merge}")
                #
                # output_file_merge = "result"
                # logging.info(f"Consumer S-3  | File {output_file_merge}")
                #
                # # gcp.merge_chunks(cube, f"Python/results/test5", "result")
                # gdalcubepy.gdalcubes.merge_chunks(cube, output_merge, output_file_merge)
                # logging.info(f"Consumer | Done merging chunks ...{data}")

                continue
