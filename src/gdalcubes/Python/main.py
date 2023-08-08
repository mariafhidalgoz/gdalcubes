import os

import gdalcubepy


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


def create_datacube_from_gdalcube_c() -> None:
    os.chdir('../')
    path = os.getcwd()
    print(f"PWD: {path}")
    # Image Collection
    gdalcubepy.gdalcubes.gc_create_image_collection_from_format_test(
        f"{os.getcwd()}/Python/L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
        # f"{os.getcwd()}/Python/L8_Amazon_mini",
        f"{os.getcwd()}/Python/new_image_collection.db",
        f"{os.getcwd()}/formats/L8_SR.json")

    # Raster Cube
    gdalcubepy.gdalcubes.raster_cube(
        f"/Users/maria/GitHub/gdalcubes/src/gdalcubes/Python/new_image_collection.db",
        f"Python/band_select.nc")


if __name__ == '__main__':
    # TODO: Create raster cube
    create_datacube_from_gdalcube_c()
    # TODO: Pointers Error
    # create_datacube_from_gdalcube_py()
