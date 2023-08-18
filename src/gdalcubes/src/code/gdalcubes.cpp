//
// Created by Maria Hidalgo on 25.07.23.
//

#include "gdalcubes.h"

#include <fstream>
#include <iostream>

#include "../apply_pixel.h"
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

void gdalcubes::gc_create_image_collection_from_format_all(
    std::string input = "./L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    std::string output = "./new_image_collection.db",
    std::string format = "/Users/maria/GitHub/gdalcubes/src/gdalcubes/formats/L8_SR.json") {
    config::instance()->gdalcubes_init();
    config::instance()->set_error_handler(error_handler::error_handler_debug);
    std::cout << "GOOOO -> gc_create_image_collection_from_format_all" << std::endl;

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

    std::string line;
    std::ifstream infile(filename);
    while (std::getline(infile, line))
        out.push_back(line);
    return out;
}

// gc_create_image_collection_cube
// std::shared_ptr<image_collection_cube> gdalcubes::raster_cube(
void gdalcubes::raster_cube(
    std::string input = "./image_collection.db",
    std::string output = "./complete_netcdf.nc") {
    config::instance()->gdalcubes_init();

    //    cube_view cv;
    //    cv.srs("EPSG:32622");
    //    cv.set_x_axis(-59.12746, -52.09798, 100.0);
    //    cv.set_y_axis(-6.84404, -1.844241, 100.0);
    //    cv.set_t_axis(datetime::from_string("2014-07-01"), datetime::from_string("2014-07-31"), duration::from_string("P1D"));
    //    std::cout << "Cube View created" << std::endl;
    //    std::cout << cv.bottom() << std::endl;
    //    std::cout << cv.dx() << std::endl;

    //    auto icc = image_collection_cube::create(input, cv);
    auto icc = image_collection_cube::create(input);
    //    auto icc = image_collection_cube::create(ic, cv);
    //    auto icc = image_collection_cube::create(ic);
    std::cout << "Image Collection Cube | Raster Cube created" << std::endl;
    //    std::cout << icc << std::endl;

    //    auto cb = select_bands_cube::create(icc, std::vector<std::string>{"B04", "B05"});
    //    std::cout << "Select Bands" << std::endl;
    //    cb->write_netcdf_file(output);
    icc->write_netcdf_file(output);
    std::cout << "Write NetCDF" << std::endl;
}

void gdalcubes::write_chunks_netcdf(
    std::string input = "./image_collection.db",
    std::string output = "Python",
    uint16_t nthreads = 1) {
    config::instance()->gdalcubes_init();

    config::instance()->set_default_chunk_processor(std::dynamic_pointer_cast<chunk_processor>(std::make_shared<chunk_processor_multithread>(nthreads)));

    //    auto icc = image_collection_cube::create(input, cv);
    auto icc = image_collection_cube::create(input);
    std::cout << "Image Collection Cube | Raster Cube created" << std::endl;

    auto ndvi = apply_pixel_cube::create(icc, {"(B04-B05)/(B04+B05)"});
    //    auto cb = select_bands_cube::create(icc, std::vector<std::string>{"B04", "B05"});

    //    uint16_t count_chunks = icc->count_chunks();
    uint16_t count_chunks = ndvi->count_chunks();
    std::cout << "count_chunks" << std::endl;
    std::cout << count_chunks << std::endl;
    //    icc->write_chunks_netcdf(output, "chunks", 0);
    ndvi->write_chunks_netcdf(output, "chunks", 0);
    std::cout << "Write Chunks NetCDF" << std::endl;
}

void gdalcubes::write_single_chunk_netcdf(
    std::string input = "./image_collection.db",
    std::string output = "./single_chunk.nc",
    chunkid_t chunk_id = 1) {
    config::instance()->gdalcubes_init();

    config::instance()->set_default_chunk_processor(std::dynamic_pointer_cast<chunk_processor>(std::make_shared<chunk_processor_multithread>(1)));

    //    auto icc = image_collection_cube::create(input, cv);
    auto icc = image_collection_cube::create(input);
    std::cout << "Image Collection Cube | Raster Cube created" << std::endl;

    uint16_t count_chunks = icc->count_chunks();
    std::cout << "count_chunks" << std::endl;
    std::cout << count_chunks << std::endl;
    //    auto co = icc->chunk_coords_from_id(1);
    ////    auto si = icc->chunk_size(1);
    //    std::cout << "co" << std::endl;
    //    std::cout << co.data() << std::endl;

    //    for (uint32_t i=0; i<icc->count_chunks(); ++i) {
    //        std::cout <<  std::endl <<  "CHUNK ID " << i << std::endl;
    //        std::cout << "---------------------------------------------------------"<< std::endl;
    //        std::shared_ptr<chunk_data> dat = icc->read_chunk(i);
    //        if (!dat->empty()) {
    //            std::cout << "IN" << std::endl;
    //            uint32_t ncol = dat->size()[0];
    //            uint32_t nrow = dat->size()[1];
    //        }
    //    }

    icc->write_single_chunk_netcdf(chunk_id, output, 0);
    std::cout << "Write Single NetCDF" << std::endl;
}

}  // namespace gdalcubes
