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
    static void gc_create_image_collection_from_format(std::vector<std::string> files,
                                                       std::string format_file,
                                                       std::string outfile);
    static void gc_create_image_collection_from_format_all(std::string input, std::string output, std::string format);

    static void raster_cube(std::string input, std::string output);
    static void write_chunks_netcdf(std::string input, std::string output, uint16_t nthreads);
    static void write_single_chunk_netcdf(std::string input, std::string output, chunkid_t chunk_id);

    static std::vector<std::string> string_list_from_text_file(std::string filename);
};
}  // namespace gdalcubes

#endif  // GDALCUBES_GDALCUBES_H
