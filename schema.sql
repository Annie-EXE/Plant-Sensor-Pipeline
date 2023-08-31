-- File to create database and tables within the database

DROP DATABASE IF EXISTS plants;
CREATE DATABASE plants;
\c plants;

CREATE TABLE IF NOT EXISTS sun_condition (
   sun_condition_id INT GENERATED ALWAYS AS IDENTITY,
   sun_condition_type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS shade_condition (
   shade_condition_id INT GENERATED ALWAYS AS IDENTITY,
   shade_condition_type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS plant_origin (
    plant_origin_id INT GENERATED ALWAYS AS IDENTITY,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    country TEXT,
    PRIMARY KEY (plant_origin_id),
    CONSTRAINT unique_latitude_longitude UNIQUE (latitude, longitude)
);

CREATE TABLE IF NOT EXISTS botanist (
    botanist_id INT GENERATED ALWAYS AS IDENTITY,
    botanist_name TEXT NOT NULL UNIQUE,
    botanist_email TEXT NOT NULL UNIQUE,
    botanist_phone_number TEXT NOT NULL UNIQUE,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE IF NOT EXISTS plant (
    plant_id SMALLINT NOT NULL UNIQUE,
    plant_name TEXT NOT NULL,
    plant_scientific_name TEXT, 
    plant_origin_id SMALLINT,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (plant_origin_id) REFERENCES plant_origin(plant_origin_id)
);

CREATE TABLE IF NOT EXISTS water_history (
    water_history_id INT GENERATED ALWAYS AS IDENTITY,
    time_watered TIMESTAMP NOT NULL,
    plant_id INT NOT NULL,
    PRIMARY KEY (water_history_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    CONSTRAINT unique_time_plant UNIQUE (time_watered, plant_id)
);

CREATE TABLE IF NOT EXISTS reading_information (
    reading_information_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    plant_reading_time TIMESTAMP NOT NULL,
    botanist_id SMALLINT NOT NULL,
    soil_moisture DECIMAL,
    sun_condition_id INT,
    shade_condition_id INT, 
    temperature DECIMAL NOT NULL,
    PRIMARY KEY (reading_information_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (sun_condition_id) REFERENCES sun_condition(sun_condition_id),
    FOREIGN KEY (shade_condition_id) REFERENCES shade_condition(shade_condition_id),
    CONSTRAINT unique_plant_reading_time UNIQUE (plant_id, plant_reading_time)
);


CREATE SCHEMA long_term;


CREATE TABLE IF NOT EXISTS long_term.sun_condition (
   sun_condition_id INT GENERATED ALWAYS AS IDENTITY,
   sun_condition_type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS long_term.shade_condition (
   shade_condition_id INT GENERATED ALWAYS AS IDENTITY,
   shade_condition_type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS long_term.plant_origin (
    plant_origin_id INT GENERATED ALWAYS AS IDENTITY,
    latitude DECIMAL,
    longitude DECIMAL,
    country TEXT,
    PRIMARY KEY (plant_origin_id),
    CONSTRAINT unique_latitude_longitude UNIQUE (latitude, longitude)
);

CREATE TABLE IF NOT EXISTS long_term.botanist (
    botanist_id INT UNIQUE,
    botanist_name TEXT NOT NULL UNIQUE,
    botanist_email TEXT,
    botanist_phone_number TEXT,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE IF NOT EXISTS long_term.plant (
    plant_id SMALLINT NOT NULL UNIQUE,
    plant_name TEXT NOT NULL,
    plant_scientific_name TEXT, 
    plant_origin_id SMALLINT,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (plant_origin_id) REFERENCES plant_origin(plant_origin_id)
);

CREATE TABLE IF NOT EXISTS long_term.water_history (
    water_history_id INT GENERATED ALWAYS AS IDENTITY,
    time_watered TIMESTAMP NOT NULL,
    plant_id INT NOT NULL,
    PRIMARY KEY (water_history_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    CONSTRAINT unique_time_plant UNIQUE (time_watered, plant_id)
);

CREATE TABLE IF NOT EXISTS long_term.reading_information (
    reading_information_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    plant_reading_time TIMESTAMP NOT NULL,
    botanist_id SMALLINT NOT NULL,
    soil_moisture DECIMAL,
    sun_condition_id INT,
    shade_condition_id INT, 
    temperature DECIMAL NOT NULL,
    PRIMARY KEY (reading_information_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (sun_condition_id) REFERENCES sun_condition(sun_condition_id),
    FOREIGN KEY (shade_condition_id) REFERENCES shade_condition(shade_condition_id),
    CONSTRAINT unique_plant_reading_time UNIQUE (plant_id, plant_reading_time)
);