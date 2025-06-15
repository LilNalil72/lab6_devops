ALTER TABLE patients ADD COLUMN gender VARCHAR(20);
INSERT INTO schema_version (version) VALUES (4);