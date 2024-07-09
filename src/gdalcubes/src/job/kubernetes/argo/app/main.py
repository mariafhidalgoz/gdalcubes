"""
------------------------------------------------------------------------
Main application file.

Push messages to into the redis queue.


: 08.11.23
: zach wolpe
: zach.wolpe@medibio.com.au
------------------------------------------------------------------------
"""

import argparse
import datetime
import json
import logging
import os
import random
import time
import uuid
from gdalcubepy import gdalcubes as gcp
from pathlib import Path

logging.basicConfig(level=logging.INFO)


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
    return cube


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


def main():
    """
    Generate random messages and push to redis queue.

    Arguments:
        num_messages: number of messages to generate

    Return: None
    """

    # Current path
    os.chdir('.')
    # os.chdir('../')  # For Debug
    current_path = os.getcwd()
    logging.info(f"Producer | Main | PWD: {current_path}")

    # Creating a temporary directory with the task_id name
    task_id = str(uuid.uuid4())
    logging.info(f"Producer | Main | task_id: {task_id}")
    temp_folder = f"/tmp/{task_id}"

    # Arguments
    parser = argparse.ArgumentParser(description='Program to produce messages.')
    parser.add_argument("-fn", "--format-name", default="L8_SR", help="Format name")
    parser.add_argument("-cn", "--chunks-name", default="", help="Chunks name")
    parser.add_argument("-cs", "--size", default="64", help="Size of chunk")
    parser.add_argument("-src", "--source", default=f"{current_path}/Python/file_list.txt", help="Files folder or File list.")
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
    logging.info(f"Producer | Main | Starting process ...")
    logging.info(f"Producer | Main | format_name {format_name}")
    logging.info(f"Producer | Main | chunks_name {chunks_name}")
    logging.info(f"Producer | Main | files_src {files_src}")
    logging.info(f"Producer | Main | files_dest {files_dest}")
    logging.info(f"Producer | Main | current_path {current_path}")

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
        message = dict(
            task_id=task_id,
            write_chunks=dict(
                chunk_id=chunk_id,
                output_image_collection=output_image_collection,
                chunks_name=chunks_name,
                chunk_size=chunk_size,
                files_dest=files_dest,
                # cube=cube,
            )
        )

        # Save message
        message_json = json.dumps(message)

        file_name = f"{files_dest}/{task_id}_{chunk_id}.txt"
        f = open(file_name, 'w+')  # open file in write mode
        f.write(message_json)
        f.close()

        # push to redis queue
        # _msg_sample = message['write_chunks'][:4] + '...'
        # logging.info(f'Pushing message number {chunk_id} (id: {chunk_id}): message={_msg_sample}')

        # Create tag for chunk
        open(f"{files_dest}/{task_id}_{chunk_id}.PROCESS", 'a').close()

    end_time = time.time()
    utils_log_times(start_time, end_time)
    logging.info(f"Producer | Main | Done processing.")


if __name__ == '__main__':
    print('Launching main application...')
    main()
    print('Main application completed.')
