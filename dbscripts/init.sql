DROP DATABASE IF EXISTS :DB_NAME;
DROP ROLE IF EXISTS :DB_LOGIN;
CREATE USER :DB_LOGIN WITH PASSWORD :DB_LOGIN_PASSWORD CREATEDB;
CREATE DATABASE :DB_NAME WITH TEMPLATE = :TEMPLATE_DB_NAME OWNER :DB_LOGIN;
GRANT ALL ON DATABASE :DB_NAME TO :DB_LOGIN;
