#!/usr/bin/env python

import os
import time

import gdalcubepy

import rediswq

host = "redis"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_HOST")
print(f"Host {host}")

q = rediswq.RedisWQ(name="job2", host=host)
print("Worker with sessionID: " + q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
while not q.empty():
    item = q.lease(lease_secs=10, block=True, timeout=2)
    if item is not None:
        itemstr = item.decode("utf-8")  # Send the ide of the chunk
        print(f"Working on {itemstr}")
        print(f"Chunk {int(itemstr)}")
        print(f"Path CWD {os.getcwd()}")
        # # Image Collection
        # gdalcubepy.gdalcubes.gc_create_image_collection_from_format_all(
        #     f"{os.getcwd()}/file_list.txt",
        #     f"{os.getcwd()}/new_image_collection_from_file.db",
        #     f"/opt/gdalcubes/formats/L8_SR.json")
        # Write single chunk netcdf
        gdalcubepy.gdalcubes.write_single_chunk_netcdf(
            f"{os.getcwd()}/new_image_collection_from_file.db",
            f"single_chunk_{int(itemstr)}.nc",
            int(itemstr)
        )
        time.sleep(1000)  # Put your actual work here instead of sleep.
        q.complete(item)
    else:
        print("Waiting for work")
print("Queue empty, exiting")
