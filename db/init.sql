create database IF NOT EXISTS gamesdb;
use gamesdb;
DROP TABLE IF EXISTS games;
create table games (
     id varchar(255),
     nom_jeux varchar(255),
     img_src varchar(255) ,
     prix  varchar(255) ,
     region varchar(255),
     etat varchar(255)
);