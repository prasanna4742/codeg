-- CREATE EXTENSION IF NOT EXISTS vector;

-- Function to create extension on all databases
-- CREATE OR REPLACE FUNCTION create_extension_on_all_databases()
-- RETURNS void AS $$
-- DECLARE
--     db_name TEXT;
-- BEGIN
--     FOR db_name IN SELECT datname FROM pg_database WHERE datistemplate = false LOOP
--         EXECUTE format('CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;');
--     END LOOP;
-- END;
-- $$ LANGUAGE plpgsql;

-- Run the function
-- SELECT create_extension_on_all_databases();

-- CREATE DATABASE ragdb;

-- CREATE ROLE pras LOGIN PASSWORD 'pras';

-- GRANT ALL PRIVILEGES ON DATABASE ragdb TO pras;

-- Enable the vector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the vector store table
-- CREATE TABLE IF NOT EXISTS vector_store (
--     id BIGSERIAL PRIMARY KEY,
--     content TEXT,
--     metadata JSONB,
--     embedding VECTOR(384)
-- );

-- Create an index on the embedding column for faster similarity searches
-- CREATE INDEX ON vector_store USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);