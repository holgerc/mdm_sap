-- MDM Database Initialization Script
-- This script runs when PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE mdm_db TO mdm;

-- Create default schema
CREATE SCHEMA IF NOT EXISTS mdm;

-- Set search path
ALTER DATABASE mdm_db SET search_path TO public, mdm;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'MDM Database initialized successfully at %', NOW();
END $$;
