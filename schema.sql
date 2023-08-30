-- File to create database and tables within the database

DROP DATABASE IF EXISTS plants;
CREATE DATABASE plants;
\c plants;

CREATE TABLE IF NOT EXISTS sunlight_type (
    sunlight_type_id INT UNIQUE NOT NULL,
    sunlight_type TEXT NOT NULL,
    PRIMARY KEY (sunlight_type_id)
);

CREATE TABLE IF NOT EXISTS plant_origin (
    plant_origin_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id INT NOT NULL,
    latitude SMALLINT NOT NULL,
    longitude SMALLINT NOT NULL,
    country TEXT NOT NULL,
    PRIMARY KEY (plant_origin_id), 
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE IF NOT EXISTS botanist (
    botanist_id INT GENERATED ALWAYS AS IDENTITY,
    botanist_name TEXT NOT NULL,
    botanist_email TEXT,
    botanist_phone_number TEXT,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE IF NOT EXISTS plant (
    plant_id SMALLINT NOT NULL UNIQUE,
    plant_name TEXT NOT NULL,
    plant_scientific_name TEXT, 
    plant_origin SMALLINT,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (plant_origin) REFERENCES plant_origin(plant_origin_id)
);

CREATE TABLE IF NOT EXISTS water_history (
    water_history_id INT GENERATED ALWAYS AS IDENTITY,
    time_watered TIMESTAMP NOT NULL,
    plant_id INT NOT NULL,
    PRIMARY KEY (water_history_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE IF NOT EXISTS reading_information (
    reading_information_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    plant_reading_time TIMESTAMP NOT NULL,
    botanist_id SMALLINT NOT NULL,
    soil_moisture DECIMAL,
    sunlight_id INT,
    temperature DECIMAL NOT NULL,
    PRIMARY KEY (reading_information_id),
    FOREIGN KEY (sunlight_id) REFERENCES sunlight_type(sunlight_type_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id)
);
