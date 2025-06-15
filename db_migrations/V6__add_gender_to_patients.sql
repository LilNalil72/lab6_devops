ALTER TABLE patients ADD COLUMN gender VARCHAR(1);
INSERT INTO schema_version (version) VALUES (6);

