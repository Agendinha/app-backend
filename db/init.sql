CREATE TABLE IF NOT EXISTS "usuario" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    postalcode VARCHAR(10),
    usertype VARCHAR(20)
);
