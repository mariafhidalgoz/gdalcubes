//
// Created by Maria Hidalgo on 18.07.23.
//

#include <pybind11/pybind11.h>

#include "../dummy.h"

namespace py = pybind11;

void init_dummy_view(py::module &m) {
//    py::class_<gdalcubes::dummy_cube, gdalcubes::cube>(m, "dummy_cube")
//        .def(py::init<cube_view, uint16_t, double>(), py::arg("v"), py::arg("nbands"), py::arg("nbands"));
}
