CREATE DATABASE template_postgis WITH ENCODING 'UTF-8';
UPDATE pg_database SET datistemplate=true WHERE datname='template_postgis';
\c template_postgis
CREATE EXTENSION postgis;
