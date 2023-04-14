CREATE TABLE employers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    site_url VARCHAR(255),
    logo_url VARCHAR(255)
);

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    employer_id INTEGER REFERENCES employers(id),
    salary_from INTEGER,
    salary_to INTEGER,
    salary_currency VARCHAR(10),
    published_at TIMESTAMP,
    url VARCHAR(255)
);