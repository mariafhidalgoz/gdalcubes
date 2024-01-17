# Creating the producer
import json
import logging
import time
from enum import Enum

from kafka import KafkaProducer, KafkaConsumer

logging.basicConfig(level=logging.INFO)

GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC = "gdalcubespy-notifications"
GDALCUBESPY_CONSUMER_KAFKA_TOPIC = "write-netcdf"

producer = KafkaProducer(bootstrap_servers="kafka:9092")

consumer = KafkaConsumer(
    GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC,
    bootstrap_servers="kafka:9092",
)


class Producers(Enum):
    CREATE_IMAGE_COLLECTION = 1
    WRITE_CHUNKS = 2
    MERGE_CHUNKS = 3


if __name__ == '__main__':
    chunks_written = set()
    logging.info("Notification | Started sending out process...")
    while True:
        for message in consumer:
            logging.info(f"Notification | Message: {message}")
            consumed_message = json.loads(message.value.decode("utf-8"))
            task_id = consumed_message["task_id"]
            state = consumed_message["state"]

            # This sends messages to:
            # 1. Create image collection
            # 2. Write chunks
            # 3. Merge chunks

            logging.info(f"Notification | State: {state}")
            # 1. Producers.CREATE_IMAGE_COLLECTION
            if state == 1:
                # if state == Producers.CREATE_IMAGE_COLLECTION:
                logging.info("Notification | Creating Image Collection ...")

                create_cube = consumed_message["create_cube"]

                data = dict(
                    task_id=task_id,
                    # state=Producers.CREATE_IMAGE_COLLECTION,
                    state=1,
                    create_cube=dict(
                        format_name=create_cube['format_name'],
                        chunks_name=create_cube['chunks_name'],
                        files_src=create_cube['files_src'],
                        files_dest=create_cube['files_dest'],
                        current_path=create_cube['current_path'],
                    )
                )

                # send messages to kafka topic
                producer.send(GDALCUBESPY_CONSUMER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
                logging.info(f"Notification | Done creating Image Collection ...{data}")

            # 2. Producers.WRITE_CHUNKS
            if state == 2:
                # if state == Producers.WRITE_CHUNKS:
                logging.info("Notification | Writing chunks...")

                write_chunks = consumed_message["write_chunks"]

                # 2.1. Check total of chunks
                total_chunks = write_chunks['total_chunks']
                # cube = write_chunks['cube']

                # 2.2. Publish a message to write each chunk
                for chunk_id in range(total_chunks):
                    data = dict(
                        task_id=task_id,
                        state=2,
                        # state=Producers.WRITE_CHUNKS,
                        write_chunks=dict(
                            chunk_id=chunk_id,
                            # cube=cube,
                        )
                    )

                    # Send message to kafka topic
                    producer.send(GDALCUBESPY_CONSUMER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
                    logging.info(f"Notification - Done writing chunks ...{data}")

            # 3. merge chunks. op1: merge chunk when it finishes. op2: wait until all messages finish.
            # add consumer
            # when all chunks are processed, send other message to join the chunks
            # if state == Producers.MERGE_CHUNKS:
            if state == 3:
                logging.info("Notification - Merging chunks...")
                continue

            time.sleep(1)
