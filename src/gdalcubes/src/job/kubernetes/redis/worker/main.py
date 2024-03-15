"""
------------------------------------------------------------------------
Worker Instance.

Workers listen to the redis queue and process messages.


: 08.11.23
: zach wolpe
: zach.wolpe@medibio.com.au
------------------------------------------------------------------------
"""

import  config
import  random
import  json
import time
import datetime
import logging
import os
import glob

from gdalcubepy import gdalcubes as gcp
from redis_module import redis_access

logging.basicConfig(level=logging.INFO)



def utils_log_times(start_time, end_time) -> str:
    start_dt = datetime.datetime.fromtimestamp(start_time)
    end_dt = datetime.datetime.fromtimestamp(end_time)
    return (f"{end_time - start_time},"
            f"{start_dt.strftime('%Y-%m-%d %H:%M:%S')},"
            f"{end_dt.strftime('%Y-%m-%d %H:%M:%S')}")

def are_chunks_in_progress(files_dest):
    any_file_in_progres = any(glob.glob(f"{files_dest}/*.PROCESS"))
    if any_file_in_progres:
        logging.info(f"Consumer | Are chunks in progress? | True.")
        return True
    logging.info(f"Consumer | Are chunks in progress? | False.")
    return False

def gcp_merge(cube, files_dest):
    logging.info("Consumer | Merge | Start...")
    start_time = time.time()
    # cube = gcp.create_image_collection_cube(
    #     f"{os.getcwd()}/Python/results/new_image_collection_from_txt_file.db")

    # output_merge = "Python/results/test3"
    output_merge = f"{files_dest}"
    logging.info(f"Consumer | Merge | Folder {output_merge}")

    output_file_merge = "result"
    logging.info(f"Consumer | Merge | File {output_file_merge}")

    # gcp.merge_chunks(cube, f"Python/results/test5", "result")
    gcp.merge_chunks(cube, output_merge, output_file_merge)
    end_time = time.time()

    log_duration = utils_log_times(start_time, end_time)
    logging.info(f"Consumer | Merge | seconds,start,end | {log_duration}")
    logging.info(f"Consumer | Merge | End.")


def process_message(db, message_json: str):
    message = json.loads(message_json)
    logging.info(f"Message received: id={message['id']}, message_number={message['data']['message_no']}")
    print(f"Message received: id={message['id']}, message_number={message['data']['message_no']}")

    # # mimic potential processing errors
    # processed_ok = random.choices((True, False), weights=(5, 1), k=1)[0]
    # if processed_ok:
    #     logging.info("\t>> Processed successfully.")
    #     print("\t>> Processed successfully.")
    # else:
    #     logging.info("\tProcessing failed - requeuing...")
    #     print("\tProcessing failed - requeuing...")
    #     redis_access.redis_queue_push(config, db, message_json)

    consumed_message = json.loads(message_json)
    task_id = consumed_message["task_id"]

    logging.info("Consumer | Main | Writing chunks...")
    write_chunks = consumed_message["write_chunks"]

    chunk_id = write_chunks['chunk_id']
    output_image_collection = write_chunks['output_image_collection']
    files_dest = write_chunks['files_dest']
    chunks_name = write_chunks['chunks_name']
    chunk_size = write_chunks['chunk_size']
    # celery_task_write_chunk.delay(task_id, chunk_id)

    # Dont process again if the state is SUCCESS
    file_success = f"{files_dest}/{task_id}_{chunk_id}.SUCCESS"
    if os.path.exists(file_success):
        logging.info(f"Consumer | Main | Duplicated message | {message}")
        if file_success.split(".")[-1].strip("SUCCESS") == "":
            count = 1
        else:
            count = int(file_success.split(".")[-1].strip("SUCCESS")) + 1
        # os.rename(file_success, f"{files_dest}/{task_id}_{chunk_id}.SUCCESS{count}")
        logging.info(f"Consumer | Main | Duplicated message | {task_id}_{chunk_id} | count {count}")
        os.rename(file_success, f"{files_dest}/{task_id}_{chunk_id}.SUCCESS_MORE")
        # continue

    # cube = write_chunks['cube']
    cube = gcp.create_image_collection_cube(output_image_collection, chunk_size)

    # Write single chunk netcdf
    is_chunk_empty = gcp.is_chunk_empty(cube, chunk_id)
    logging.info(f"Consumer | Main | Chunk Id {chunk_id} is empty {is_chunk_empty}.")
    start_time = time.time()
    if not is_chunk_empty:
        logging.info(f"Consumer | Main | Start processing Chunk Id {chunk_id} ...")
        output_chunk = f"{files_dest}/{chunks_name}{chunk_id}.nc"
        gcp.write_single_chunk_netcdf(cube, output_chunk, chunk_id)
        logging.info(f"Consumer | Main | Chunk Id {chunk_id} processed")
    end_time = time.time()
    log_duration = utils_log_times(start_time, end_time)
    logging.info(f"Consumer | Main | seconds,start,end | {log_duration}")

    # Write processed chunk
    with open(f"{files_dest}/report_{task_id}_{chunk_id}.txt", "a") as report:
        report.write(f"{task_id},"
                     f"{chunk_id},"
                     f"{is_chunk_empty},"
                     f"{log_duration}\n")

    file_in_process = f"{files_dest}/{task_id}_{chunk_id}.PROCESS"
    if os.path.exists(file_in_process):
        os.rename(file_in_process, file_success)

    logging.info(f"Consumer | Main | End.")

    if not are_chunks_in_progress(files_dest):
        logging.info(f"Consumer | Merging | Start ...")
        gcp_merge(cube, files_dest)
        # Create tag for ending process
        end_time = time.time()
        end_dt = datetime.datetime.fromtimestamp(end_time)
        open(f"{files_dest}/{task_id}_{end_dt.strftime('%Y-%m-%d %H:%M:%S')}.END", 'a').close()
        logging.info(f"Consumer | Merging | End.")


def main():
    """
    Consumes items from the Redis queue.
    """

    # connect to Redis
    db = redis_access.redis_db(config)

    while True:
        message_json = redis_access.redis_queue_pop(config, db)  # this blocks until an item is received
        process_message(db, message_json)


if __name__ == '__main__':
    logging.info("Launching worker...")
    print('Launching worker...')
    main()
    logging.info("Worker terminated successfully.")
    print('Worker terminated successfully.')