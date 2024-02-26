# Creating the consumer to process the data
# Creating the producer to notify the status of the process
import json
import logging
import time
import datetime
from enum import Enum
import os
import glob
# from pathlib import Path

from gdalcubepy import gdalcubes as gcp
# from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(level=logging.INFO)

GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC = "gdalcubespy-notifications"
GDALCUBESPY_CONSUMER_KAFKA_TOPIC = "write-netcdf"

# admin_client = KafkaAdminClient(
#     bootstrap_servers="kafka:9092",
#     # client_id='test'
# )
#
# topic_list = []
# topic_list.append(NewTopic(name=GDALCUBESPY_CONSUMER_KAFKA_TOPIC, num_partitions=6, replication_factor=1))
# admin_client.create_topics(new_topics=topic_list, validate_only=False)

producer = KafkaProducer(bootstrap_servers="kafka:9092")

consumer = KafkaConsumer(
    GDALCUBESPY_CONSUMER_KAFKA_TOPIC,
    bootstrap_servers="kafka:9092",
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='blog_group',
    max_poll_records=1,
    max_poll_interval_ms=30000,
    connections_max_idle_ms=1080000,  # 18 minutes
    session_timeout_ms=25000,
    group_initial_rebalance_delay_ms=120000
)


class Producers(Enum):
    CREATE_IMAGE_COLLECTION = 1
    WRITE_CHUNKS = 2
    MERGE_CHUNKS = 3

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

def gcp_merge(cube):
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

if __name__ == '__main__':
    logging.info("Consumer | Main | Started chunks processor...")
    while True:
        for message in consumer:
            logging.info(f"Consumer | Main | "
                         f"Topic = {message.topic} - "
                         f"Partition = {message.partition} - "
                         f"Offset = {message.offset} - "
                         f"key = {message.key} - "
                         f"value = {message.value} - ")
            consumed_message = json.loads(message.value.decode("utf-8"))
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
                continue

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
            with open(f"{files_dest}/report_{task_id}_{message.partition}.txt", "a") as report:
                report.write(f"{task_id},"
                         f"{message.partition},"
                         f"{chunk_id},"
                         f"{is_chunk_empty},"
                         f"{log_duration}\n")

            file_in_process = f"{files_dest}/{task_id}_{chunk_id}.PROCESS"
            if os.path.exists(file_in_process):
                os.rename(file_in_process, file_success)

            logging.info(f"Consumer | Main | End.")

            if not are_chunks_in_progress(files_dest):
                logging.info(f"Consumer | Merging | Start ...")
                gcp_merge(cube)
                # Create tag for ending process
                end_time = time.time()
                end_dt = datetime.datetime.fromtimestamp(end_time)
                open(f"{files_dest}/{task_id}_{end_dt.strftime('%Y-%m-%d %H:%M:%S')}.END", 'a').close()

            # data = dict(
            #     task_id=task_id,
            #     state=3,
            #     # state=Producers.MERGE_CHUNKS,
            #     merge_chunks=dict(
            #         chunk_id=chunk_id,
            #     )
            # )

            # send messages to kafka topic
            # producer.send(GDALCUBESPY_NOTIFICATIONS_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
            # logging.info(f"Consumer | Done writing chunk ...{data}")

            # # if state == Producers.MERGE_CHUNKS:
            # if state == 3:
            #     logging.info("Consumer S-3 | Merging chunks...")
            #     # cube = gcp.create_image_collection_cube(
            #     #     f"{os.getcwd()}/Python/results/new_image_collection_from_txt_file.db")
            #     total_chunks = gcp.total_chunks(cube)
            #     logging.info(f"Consumer S-3  | Total chunks {total_chunks}")
            #
            #     # output_merge = "Python/results/test3"
            #     output_merge = f"{files_dest}"
            #     logging.info(f"Consumer S-3  | Folder {output_merge}")
            #
            #     output_file_merge = "result"
            #     logging.info(f"Consumer S-3  | File {output_file_merge}")
            #
            #     # gcp.merge_chunks(cube, f"Python/results/test5", "result")
            #     gcp.merge_chunks(cube, output_merge, output_file_merge)
            #     logging.info(f"Consumer | Done merging chunks ...{data}")
            #
            #     # continue

    # consumer.close()
