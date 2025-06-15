INSERT INTO doctors (full_name, specialization)
VALUES ('Иванов Петр Сергеевич', 'Терапевт');

INSERT INTO patients (full_name, policy_number)
VALUES ('Сидорова Мария Ивановна', '1234567890');

INSERT INTO patients (full_name, policy_number)
VALUES ('Гойда Сергей Романович', '1234567891');

INSERT INTO doctors (full_name, specialization)
VALUES ('Сабиров Наиль Ильдусович', 'Гинеколог');

INSERT INTO appointments (doctor_id, patient_id, appointment_time)
VALUES (1, 1, '2023-12-01 14:30:00');

INSERT INTO schema_version (version)
VALUES (5)
ON CONFLICT (version) DO NOTHING;
