
Create environment
```shell
virtualenv --python=python3.10 .venv
```

```shell
mkdir build
cd build
```

```shell
make clean
```

```shell
cd build
cmake .. \
-DPYTHON_LIBRARY_DIR="/Users/maria/GitHub/gdalcubes/src/gdalcubes/.venv/lib/python3.10/site-packages" \
-DPYTHON_EXECUTABLE="/Users/maria/GitHub/gdalcubes/src/gdalcubes/.venv/bin/python3.10" \
-DCMAKE_INSTALL_PREFIX=/usr/local/ -DCMAKE_BUILD_TYPE=Release
make -j 2
make install
```

```shell
cmake .. -DPYTHON_LIBRARY_DIR="/Users/maria/GitHub/gdalcubes/src/gdalcubes/.venv/lib/python3.10/site-packages" -DPYTHON_EXECUTABLE="/Users/maria/GitHub/gdalcubes/src/gdalcubes/.venv/bin/python3.10" -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Debug && make -j 2 && make install
```


Activate environment
```shell
source .venv/bin/activate
```

```shell
python Python/main.py -dest "/Users/maria/GitHub/gdalcubes/src/gdalcubes/Python/results/new_result"
```

```shell
python Python/main.py -dest "/Users/maria/GitHub/gdalcubes/src/gdalcubes/Python/results/new_result" \
    -src "/Users/maria/GitHub/gdalcubes/src/gdalcubes/Python/L8_Amazon_mini"
```

```shell
python
```


```python step by step in python | ERROR: Pointers
import gdalcubepy
import os
# Collection Format
format_str = f"{os.getcwd()}/formats/L8_SR.json"
cf = gdalcubepy.collection_format(format_str)
collection_is_null = cf.is_null()
if collection_is_null:
    print(f"ERROR: Creating Collection {format_str}.")
else:
    print(f"Collection {format_str} created.")

# Image Collection
list_files = ["/Users/maria/Documents/thesis/L8_Amazon_mini/LC082290642019031601T2-SC20190715045938/"]
ic = gdalcubepy.image_collection()
ic.create(cf, list_files, False)
ic.write("./new_image_collection.db")

# Cube view
cv = gdalcubepy.cube_view()
cv.srs("EPSG:3857")
cv.set_x_axis(-6180000.0, -6080000.0, 1000.0)
cv.set_y_axis(-550000.0, -450000.0, 1000.0)
# cv.set_t_axis(datetime::from_string("2014-01-01"), datetime::from_string("2014-12-31"), duration::from_string("P1D"));

from datetime import datetime
datetime_str = '14-01-01'
datetime_object = datetime.strptime(datetime_str, '%y-%m-%d')


# Raster Cube
icc = gdalcubepy.image_collection_cube(ic)
# raster_cube(L8.col, v)

# Select Bands
# gc_create_select_bands_cube
# L8.cube = select_bands(raster_cube(L8.col, v), c("B04", "B05"))

# Create field with NDVI
# L8.ndvi = apply_pixel(L8.cube, "(B05-B04)/(B05+B04)", "NDVI") 

# Create ncdf_cube
# ncdf_cube

# Plot ncdf_cube
# https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/

# exmaple in R
#' L8.col = image_collection(file.path(tempdir(), "L8.db"))
#' v = cube_view(extent=list(left=388941.2, right=766552.4, 
#'               bottom=4345299, top=4744931, t0="2018-04", t1="2018-06"),
#'               srs="EPSG:32618", nx = 497, ny=526, dt="P1M")
#'               
#' plot(select_bands(raster_cube(L8.col, v), c("B02", "B03", "B04")), rgb=3:1)
#'               
#' L8.cube = select_bands(raster_cube(L8.col, v), c("B04", "B05")) 
#' L8.ndvi = apply_pixel(L8.cube, "(B05-B04)/(B05+B04)", "NDVI") 
#' plot(reduce_time(L8.ndvi, "median(NDVI)"), key.pos=1, zlim=c(0,1))
```

```python 
import os
from gdalcubepy import gdalcubes as gcp

# gdalcubes: Image Collection
# From a txt file
gcp.create_image_collection(
    f"{os.getcwd()}/Python/file_list.txt",
    f"{os.getcwd()}/Python/results/new_image_collection_from_txt_file.db",
    f"{os.getcwd()}/formats/L8_SR.json")
# From folder
gcp.create_image_collection(
    f"{os.getcwd()}/Python/L8_Amazon_mini",
    f"{os.getcwd()}/Python/results/new_image_collection_from_folder.db",
    f"{os.getcwd()}/formats/L8_SR.json")
# List from txt file 
gcp.string_list_from_text_file(
    f"{os.getcwd()}/Python/file_list.txt")


# gdalcubes: Raster Cube
gcp.raster_cube(
    f"{os.getcwd()}/Python/results/new_image_collection_from_folder.db",
    f"Python/results/netcdf_180_images.nc")

# Create cube
cube = gcp.create_image_collection_cube(
    f"{os.getcwd()}/Python/results/new_image_collection_from_file.db")
# Chunks number of a cube
gcp.total_chunks(cube)

# Write chunks netcdf
gcp.write_chunks_netcdf(
    f"{os.getcwd()}/Python/results/new_image_collection_from_file.db",
    "Python/results/"
)
# Write single chunk netcdf
# From db file
gcp.write_single_chunk_netcdf(
    f"{os.getcwd()}/Python/results/new_image_collection_from_file.db",
    f"Python/results/single_chunk_3.nc",
    3
)
# From python cube
gcp.write_single_chunk_netcdf(
    cube,
    f"Python/results/single_chunk_3.nc",
    3
)

# Merge chunks netcdf
import os
from gdalcubepy import gdalcubes as gcp
cube = gcp.create_image_collection_cube(
    f"{os.getcwd()}/Python/results/new_image_collection_from_txt_file.db")
gcp.total_chunks(cube)
gcp.merge_chunks(cube, f"Python/results/test3")

```

Deactivate environment
```shell
deactivate
```


**Docker** 

Build image
```shell
docker build -t gdalcubepy -f DockerfilePython .
```

Run container
```shell
docker run -t gdalcubepy
```

Activate environment
```shell
. /opt/gdalcubes/.venv/bin/activate
```

Test library in container
```python
import gdalcubepy
```

Push the image to Docker Hub
```shell
docker tag gdalcubepy mafehiza/gdalcubepy
docker push mafehiza/gdalcubepy
```
