-- schema.sql — DDL (Data Definition Language) for Silent Voices
-- These CREATE TABLE statements define the database structure

CREATE TABLE users (
    id               SERIAL PRIMARY KEY,
    full_name        VARCHAR(100) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    hashed_password  VARCHAR(255) NOT NULL,
    role             VARCHAR(10) DEFAULT 'user',
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Sprint 2 will add:
-- CREATE TABLE sessions (...)
-- CREATE TABLE gesture_results (...)
-- CREATE TABLE feedback (...)