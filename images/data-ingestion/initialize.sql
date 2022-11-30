DROP TABLE IF EXISTS people;
CREATE TABLE IF NOT EXISTS people (
    given_name VARCHAR(255) NOT NULL,
    family_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    place_of_birth VARCHAR(255) NOT NULL,
    INDEX(place_of_birth)
);

DROP TABLE IF EXISTS places;
CREATE TABLE IF NOT EXISTS places (
    city VARCHAR(255) NOT NULL,
    county VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    INDEX(city)
);