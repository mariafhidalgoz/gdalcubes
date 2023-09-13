import argparse
import os
import uuid
from pathlib import Path

import gdalcubepy
import netCDF4


def create_datacube_from_gdalcube_py():
    # Collection Format
    format_str = "/Users/maria/GitHub/gdalcubes/src/gdalcubes/formats/L8_SR.json"
    cf = gdalcubepy.collection_format(format_str)
    collection_is_null = cf.is_null()
    if collection_is_null:
        print(f"ERROR: Creating Collection {format_str}.")
    else:
        print(f"Collection {format_str} created.")

    # cf = gdalcubepy.collection_format()
    # cf.load_file(format_str)
    # cf.is_null()

    # "/Users/maria/Documents/thesis/L8_Amazon_mini/LC082260632014071901T1-SC20190715045926/LC08_L1TP_226063_20140719_20170421_01_T1_pixel_qa.tif"

    d = gdalcubepy.filesystem.is_directory(".")
    w = gdalcubepy.filesystem.get_working_dir()
    d2 = gdalcubepy.filesystem.is_directory("L8_Amazon_mini/LC082260632014071901T1-SC20190715045926")

    # Image Collection
    list_files = ["./L8_Amazon_mini/LC082290642019031601T2-SC20190715045938/"]
    ic = gdalcubepy.image_collection()
    ic.create(cf, list_files, False)
    ic.write("./new_image_collection.db")


def show_data():
    f = netCDF4.Dataset('results/complete_netcdf.nc')
    print(f)
    print(f.variables.keys())  # get all variable names
    B04 = f.variables['B04']  # temperature variable
    print(B04)
    print(B04.dimensions)
    print(B04.shape)
    # # for d in f.dimensions.items():
    # #     print(d)
    # times = f.variables["B04"]  # time coord var
    # print('units = %s, values = %s' % (times.x, times[:]))

    # import matplotlib.pyplot as plt
    # %matplotlib
    # inline
    # cs = plt.contourf(soilm)

    bs = netCDF4.Dataset('results/single_chunk.nc')
    print(bs)
    print(bs.variables.keys())  # get all variable names
    B04 = bs.variables['B04']  # temperature variable
    print(B04)
    print(B04.dimensions)
    print(B04.shape)


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
    parser = argparse.ArgumentParser(description='Program to work with gdalcubes.')
    parser.add_argument("-fn", "--format-name", default="L8_SR", help="Format name")
    parser.add_argument("-cn", "--chunks-name", default="", help="Chunks name")
    parser.add_argument("-src", "--source", default=f"{path}/Python/file_list.txt", help="Files folder or File list.")
    # parser.add_argument("-src", "--source", default=f"{path}/Python/L8_Amazon_mini", help="Files folder or File list.")
    parser.add_argument("-dest", "--destination", default=temp_folder, help="Destination location")
    args = parser.parse_args()
    format_name = args.format_name
    chunks_name = args.chunks_name
    files_src = args.source
    print(f"files_src {files_src}")

    # Define destination folder
    if temp_folder == args.destination:
        files_dest = temp_folder
    else:
        files_dest = args.destination
    Path(files_dest).mkdir(parents=True, exist_ok=True)

    # Create Image Collection from file
    output_image_collection = f"{files_dest}/image_collection.db"
    format_ic = f"{path}/formats/{format_name}.json"
    gdalcubepy.gdalcubes.create_image_collection(files_src, output_image_collection, format_ic)

    # Create cube
    cube = gdalcubepy.gdalcubes.create_image_collection_cube(output_image_collection)

    # Chunks number of a cube
    total_chunks = gdalcubepy.gdalcubes.total_chunks(cube)

    # Write single chunk netcdf
    for chunk_id in range(total_chunks):
        is_chunk_empty = gdalcubepy.gdalcubes.is_chunk_empty(cube, chunk_id)
        print(f"Chunk Id {chunk_id} is empty {is_chunk_empty}.")
        if not is_chunk_empty:
            output_chunk = f"{files_dest}/{chunks_name}{chunk_id}.nc"
            gdalcubepy.gdalcubes.write_single_chunk_netcdf(cube, output_chunk, chunk_id)

    # show_data()

    # TODO: Pointers Error
    # create_datacube_from_gdalcube_py()
