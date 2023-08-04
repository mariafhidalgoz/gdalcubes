//
// Created by Maria Hidalgo on 18.07.23.
//

#include <pybind11/pybind11.h>

#include "../motorcycle.h"

namespace py = pybind11;


void init_example_pybind11(py::module &m) {

    py::class_<gdalcubes::Motorcycle>(m, "Motorcycle")
            .def(py::init<std::string>(), py::arg("name"))
            .def(py::init<>())
            .def("get_name",
                 py::overload_cast<>(&gdalcubes::Motorcycle::get_name, py::const_))
            .def("create",
                 py::overload_cast<>(&gdalcubes::Motorcycle::create, py::const_))
            .def_static("create2",
                        py::overload_cast<>(&gdalcubes::Motorcycle::create2))
            .def("ride",
                 py::overload_cast<std::string, std::string>(&gdalcubes::Motorcycle::ride, py::const_),
                 py::arg("road"), py::arg("road2"))
            .def("load_file",
                 py::overload_cast<std::string>(&gdalcubes::Motorcycle::load_file),
                 py::arg("filename"));

}

