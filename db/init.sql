create database IF NOT EXISTS gamesdb;
use gamesdb;
create table IF NOT EXISTS games (
     id int NOT NULL,
     nom_jeux varchar(255),
     img_src varchar(255) ,
     prix  varchar(255) ,
     region varchar(255),
     etat varchar(255),
     PRIMARY KEY (id)
);