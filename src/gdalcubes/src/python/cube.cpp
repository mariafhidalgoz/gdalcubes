//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../cube.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_cube(py::module &m) {
    py::class_<gdalcubes::cube, std::shared_ptr<gdalcubes::cube>>(m, "cube");
    //    .def(py::init<>());
    //    .def(py::init<std::shared_ptr<gdalcubes::cube_stref>>(), py::arg("st_ref"));
    //    .def("make_constructible_json", &gdalcubes::cube::make_constructible_json);
}
