//
// Created by Maria Hidalgo on 25.07.23.
//

#include "gdalcubes.h"

#include <fstream>
#include <iostream>

#include "../select_bands.h"

namespace gdalcubes {

void gdalcubes::gc_create_image_collection_from_format(
    std::vector<std::string> files,
    std::string format_file,
    std::string outfile) {
    bool unroll_archives = true;
    collection_format cfmt(format_file);
    if (unroll_archives) {
        files = image_collection::unroll_archives(files);
    }
    image_collection::create(cfmt, files)->write(outfile);
}

void gdalcubes::gc_create_image_collection_from_format_test(
    std::string input = "./L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    std::string output = "./new_image_collection.db",
    std::string format = "/Users/maria/GitHub/gdalcubes/src/gdalcubes/formats/L8_SR.json") {
    config::instance()->gdalcubes_init();
    config::instance()->set_error_handler(error_handler::error_handler_debug);
    std::cout << "GOOOO -> gc_create_image_collection_from_format_test" << std::endl;

    bool scan_archives = true;
    bool recursive = false;
    bool strict = false;

    std::vector<std::string> in;

    if (filesystem::is_directory(input)) {
        std::cout << "Is directory" << std::endl;
        if (recursive) {
            filesystem::iterate_directory_recursive(input, [&in](const std::string &p) {
                if (filesystem::is_regular_file(p)) {
                    in.push_back(filesystem::make_absolute(p));
                }
            });

        } else {
            filesystem::iterate_directory(input, [&in](const std::string &p) {
                std::cout << "Is file" << std::endl;
                std::cout << p << std::endl;
                if (filesystem::is_regular_file(p)) {
                    std::cout << "Push file" << std::endl;
                    in.push_back(filesystem::make_absolute(p));
                }
            });
        }
    } else if (filesystem::is_regular_file(input)) {
        std::cout << "Is regular file" << std::endl;
        in = string_list_from_text_file(input);
    } else {
        throw std::string("ERROR in gdalcubes create_collection: Invalid input, provide a text file or directory.");
    }

    if (scan_archives) {
        in = image_collection::unroll_archives(in);
    }
    std::cout << "ARCHIVES" << std::endl;
    std::cout << in.data() << std::endl;

    collection_format f(format);
    std::cout << format << std::endl;

    auto ic = image_collection::create(f, in, strict);
    std::cout << "Image Collection created" << std::endl;
    std::cout << ic << std::endl;

    ic->write(output);
    std::cout << ic->to_string() << std::endl;
}

std::vector<std::string> gdalcubes::string_list_from_text_file(std::string filename) {
    std::vector<std::string> out;

    std::cout << "filename" << std::endl;
    std::cout << filename << std::endl;
    std::string line;
    std::ifstream infile(filename);
    while (std::getline(infile, line))
        std::cout << "line" << std::endl;
    std::cout << line << std::endl;
    out.push_back(line);
    std::cout << "Output" << std::endl;
    return out;
}

// gc_create_image_collection_cube
// std::shared_ptr<image_collection_cube> gdalcubes::raster_cube(
void gdalcubes::raster_cube(
    std::string input = "./image_collection.db",
    std::string output = "./band_select.nc") {

    cube_view cv;
    cv.srs("EPSG:3857");
    cv.set_x_axis(-6180000.0, -6080000.0, 100.0);
    cv.set_y_axis(-550000.0, -450000.0, 100.0);
    cv.set_t_axis(datetime::from_string("2016-07-01"), datetime::from_string("2016-07-31"), duration::from_string("P1D"));
//    cube_view w;
//    w.left() = 300000.000;
//    w.top() = 5800020.000;
//    w.bottom() = 5690220.000;
//    w.right() = 409800.000;
//    w.srs() = "EPSG:32632";
//    w.nx() = 500;
//    w.ny() = 500;
//    w.dt(duration::from_string("P1D"));
//    w.t0() = datetime::from_string("2018-06-14");
//    w.t1() = datetime::from_string("2018-06-14");
    std::cout << "Cube View created" << std::endl;
    std::cout << cv.bottom() << std::endl;
    std::cout << cv.dx() << std::endl;

    auto icc = image_collection_cube::create(input, cv);
//    auto icc = image_collection_cube(ic);
//    auto icc = image_collection_cube::create(ic, cv);
//    auto icc = image_collection_cube::create(ic);
    std::cout << "Image Collection Cube | Raster Cube created" << std::endl;
    //    std::cout << icc << std::endl;

    auto cb = select_bands_cube::create(icc, std::vector<std::string>{"B04", "B05"});
    std::cout << "Select Bands" << std::endl;
    cb->write_netcdf_file(output);
    std::cout << "Write NetCDF" << std::endl;

//    cb2->write_tif_collection("/Users/maria/GitHub/gdalcubes/src/gdalcubes/Python",
//                              "blabla", true, true, std::map<std::string, std::string>(), "NEAREST", packed_export::make_uint8(1, 0));

//    cb->write_gdal_image("test_example_1_write_gdal.tif");
}

}  // namespace gdalcubes
