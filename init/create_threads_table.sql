CREATE TABLE IF NOT EXISTS threads (
    thread_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    thread_name VARCHAR(100) NOT NULL
);
