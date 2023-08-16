//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../code/gdalcubes.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_gdalcubes(py::module &m) {
    py::class_<gdalcubes::gdalcubes>(m, "gdalcubes")
        .def_static("gc_create_image_collection_from_format",
                    py::overload_cast<std::vector<std::string>, std::string, std::string>(
                        &gdalcubes::gdalcubes::gc_create_image_collection_from_format),
                    py::arg("files"),
                    py::arg("format_file"),
                    py::arg("outfile"))
        .def_static("gc_create_image_collection_from_format_all",
                    py::overload_cast<std::string, std::string, std::string>(
                        &gdalcubes::gdalcubes::gc_create_image_collection_from_format_all),
                    py::arg("input"),
                    py::arg("output"),
                    py::arg("format"))
        .def_static("raster_cube",
                    py::overload_cast<std::string, std::string>(
                        &gdalcubes::gdalcubes::raster_cube),
                    py::arg("input"),
                    py::arg("output"))
        .def_static("write_chunks_netcdf",
                    py::overload_cast<std::string, std::string, uint16_t>(
                        &gdalcubes::gdalcubes::write_chunks_netcdf),
                    py::arg("input"),
                    py::arg("output"),
                    py::arg("nthreads"))
        .def_static("write_single_chunk_netcdf",
                    py::overload_cast<std::string, std::string, gdalcubes::chunkid_t>(
                        &gdalcubes::gdalcubes::write_single_chunk_netcdf),
                    py::arg("input"),
                    py::arg("output"),
                    py::arg("chunk_id"));
}
