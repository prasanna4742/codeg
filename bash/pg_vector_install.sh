#!/bin/bash

# Set variables
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb
POSTGRES_ROOT=/c/Users/PKulkarni4/Desktop/work/code/codeRAG/db
DATA_DIR=$POSTGRES_ROOT/data
SQL_DIR=$POSTGRES_ROOT/sql
# Create the data directory if it doesn't exist
mkdir -p $DATA_DIR
mkdir -p $SQL_DIR

# Create a script to enable pg_vector extension for all databases
cat > $SQL_DIR/init.sql <<EOF
CREATE EXTENSION IF NOT EXISTS vector;

-- Function to create extension on all databases
CREATE OR REPLACE FUNCTION create_extension_on_all_databases()
RETURNS void AS $$
DECLARE
    db_name TEXT;
BEGIN
    FOR db_name IN SELECT datname FROM pg_database WHERE datistemplate = false LOOP
        EXECUTE format('CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;');
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Run the function
SELECT create_extension_on_all_databases();
EOF

# Run the Docker container
docker run -d --name my-postgres \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -v $DATA_DIR:/var/lib/postgresql/data \
  -v $SQL_DIR/init.sql:/docker-entrypoint-initdb.d/init.sql \
  pgvector/pgvector:pg16