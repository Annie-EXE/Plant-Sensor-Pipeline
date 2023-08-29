-- File to create database and tables within the database

DROP DATABASE IF EXISTS plants;
CREATE DATABASE plants;
\c plants;

CREATE TABLE IF NOT EXISTS sunlight_type (
    sunlight_type_id INT UNIQUE NOT NULL,
    sunlight_type TEXT NOT NULL,
    PRIMARY KEY (sunlight_type_id)
);

CREATE TABLE IF NOT EXISTS sunlight (
    sunlight_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    PRIMARY KEY (sunlight_id),
    FOREIGN KEY (sunlight_id) REFERENCES sunlight_type(sunlight_type_id)
);

CREATE TABLE IF NOT EXISTS soil_moisture (
    soil_moisture_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    soil_moisture_value DECIMAL NOT NULL, 
    PRIMARY KEY (soil_moisture_id)
);

CREATE TABLE IF NOT EXISTS temperature (
    temp_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    temperature_value DECIMAL NOT NULL, 
    PRIMARY KEY (temp_id)
);

CREATE TABLE IF NOT EXISTS plant_origin (
    origin_id GENERATED ALWAYS AS IDENTITY,
    latitude SMALLINT NOT NULL,
    longitude SMALLINT NOT NULL,
    country TEXT NOT NULL,
    PRIMARY KEY (origin_id)
);

CREATE TABLE IF NOT EXISTS botanist (
    botanist_id GENERATED ALWAYS AS IDENTITY,
    botanist_name TEXT NOT NULL,
    botanist_email TEXT,
    botanist_phone_number TEXT,
    PRIMARY KEY (botanist_id)
);
