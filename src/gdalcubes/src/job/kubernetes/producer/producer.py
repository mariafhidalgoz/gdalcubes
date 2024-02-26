# Creating the producer
import argparse
import json
import os
import time
import uuid
import datetime
import logging
from enum import Enum
from pathlib import Path

from gdalcubepy import gdalcubes as gcp
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)

GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC = "gdalcubespy-notifications"
GDALCUBESPY_CONSUMER_KAFKA_TOPIC = "write-netcdf"

producer = KafkaProducer(bootstrap_servers="kafka:9092")


class Producers(Enum):
    CREATE_IMAGE_COLLECTION = 1
    WRITE_CHUNKS = 2
    MERGE_CHUNKS = 3

def utils_log_times(start_time, end_time):
    start_dt = datetime.datetime.fromtimestamp(start_time)
    end_dt = datetime.datetime.fromtimestamp(end_time)
    logging.info(f"Producer | --- Time: {end_time - start_time} seconds. "
                 f"Start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}. "
                 f"End: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} ---")

def gcp_create_image_collection(files_src, output_image_collection, format_ic) -> None:
    logging.info("Producer | Image Collection | Start ...")
    start_time = time.time()
    gcp.create_image_collection(files_src, output_image_collection, format_ic)
    end_time = time.time()
    utils_log_times(start_time, end_time)
    logging.info("Producer | Image Collection | End.")

def gcp_create_cube(output_image_collection, chunk_size):
    logging.info(f"Producer | Cube | Start ...")
    start_time = time.time()
    cube = gcp.create_image_collection_cube(output_image_collection, chunk_size)
    end_time = time.time()
    utils_log_times(start_time, end_time)
    logging.info(f"Producer | Cube | End.")
    return  cube

def get_chunks_with_data(cube, total_chunks) -> list:
    logging.info(f"Producer | Get Chunks with Data | Start ...")
    start_time = time.time()
    chunks_with_data = []
    for chunk_id in range(total_chunks):
        is_chunk_empty = gcp.is_chunk_empty(cube, chunk_id)
        # logging.info(f"Producer | Chunk Id {chunk_id} is empty? -> {is_chunk_empty}.")
        # print(f"Producer | Chunk Id {chunk_id} is empty? -> {is_chunk_empty}.")
        if not is_chunk_empty:
            chunks_with_data.append(chunk_id)
    utils_log_times(start_time, end_time)
    logging.info(f"Producer | Get Chunks with Data | End.")
    return chunks_with_data

if __name__ == '__main__':

    # Current path
    os.chdir('.')
    # os.chdir('../')  # For Debug
    path = os.getcwd()
    logging.info(f"Producer | Main | PWD: {path}")

    # Creating a temporary directory with the task_id name
    task_id = str(uuid.uuid4())
    logging.info(f"Producer | Main | task_id: {task_id}")
    temp_folder = f"/tmp/{task_id}"

    # Arguments
    parser = argparse.ArgumentParser(description='Program to produce messages.')
    parser.add_argument("-fn", "--format-name", default="L8_SR", help="Format name")
    parser.add_argument("-cn", "--chunks-name", default="", help="Chunks name")
    parser.add_argument("-cs", "--size", default="64", help="Size of chunk")
    parser.add_argument("-src", "--source", default=f"{path}/Python/file_list.txt", help="Files folder or File list.")
    parser.add_argument("-dest", "--destination", default=temp_folder, help="Destination location")
    args = parser.parse_args()
    format_name = args.format_name
    chunks_name = args.chunks_name
    chunk_size = int(args.size)
    files_src = args.source

    # Define destination folder
    if temp_folder == args.destination:
        files_dest = temp_folder
    else:
        files_dest = args.destination

    # Create destination dir
    Path(files_dest).mkdir(parents=True, exist_ok=True)

    # Create tag for starting process
    start_time = time.time()
    start_dt = datetime.datetime.fromtimestamp(start_time)
    open(f"{files_dest}/{task_id}_{start_dt.strftime('%Y-%m-%d %H:%M:%S')}.START", 'a').close()

    # Start process by creating an image collection from file/folder
    data = dict(
        task_id=task_id,
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
    logging.info(f"Producer | Main | Starting process ...{data}")
    create_cube = data["create_cube"]
    format_name = create_cube['format_name']
    chunks_name = create_cube['chunks_name']
    files_src = create_cube['files_src']
    files_dest = create_cube['files_dest']
    current_path = create_cube['current_path']
    logging.info(f"Producer | Main | files_src {files_src}")
    logging.info(f"Producer | Main | files_dest {files_dest}")
    logging.info(f"Producer | Main | current_path {current_path}")
    logging.info(f"Producer | Main | format_name {format_name}")

    output_image_collection = f"{files_dest}/image_collection.db"
    # format_ic = f"{current_path}/formats/{format_name}.json"
    format_ic = f"{format_name}.json"

    # Create Image Collection from file
    gcp_create_image_collection(files_src, output_image_collection, format_ic)
    # gcp.create_image_collection("file_list.txt", "new_image_collection.db", "L8_SR.json")

    # Create cube
    cube = gcp_create_cube(output_image_collection, chunk_size)

    # Total chunks in a cube
    total_chunks = gcp.total_chunks(cube)
    logging.info(f"Producer | Main | Total chunks {total_chunks}")

    # 2.2. Publish a message to write each chunk

    # Check chunks with data
    # chunks_with_data = get_chunks_with_data(cube, total_chunks)
    # logging.info(f"Producer | Main | Total chunks with data {len(chunks_with_data)}.")

    # Publish messages
    start_time = time.time()
    for chunk_id in range(total_chunks):
        data = dict(
            task_id=task_id,
            state=2,
            # state=Producers.WRITE_CHUNKS,
            write_chunks=dict(
                chunk_id=chunk_id,
                output_image_collection=output_image_collection,
                chunks_name=chunks_name,
                chunk_size=chunk_size,
                files_dest=files_dest,
                # output_image_collection=output_image_collection,
                # cube=cube,
            )
        )

        # Send message to kafka topic
        producer.send(GDALCUBESPY_CONSUMER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
        # logging.info(f"Producer | Main | Done sending chunk ...{data}")

        # Create tag for chunk
        open(f"{files_dest}/{task_id}_{chunk_id}.PROCESS", 'a').close()

    end_time = time.time()
    utils_log_times(start_time, end_time)
    logging.info(f"Producer | Main | Done processing.")

    # time.sleep(1)
    while True:
        time.sleep(60)
