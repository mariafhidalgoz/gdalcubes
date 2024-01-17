# Creating the producer
import argparse
import json
import os
import time
import uuid
import datetime
from enum import Enum

from kafka import KafkaProducer

GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC = "gdalcubespy-notifications"

producer = KafkaProducer(bootstrap_servers="kafka:9092")


class Producers(Enum):
    CREATE_IMAGE_COLLECTION = 1
    WRITE_CHUNKS = 2
    MERGE_CHUNKS = 3


if __name__ == '__main__':

    # Current path
    os.chdir('.')
    # os.chdir('../')  # For Debug
    path = os.getcwd()
    print(f"PWD: {path}")

    # Creating a temporary directory with the task_id name
    task_id = uuid.uuid4()
    print('task_id: ' + str(task_id))
    temp_folder = f"/tmp/{task_id}"

    # Arguments
    parser = argparse.ArgumentParser(description='Program to produce messages.')
    parser.add_argument("-fn", "--format-name", default="L8_SR", help="Format name")
    parser.add_argument("-cn", "--chunks-name", default="", help="Chunks name")
    parser.add_argument("-src", "--source", default=f"{path}/Python/file_list.txt", help="Files folder or File list.")
    parser.add_argument("-dest", "--destination", default=temp_folder, help="Destination location")
    args = parser.parse_args()
    format_name = args.format_name
    chunks_name = args.chunks_name
    files_src = args.source

    # Define destination folder
    if temp_folder == args.destination:
        files_dest = temp_folder
    else:
        files_dest = args.destination

    # Start process by creating an image collection from file/folder
    data = dict(
        task_id=str(task_id),
        # state=Producers.CREATE_IMAGE_COLLECTION,
        state=1,
        create_cube=dict(
            format_name=format_name,
            chunks_name=chunks_name,
            files_src=files_src,
            files_dest=files_dest,
            current_path=path,
        )
    )

    # send messages to kafka topic
    print(f"Producer | Start sending process ...{data}")
    start_time = time.time()
    start_dt = datetime.datetime.fromtimestamp(start_time)
    producer.send(GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    end_time = time.time()
    end_dt = datetime.datetime.fromtimestamp(end_time)
    print(f"Producer | --- Time start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Producer | --- Time end: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Producer | --- {end_time - start_time} seconds ---")
    print(f"Producer | Done sending process ...{data}")

    # time.sleep(1)
    while True:
        time.sleep(60)
