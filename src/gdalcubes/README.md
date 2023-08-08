
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
python
```


```python
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
import gdalcubepy

# gdalcubes: Image Collection
gdalcubepy.gdalcubes.gc_create_image_collection_from_format_test(
    f"{os.getcwd()}/Python/L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    f"{os.getcwd()}/Python/new_image_collection.db",
    f"{os.getcwd()}/formats/L8_SR.json")
# gdalcubepy.gdalcubes.gc_create_image_collection_from_format(
#     [f"{os. getcwd()}/Python/L8_Amazon_mini/LC082290632016072901T1-SC20190715045704"],
#     f"{os. getcwd()}/formats/L8_SR.json",
#     f"{os. getcwd()}/Python/new_image_collection.db")
# gdalcubes: Raster Cube
gdalcubepy.gdalcubes.raster_cube(
    f"{os.getcwd()}/Python/L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    f"Python/band_select_2.nc",
    f"{os.getcwd()}/formats/L8_SR.json")
```

Deactivate environment
```shell
deactivate
```
