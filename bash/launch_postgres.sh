#!/bin/bash

# Default values
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
# export POSTGRES_DB=ragdb

# Create local directory for PostgreSQL data if it doesn't exist
mkdir -p ./postgres_data

# Check if the container already exists
CONTAINER_EXISTS=$(docker-compose ps -q postgres)

if [ -z "$CONTAINER_EXISTS" ]; then
    echo "Creating and starting PostgreSQL container..."
    docker-compose up -d
else
    echo "PostgreSQL container already exists. Starting it..."
    docker-compose start
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec -T postgres pg_isready -U $POSTGRES_USER; do
  sleep 1
done

# Create user and database if they don't exist
# docker-compose exec -T postgres psql -  U postgres <<-EOSQL
#     DO
#     \$do\$
#     BEGIN
#        IF NOT EXISTS (
#           SELECT FROM pg_catalog.pg_roles
#           WHERE  rolname = '$POSTGRES_USER') THEN
#           CREATE ROLE $POSTGRES_USER LOGIN PASSWORD '$POSTGRES_PASSWORD';
#        END IF;
#     END
#     \$do\$;

#     SELECT 'CREATE DATABASE $POSTGRES_DB'
#     WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB')\gexec

#     GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
# EOSQL

# # Enable pg_vector extension on the new database
# docker-compose exec -T postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "PostgreSQL is ready!"
echo "Connection details:"
echo "Host: localhost"
echo "Port: 5432"
# echo "User: $POSTGRES_USER"
# echo "Password: $POSTGRES_PASSWORD"
# echo "Database: $POSTGRES_DB"
echo "pg_vector extension is enabled on the database."
echo "PostgreSQL data is stored in: $(pwd)/postgres_data"