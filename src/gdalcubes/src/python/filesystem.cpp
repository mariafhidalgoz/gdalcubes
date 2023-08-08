//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../filesystem.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_filesystem(py::module &m) {
    py::class_<gdalcubes::filesystem>(m, "filesystem")
        .def_static("is_directory",
                    py::overload_cast<std::string>(&gdalcubes::filesystem::is_directory),
                    py::arg("p"))
        .def_static("get_working_dir",
                    py::overload_cast<>(&gdalcubes::filesystem::get_working_dir));
}
