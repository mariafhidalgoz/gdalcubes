//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../code/gdalcubes.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

void init_gdalcubes(py::module &m) {
    py::class_<gdalcubes::gdalcubes>(m, "gdalcubes")
        .def_static("create_image_collection",
                    py::overload_cast<std::vector<std::string>, std::string, std::string>(
                        &gdalcubes::gdalcubes::create_image_collection),
                    py::arg("files"),
                    py::arg("format_file"),
                    py::arg("outfile"))
        .def_static("create_image_collection",
                    py::overload_cast<std::string, std::string, std::string>(
                        &gdalcubes::gdalcubes::create_image_collection),
                    py::arg("input"),
                    py::arg("output"),
                    py::arg("format"))
        .def_static("string_list_from_text_file",
                    py::overload_cast<std::string>(
                        &gdalcubes::gdalcubes::string_list_from_text_file),
                    py::arg("filename"))

        .def_static("raster_cube",
                    py::overload_cast<std::string, std::string>(
                        &gdalcubes::gdalcubes::raster_cube),
                    py::arg("input"),
                    py::arg("output"))

        .def_static("create_image_collection_cube",
                    py::overload_cast<std::string, uint32_t>(
                        &gdalcubes::gdalcubes::create_image_collection_cube),
                    py::arg("input"),
                    py::arg("chunk_size"))
        .def_static("total_chunks",
                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection_cube>>(
                        &gdalcubes::gdalcubes::total_chunks),
                    py::arg("cube"))
        .def_static("is_chunk_empty",
                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection_cube>, gdalcubes::chunkid_t>(
                        &gdalcubes::gdalcubes::is_chunk_empty),
                    py::arg("cube"),
                    py::arg("chunk_id"))

        .def_static("write_chunks_netcdf",
                    py::overload_cast<std::string, std::string>(
                        &gdalcubes::gdalcubes::write_chunks_netcdf),
                    py::arg("input"),
                    py::arg("output"))
        .def_static("write_single_chunk_netcdf",
                    py::overload_cast<std::string, std::string, gdalcubes::chunkid_t, uint32_t, uint32_t, uint32_t>(
                        &gdalcubes::gdalcubes::write_single_chunk_netcdf),
                    py::arg("input"),
                    py::arg("output"),
                    py::arg("chunk_id"),
                    py::arg("t"),
                    py::arg("x"),
                    py::arg("y"))
        .def_static("write_single_chunk_netcdf",
                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection_cube>, std::string, gdalcubes::chunkid_t>(
                        &gdalcubes::gdalcubes::write_single_chunk_netcdf),
                    py::arg("cube"),
                    py::arg("output"),
                    py::arg("chunk_id"))

        .def_static("merge_chunks",
                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection_cube>, std::string, std::string>(
                        &gdalcubes::gdalcubes::merge_chunks),
                    py::arg("cube"),
                    py::arg("work_dir"),
                    py::arg("file_name"));
}
