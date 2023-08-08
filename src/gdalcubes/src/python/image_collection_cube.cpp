//
// Created by Maria Hidalgo on 18.07.23.
//

#include "../image_collection_cube.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

//#define PYBIND11_DECLARE_HOLDER_TYPE(type, holder_type) \
//    namespace pybind11 { namespace detail { \
//    template <typename type> \
//    class type_caster<holder_type, enable_if_t<!is_shared_ptr<holder_type>::value>> \
//        : public type_caster_holder<type, holder_type> { }; \
//    }}

//#define PYBIND11_DECLARE_HOLDER_TYPE(type, holder_type) \
//    namespace pybind11 { namespace detail { \
//    template <typename type> \
//    class type_caster<holder_type, enable_if_t<!is_shared_ptr<holder_type>::value>> \
//        : public type_caster_holder<type, holder_type> { }; \
//    }}

//PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>)

namespace py = pybind11;

void init_image_collection_cube(py::module &m) {

//    py::class_<gdalcubes::image_collection_cube, gdalcubes::cube>(m, "image_collection_cube");
    py::class_<gdalcubes::cube, std::shared_ptr<gdalcubes::cube>, gdalcubes::image_collection_cube>(m, "image_collection_cube")
//    py::class_<gdalcubes::image_collection_cube, std::enable_shared_from_this<gdalcubes::cube>>(m, "image_collection_cube");
//    py::class_<gdalcubes::image_collection_cube, gdalcubes::cube, std::shared_ptr<gdalcubes::cube>>(m, "image_collection_cube");
//        .def(py::init<>());
            .def(py::init<std::shared_ptr<gdalcubes::image_collection>, gdalcubes::cube_view>(),
                 py::arg("ic"), py::arg("v"))
            .def(py::init<std::shared_ptr<gdalcubes::image_collection>>(),
                 py::arg("ic"));
    //        .def(py::init<std::string, gdalcubes::cube_view>(),
    //             py::arg("icfile"), py::arg("v"));
    //        .def(py::init<std::shared_ptr<gdalcubes::image_collection>, gdalcubes::cube_view>(),
    //             py::arg("ic"), py::arg("v"));
    //        .def(py::init<std::shared_ptr<gdalcubes::image_collection>>(), py::arg("ic"));
    //            .def(py::init<std::string>(), py::arg("filename"))
    //            .def(py::init<gdalcubes::image_collection, gdalcubes::c>(), py::arg("ic"), py::arg("v"));
    //        .def_static("create",
    //                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection>, gdalcubes::cube_view>
    //                        (&gdalcubes::image_collection_cube::create),
    //                    py::arg("ic"), py::arg("v"));
    //        .def_static("create",
    //                    py::overload_cast<std::shared_ptr<gdalcubes::image_collection>>(&gdalcubes::image_collection_cube::create),
    //                    py::arg("ic"));
}
