-- doctors + shifts
CREATE TABLE IF NOT EXISTS doctors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  specialty VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS shifts (
  id SERIAL PRIMARY KEY,
  doctor_id INT REFERENCES doctors(id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL
);
