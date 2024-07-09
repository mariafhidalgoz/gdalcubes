//
// Created by Maria Hidalgo on 25.07.23.
//

#ifndef GDALCUBES_GDALCUBES_H
#define GDALCUBES_GDALCUBES_H

#include <fstream>

#include "../image_collection_cube.h"

namespace gdalcubes {
class gdalcubes {
   public:
    static void create_image_collection(
        std::vector<std::string> files,
        std::string format_file,
        std::string outfile);
    static void create_image_collection(
        std::string input,
        std::string output,
        std::string format);
    static std::vector<std::string> string_list_from_text_file(
        std::string filename);

    static void raster_cube(std::string input, std::string output);

    static std::shared_ptr<image_collection_cube> create_image_collection_cube(
        std::string input,
        uint32_t x,
        uint32_t y,
        uint32_t t);
    static int total_chunks(std::shared_ptr<image_collection_cube> cube);
    static bool is_chunk_empty(
        std::shared_ptr<image_collection_cube> cube,
        chunkid_t chunk_id);

    static void write_chunks_netcdf(
        std::string input,
        std::string output);
    static bool write_single_chunk_netcdf(
        std::string input,
        std::string output,
        chunkid_t chunk_id,
        uint32_t x,
        uint32_t y,
        uint32_t t);
    static bool write_single_chunk_netcdf(
        std::shared_ptr<image_collection_cube> cube,
        std::string output,
        chunkid_t chunk_id);

    static void merge_chunks(std::shared_ptr<image_collection_cube> cube, std::string work_dir = "", std::string file_name = "result");
};
}  // namespace gdalcubes

#endif  // GDALCUBES_GDALCUBES_H
