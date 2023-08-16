import os

import gdalcubepy
import netCDF4
import numpy as np


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


def create_datacube() -> None:
    os.chdir('../')
    path = os.getcwd()
    print(f"PWD: {path}")
    # # Image Collection
    # gdalcubepy.gdalcubes.gc_create_image_collection_from_format_all(
    #     f"{os.getcwd()}/Python/L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    #     # f"{os.getcwd()}/Python/L8_Amazon_mini",
    #     f"{os.getcwd()}/Python/results/new_image_collection.db",
    #     f"{os.getcwd()}/formats/L8_SR.json")
    # # Image Collection from file
    gdalcubepy.gdalcubes.gc_create_image_collection_from_format_all(
        f"{os.getcwd()}/Python/file_list.txt",
        f"{os.getcwd()}/Python/results/new_image_collection_from_file.db",
        f"{os.getcwd()}/formats/L8_SR.json")


def create_raster_cube() -> None:
    # Raster Cube
    gdalcubepy.gdalcubes.raster_cube(
        f"{os.getcwd()}/results/new_image_collection_from_file.db",
        "results/complete_netcdf.nc")


def write_chunks_netcdf() -> None:
    # Write chunks netcdf
    gdalcubepy.gdalcubes.write_chunks_netcdf(
        f"{os.getcwd()}/results/new_image_collection_from_file.db",
        "results/",
        1
    )


def write_single_netcdf() -> None:
    # Write single chunk netcdf
    gdalcubepy.gdalcubes.write_single_chunk_netcdf(
        f"{os.getcwd()}/results/new_image_collection_from_file.db",
        f"{os.getcwd()}/results/single_chunk.nc",
        1
    )


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

    # TODO: Create data cube
    # create_datacube()
    # TODO: Create raster cube
    create_raster_cube()
    # TODO: Write chunks
    write_chunks_netcdf()
    # TODO: Single chunks
    write_single_netcdf()

    show_data()


    # TODO: Pointers Error
    # create_datacube_from_gdalcube_py()