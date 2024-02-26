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
import logging

from redis_module import redis_access

logging.basicConfig(level=logging.INFO)


def process_message(db, message_json: str):
    message = json.loads(message_json)
    logging.info(f"Message received: id={message['id']}, message_number={message['data']['message_no']}")
    print(f"Message received: id={message['id']}, message_number={message['data']['message_no']}")

    # mimic potential processing errors
    processed_ok = random.choices((True, False), weights=(5, 1), k=1)[0]
    if processed_ok:
        logging.info("\t>> Processed successfully.")
        print("\t>> Processed successfully.")
    else:
        logging.info("\tProcessing failed - requeuing...")
        print("\tProcessing failed - requeuing...")
        redis_access.redis_queue_push(config, db, message_json)


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