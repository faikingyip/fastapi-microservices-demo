-- # Log into docker
-- docker exec -it dev_postgresql_container bash

-- # Log into psql, and into the admin database, away from the target database.
-- psql -U admin -h localhost -p 5432 -d admin

CREATE USER items_srv_dev_user WITH PASSWORD 'items_srv_dev_pass';
CREATE DATABASE items_srv_dev
    WITH
    OWNER = items_srv_dev_user
    ENCODING = 'UTF8';

-- # Terminate any existing connections to the database.
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'items_srv_dev';

-- # Drop the database.
-- DROP DATABASE items_srv_dev;

CREATE USER items_srv_test_user WITH PASSWORD 'items_srv_test_pass';
CREATE DATABASE items_srv_test
    WITH
    OWNER = items_srv_test_user
    ENCODING = 'UTF8';

-- # Terminate any existing connections to the database.
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'items_srv_test';

-- # Drop the database.
-- DROP DATABASE items_srv_test;


