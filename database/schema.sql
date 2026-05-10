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

-- Sprint 2 additions
CREATE TABLE sessions (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    video_filename  VARCHAR(255),
    translated_text TEXT,
    avg_confidence  FLOAT,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE gesture_results (
    id             SERIAL PRIMARY KEY,
    session_id     INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    gesture_label  VARCHAR(50),
    confidence     FLOAT,
    frame_number   INTEGER
);

-- Sprint 3 additions

-- Add is_active to users if not already done via ALTER TABLE
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

-- Feedback table: stores user ratings on translation accuracy
CREATE TABLE IF NOT EXISTS feedback (
    id           SERIAL PRIMARY KEY,
    session_id   INTEGER NOT NULL UNIQUE REFERENCES sessions(id) ON DELETE CASCADE,
    rating       INTEGER NOT NULL CHECK (rating IN (0, 1)),
    correction   TEXT,
    submitted_at TIMESTAMP DEFAULT NOW()
);