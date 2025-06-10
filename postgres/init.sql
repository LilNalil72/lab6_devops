-- Схема для registratura
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

-- Схема для schedule
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
