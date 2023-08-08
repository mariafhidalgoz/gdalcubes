//
// Created by Maria Hidalgo on 18.07.23.
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// #include "../datetime.h"
#include "../view.h"

namespace py = pybind11;

void init_cube_view(py::module &m) {
    py::class_<gdalcubes::cube_view>(m, "cube_view")
        .def(py::init<>())
        .def_static("read_json", py::overload_cast<std::string>(&gdalcubes::cube_view::read_json), py::arg("filename"))
        .def_static("read_json_string", py::overload_cast<std::string>(&gdalcubes::cube_view::read_json_string), py::arg("str"))
        .def("write_json", py::overload_cast<std::string>(&gdalcubes::cube_view::write_json), py::arg("filename"))
        .def("set_x_axis", py::overload_cast<double, double, double>(&gdalcubes::cube_view::set_x_axis),
             py::arg("min"), py::arg("max"), py::arg("delta"))
        .def("set_y_axis", py::overload_cast<double, double, double>(&gdalcubes::cube_view::set_y_axis),
             py::arg("min"), py::arg("max"), py::arg("delta"))
        // .def("set_t_axis", py::overload_cast<gdalcubes::datetime, gdalcubes::datetime, gdalcubes::datetime>
        //     (&gdalcubes::cube_view::set_t_axis),
        //      py::arg("min"), py::arg("max"), py::arg("delta"))
        .def("srs", py::overload_cast<std::string>(&gdalcubes::cube_view::srs), py::arg("_srs"));
}
