//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../image_collection.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

void init_image_collection(py::module &m) {
    py::class_<gdalcubes::image_collection>(m, "image_collection")
        .def(py::init<>())
        .def(py::init<std::string>(), py::arg("filename"))
        .def(py::init<gdalcubes::collection_format>(), py::arg("format"))
        .def_static("create",
                    py::overload_cast<>(&gdalcubes::image_collection::create))
        .def_static("create",
                    py::overload_cast<gdalcubes::collection_format, std::vector<std::string>, bool>(&gdalcubes::image_collection::create),
                    py::arg("format"), py::arg("descriptors"), py::arg("strict"))
        //            .def("string_list_from_text_file",
        //                 py::overload_cast<std::string>(&gdalcubes::image_collection::string_list_from_text_file),
        //                 py::arg("filename"))
        //            .def("gc_create_image_collection_from_format",
        //                 py::overload_cast<std::vector<std::string>,std::string,std::string> (&gdalcubes::image_collection::gc_create_image_collection_from_format),
        //                         py::arg("files"),
        //                         py::arg("format_file"),
        //                         py::arg("outfile"))
        //            .def("gc_create_image_collection_from_format_2",
        //                 py::overload_cast<std::string,std::string,std::string> (&gdalcubes::image_collection::gc_create_image_collection_from_format_2),
        //                     py::arg("input"),
        //                     py::arg("output"),
        //                     py::arg("format"))
        .def("is_empty",
             py::overload_cast<>(&gdalcubes::image_collection::is_empty))
        .def("write",
             py::overload_cast<std::string>(&gdalcubes::image_collection::write),
             py::arg("filename"));
}
