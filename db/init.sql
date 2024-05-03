DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "customer" CASCADE;
DROP TABLE IF EXISTS "provider" CASCADE;
DROP TABLE IF EXISTS "service" CASCADE;
DROP TABLE IF EXISTS "schedule" CASCADE;

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    postalcode VARCHAR(10),
    usertype VARCHAR(20)
);

-- a customer is a user
CREATE TABLE IF NOT EXISTS "customer" (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

-- a provider is a user
CREATE TABLE IF NOT EXISTS "provider" (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    workTime VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

-- a provider has many services
CREATE TABLE IF NOT EXISTS "service" (
    id SERIAL PRIMARY KEY,
    provider_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(100),
    duration INT NOT NULL,
    FOREIGN KEY (provider_id) REFERENCES "provider"(id)
);

-- a service has many schedules
CREATE TABLE IF NOT EXISTS "schedule" (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES "customer"(id),
    FOREIGN KEY (service_id) REFERENCES "service"(id)
);
