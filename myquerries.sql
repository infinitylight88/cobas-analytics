BEGIN;

TRUNCATE TABLE
patient_results,
qc_results,
calibrations,
maintenance,
host_events,
raw_records
RESTART IDENTITY CASCADE;

TRUNCATE TABLE
patients
RESTART IDENTITY CASCADE;

TRUNCATE TABLE
archive_files
RESTART IDENTITY CASCADE;

COMMIT;


..........................................

SELECT COUNT(*)
FROM archive_files;
..........................................

SELECT COUNT(*)
FROM patient_results;
..........................................

SELECT COUNT(DISTINCT sample_id)
FROM patient_results;
..........................................
SELECT analyte_code,
COUNT(*)
FROM patient_results
GROUP BY analyte_code
ORDER BY analyte_code;
.........................................
SELECT
analyte_code,
control_name,
COUNT(*)
FROM qc_results
GROUP BY analyte_code, control_name
ORDER BY analyte_code;
........................................

SELECT
DATE(run_datetime),
analyte_code,
COUNT(*)
FROM qc_results
GROUP BY DATE(run_datetime), analyte_code
ORDER BY 1,2;
........................................
SELECT
DATE(run_datetime),
COUNT(DISTINCT sample_id)
FROM patient_results
GROUP BY DATE(run_datetime)
ORDER BY 1;
.........................................
SELECT
sample_id,
patient_initials,
patient_program,
analyte_code,
result_value
FROM patient_results
WHERE patient_program='ACTG'
LIMIT 20;
........................................
SELECT
sample_id,
qc_level,
analyte_code,
result_value
FROM patient_results
WHERE assay_group='HBA1C'
ORDER BY run_datetime;
.......................................

SELECT
DATE(run_datetime),
analyte_code,
COUNT(*)
FROM calibrations
GROUP BY DATE(run_datetime), analyte_code
ORDER BY 1,2;
......................................
