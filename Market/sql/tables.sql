CREATE TABLE IF NOT EXISTS basket (
    id BIGINT,
    product INTEGER NOT NULL DEFAULT 0,
    quantity BIGINT NOT NULL DEFAULT 0,
    pay INTEGER NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    role INTEGER NOT NULL DEFAULT 0,
    address TEXT,
    phone TEXT,
    name TEXT,
    lastname TEXT,
    email TEXT
);


CREATE TABLE IF NOT EXISTS catalog (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL DEFAULT 'None',
    description TEXT NOT NULL DEFAULT 'None',
    price INTEGER NOT NULL DEFAULT 1,
    calories INTEGER NOT NULL DEFAULT 1,
    image TEXT NOT NULL DEFAULT 'None',
    category TEXT NOT NULL DEFAULT 'None',
    subcategories TEXT NOT NULL DEFAULT 'None'
);


CREATE TABLE IF NOT EXISTS faq (
    question TEXT,
    answer TEXT
);



