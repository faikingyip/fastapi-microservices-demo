-- # Log into docker
-- docker exec -it dev_postgresql_container bash

-- # Log into psql, and into the admin database, away from the target database.
-- psql -U admin -h localhost -p 5432 -d admin

CREATE USER auth_srv_dev_user WITH PASSWORD 'auth_srv_dev_pass';
CREATE DATABASE auth_srv_dev
    WITH
    OWNER = auth_srv_dev_user
    ENCODING = 'UTF8';

-- # Terminate any existing connections to the database.
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'auth_srv_dev';

-- # Drop the database.
-- DROP DATABASE auth_srv_dev;

CREATE USER auth_srv_test_user WITH PASSWORD 'auth_srv_test_pass';
CREATE DATABASE auth_srv_test
    WITH
    OWNER = auth_srv_test_user
    ENCODING = 'UTF8';

-- # Terminate any existing connections to the database.
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'auth_srv_test';

-- # Drop the database.
-- DROP DATABASE auth_srv_test;