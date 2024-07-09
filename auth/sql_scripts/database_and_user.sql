
-- # Log into docker
-- docker exec -it dev_postgresql_container bash

-- # Log into psql, and into the admin database, away from the target database.
-- psql -U admin -h localhost -p 5432 -d admin

-- # Create the user if it doesn't already exist.
CREATE USER auth_srv_user WITH PASSWORD 'auth_srv_user';

-- # Terminate any existing connections to the database.
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'auth_srv';

-- # Drop the database.
-- DROP DATABASE auth_srv;

-- # Create a new database.
CREATE DATABASE auth_srv
    WITH
    OWNER = auth_srv_user
    ENCODING = 'UTF8';

-- # Quit the current session and log in again, this time to the target database.
-- \q
-- psql -U admin -h localhost -p 5432 -d auth_srv





GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO codefranticuser;
GRANT CONNECT ON DATABASE codefrantic TO codefranticuser;
GRANT ALL PRIVILEGES ON DATABASE codefrantic TO codefranticuser;
GRANT ALL PRIVILEGES ON SCHEMA public TO codefranticuser;
GRANT ALL ON SCHEMA public TO codefranticuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO codefranticuser;

-- Grant ownership of the tables so that the user can drop tables.
DO $$ 
DECLARE 
    table_name text; 
BEGIN 
    FOR table_name IN 
        SELECT t.table_name 
        FROM information_schema.tables t
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
    LOOP 
        EXECUTE 'ALTER TABLE public.' || table_name || ' OWNER TO codefranticuser'; 
    END LOOP; 
END $$;
