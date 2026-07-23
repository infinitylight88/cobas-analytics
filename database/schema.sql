CREATE TABLE patient_results (

    id SERIAL PRIMARY KEY,

    archive_id INTEGER,

    raw_record_id INTEGER,

    record_code INTEGER,

    result_datetime TIMESTAMP,

    test_code VARCHAR(20),

    patient_initials VARCHAR(30),

    patient_id VARCHAR(50),

    accession_number VARCHAR(50),

    patient_source VARCHAR(20),

    control_level VARCHAR(30),

    sample_type VARCHAR(10),

    units VARCHAR(30),

    flag VARCHAR(100),

    result NUMERIC,

    gender VARCHAR(10),

    dob DATE

);