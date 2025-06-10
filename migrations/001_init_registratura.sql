-- patients + appointments
CREATE TABLE IF NOT EXISTS patients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  birth_date DATE,
  phone VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS appointments (
  id SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(id),
  date_time TIMESTAMP NOT NULL,
  status VARCHAR(20) DEFAULT 'pending'
);
