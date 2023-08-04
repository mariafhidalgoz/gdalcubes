#include "./motorcycle.h"

#include <iostream>

#include <gdalwarper.h>
#include <sqlite3.h>

#include <boost/regex.hpp>
#include <set>
#include <unordered_set>


namespace gdalcubes {

Motorcycle::Motorcycle(std::string name) {
    _name = name;
}
Motorcycle::Motorcycle() : _filename(""), _db(nullptr){
    _name = "MAFE";
}

std::string Motorcycle::get_name() const {
    return _name;
}

void Motorcycle::ride(std::string road, std::string road2) const {
    std::cout << "Zoom Zoom on road: " << road << std::endl;
    std::cout << "Zoom Zoom on road2: " << road2 << std::endl;
}

void Motorcycle::load_file(std::string filename) {
    std::cout << "Zoom Zoom on road 1: " << filename << std::endl;
    std::cout << "Zoom Zoom on road 2: " << filename << std::endl;
}

int Motorcycle::create() const {
    int o = 45;
    return o;
}
std::shared_ptr<Motorcycle> Motorcycle::create2() {
    std::shared_ptr<Motorcycle> o = std::make_shared<Motorcycle>();
    return o;
}

}
