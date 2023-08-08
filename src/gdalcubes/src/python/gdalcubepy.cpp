#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_example_pybind11(py::module &);
void init_gdalcubes(py::module &);
void init_collection_format(py::module &);
void init_image_collection(py::module &);
void init_image_collection_cube(py::module &);
void init_filesystem(py::module &);
void init_cube_view(py::module &);

namespace mcl {

    PYBIND11_MODULE(gdalcubepy, m) {
        // Optional docstring
        m.doc() = "gdalcubes python library";

        init_example_pybind11(m);
        init_gdalcubes(m);
        init_collection_format(m);
        init_image_collection(m);
        init_image_collection_cube(m);
        init_filesystem(m);
        init_cube_view(m);
    }
}
