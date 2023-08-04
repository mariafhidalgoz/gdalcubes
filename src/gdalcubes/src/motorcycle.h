#include <string>

#ifndef MOTORCYCLE_H
#define MOTORCYCLE_H

#include <ogr_spatialref.h>

// SQLite forward declarations
class sqlite3;
class sqlite3_stmt;

namespace gdalcubes {

class Motorcycle {

private:

    /// Name
    std::string _name;
    std::string filename;

public:

    /// Constructor
    Motorcycle(std::string name);
    /// Constructor
    Motorcycle();

    /// Get name
    /// @return Name
    std::string get_name() const;

    /// Ride the bike
    /// @param road Name of the road
    void ride(std::string road, std::string road2) const;

    void load_file(std::string filename);


    int create() const;
    static std::shared_ptr<Motorcycle> create2();

protected:
    std::string _filename;
    sqlite3* _db;

};

}

#endif
