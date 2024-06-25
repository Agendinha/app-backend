DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "schedule" CASCADE;

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    usertype VARCHAR(100) DEFAULT 'customer' -- change it to admin if needed
);

-- a service has many schedules
CREATE TABLE IF NOT EXISTS "schedule" (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    service VARCHAR NOT NULL,
    start_time TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES "user"(id)
);
