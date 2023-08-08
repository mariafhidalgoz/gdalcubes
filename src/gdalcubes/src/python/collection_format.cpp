//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../collection_format.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_collection_format(py::module &m) {
    py::class_<gdalcubes::collection_format>(m, "collection_format")
        .def(py::init<>())
        .def(py::init<std::string>(), py::arg("filename"))
        .def("is_null",
             py::overload_cast<>(&gdalcubes::collection_format::is_null))
        .def_static("list_presets",
             py::overload_cast<>(&gdalcubes::collection_format::list_presets))
        .def("load_file",
             py::overload_cast<std::string>(&gdalcubes::collection_format::load_file),
             py::arg("filename"))
        .def("load_string",
             py::overload_cast<std::string>(&gdalcubes::collection_format::load_string),
             py::arg("jsonstr"));
}
