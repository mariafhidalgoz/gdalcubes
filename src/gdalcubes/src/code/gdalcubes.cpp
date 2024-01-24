//
// Created by Maria Hidalgo on 25.07.23.
//

#include "gdalcubes.h"

#include <fstream>
#include <iostream>

#include "../apply_pixel.h"
#include "../select_bands.h"

namespace gdalcubes {

// TODO: This function is to test sending a list of files from python
void gdalcubes::create_image_collection(
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

void gdalcubes::create_image_collection(
    std::string input = "./L8_Amazon_mini/LC082290632016072901T1-SC20190715045704",
    std::string output = "./new_image_collection.db",
    std::string format = "/Users/maria/GitHub/gdalcubes/src/gdalcubes/formats/L8_SR.json") {
    config::instance()->gdalcubes_init();

    bool scan_archives = true;
    bool recursive = true;
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
    std::cout << "Path: " << output << std::endl;
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

std::shared_ptr<image_collection_cube> gdalcubes::create_image_collection_cube(
    std::string input = "./image_collection.db",
    uint32_t chunk_size = 0) {
    config::instance()->gdalcubes_init();

    auto icc = image_collection_cube::create(input);
    return icc;
}

int gdalcubes::total_chunks(std::shared_ptr<image_collection_cube> cube) {
    uint16_t count_chunks = cube->count_chunks();
    std::cout << "count_chunks" << std::endl;
    std::cout << count_chunks << std::endl;
    return count_chunks;
}

bool gdalcubes::is_chunk_empty(
    std::shared_ptr<image_collection_cube> cube,
    chunkid_t chunk_id = 1) {
    config::instance()->gdalcubes_init();

    auto chunk = cube->read_chunk(chunk_id);
    return chunk->empty();
}

void gdalcubes::write_chunks_netcdf(
    std::string input = "./image_collection.db",
    std::string output = "Python") {
    config::instance()->gdalcubes_init();

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

    auto icc = image_collection_cube::create(input);
    std::cout << "Raster Cube created" << std::endl;

    icc->write_single_chunk_netcdf(chunk_id, output, 0);
    std::cout << "Write Single NetCDF" << std::endl;
}

void gdalcubes::write_single_chunk_netcdf(
    std::shared_ptr<image_collection_cube> cube,
    std::string output = "./single_chunk.nc",
    chunkid_t chunk_id = 1) {
    config::instance()->gdalcubes_init();

    cube->write_single_chunk_netcdf(chunk_id, output, 0);
    std::cout << "Write Single NetCDF" << std::endl;
}

// TODO: merge chunks when they are done
void gdalcubes::merge_chunks(std::shared_ptr<image_collection_cube> cube, std::string work_dir, std::string file_name) {

    config::instance()->set_default_chunk_processor(std::make_shared<chunk_processor_multithread>(2));
    //    config::instance()->set_default_chunk_processor(std::dynamic_pointer_cast<chunk_processor>(std::make_shared<chunk_processor_multithread>(2)));

    cube->write_chunks_kubernetes(work_dir, file_name);


//    std::vector<std::pair<std::string, chunkid_t>> chunk_queue;
//    filesystem::iterate_directory(work_dir, [&chunk_queue](const std::string &f) {
//        // Consider files with name X.nc, where X is an integer number
//        // Temporary files will start with a dot and are NOT considered here
//        std::string basename = filesystem::stem(f) + "." + filesystem::extension(f);
//        std::size_t pos = basename.find(".nc");
//        if (pos > 0 && pos < std::string::npos) {
//            try {
//                int chunkid = std::stoi(basename.substr(0, pos));
//                chunk_queue.push_back(std::make_pair<>(f, chunkid));
//            } catch (...) {
//            }
//        }
//    });
//
//    for (auto it = chunk_queue.begin(); it != chunk_queue.end(); ++it) {
//        try {
//            std::cout << "Merging chunk " << std::to_string(it->second) << " from " << it->first << std::endl;
//            std::shared_ptr<chunk_data> dat = std::make_shared<chunk_data>();
//            dat->read_ncdf_full(it->first);
//            //            f(it->second, dat, mutex);
//            //            filesystem::remove(it->first);
//
//            // for debugging only
//            // filesystem::move(it->first,it->first + "DONE.nc");
//
//        } catch (std::string s) {
//            GCBS_ERROR(s);
//            continue;
//        } catch (...) {
//            GCBS_ERROR("unexpected exception while processing chunk");
//            continue;
//        }
//    }
}

}  // namespace gdalcubes
