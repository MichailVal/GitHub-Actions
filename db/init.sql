CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO items (name) VALUES
    ('Item 1'),
    ('Item 2'),
    ('Item 3'),
    ('Item 4'),
    ('Item 5');
