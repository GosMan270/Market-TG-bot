CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    sub_type INTEGER NOT NULL DEFAULT 0,
    sub_time REAL NOT NULL DEFAULT 0,
    role INTEGER NOT NULL DEFAULT 0,
    setting_model INTEGER NOT NULL DEFAULT 12,
    credits INTEGER NOT NULL DEFAULT 10,
    next_credits_time REAL NOT NULL DEFAULT 0,
    setting_system TEXT NOT NULL DEFAULT '',
    setting_temperature FLOAT NOT NULL DEFAULT 1.0,
    setting_max_tokens INTEGER NOT NULL DEFAULT 2048,
    ban INTEGER DEFAULT 0,
    balance INTEGER DEFAULT 0
);

