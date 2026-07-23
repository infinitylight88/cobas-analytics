from database.db import db
from database.value_utils import date_value, field, numeric, timestamp


class PatientWriter:
    """
    Handles ONLY patient results.

    By the time execution reaches this file,
    ActivityClassifier has already excluded:

        • QC
        • Calibration
        • Maintenance
        • Host events

    Therefore every record reaching this writer is
    assumed to be a patient result.
    """

    @staticmethod
    def write(archive_id, raw_id, fields,
              activity_type, assay_group, qc_level):

        patient_identifier = PatientWriter.extract_patient_identifier(fields)

        patient_id = PatientWriter._patient_id(
            fields,
            patient_identifier
        )

        # 🚀 EXTRACTION FOR NEW COLUMNS:
        # Extract clean initials (e.g., "MA") if it's an ACTG record
        col3_val = field(fields, 3)
        patient_initials = col3_val.replace("PT INITIALS:", "").strip() if (col3_val and "PT INITIALS:" in col3_val.upper()) else None
        
        # Determine the program type
        patient_program = "ACTG" if patient_identifier else None

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT result_id
            FROM patient_results
            WHERE raw_id=%s
            LIMIT 1
            """,
            (raw_id,)
        )

        existing = cursor.fetchone()

        sample_id = PatientWriter.extract_accession(fields)

        # Base values tuple (15 standard fields)
        values = (
            archive_id,
            patient_id,
            timestamp(field(fields, 1)),
            sample_id,
            field(fields, 6),
            field(fields, 2),
            field(fields, 2),
            numeric(field(fields, 10)),
            field(fields, 7),
            field(fields, 8),
            field(fields, 12),
            field(fields, 11),
            activity_type,
            assay_group,
            qc_level,
        )

        if existing:

            cursor.execute(
                """
                UPDATE patient_results
                SET
                    archive_id=%s,
                    patient_id=%s,
                    run_datetime=%s,
                    sample_id=%s,
                    sample_type=%s,
                    analyte_code=%s,
                    analyte_name=%s,
                    result_value=%s,
                    units=%s,
                    reference_flag=%s,
                    status=%s,
                    result_flag=%s,
                    activity_type=%s,
                    assay_group=%s,
                    qc_level=%s,
                    patient_identifier=%s,  -- Added to UPDATE
                    patient_initials=%s,    -- Added to UPDATE
                    patient_program=%s      -- Added to UPDATE
                WHERE result_id=%s
                """,
                values + (patient_identifier, patient_initials, patient_program, existing[0])
            )

            return

        # ✅ FIXED: Now has exactly 19 target columns and 19 placeholder values
        cursor.execute(
            """
            INSERT INTO patient_results
            (
                archive_id,
                patient_id,
                patient_identifier,
                patient_initials,
                patient_program,
                run_datetime,
                sample_id,
                sample_type,
                analyte_code,
                analyte_name,
                result_value,
                units,
                reference_flag,
                status,
                result_flag,
                activity_type,
                assay_group,
                qc_level,
                raw_id
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                archive_id,
                patient_id,
                patient_identifier,
                patient_initials,
                patient_program,
            ) + values[2:] + (raw_id,) # Dynamically reassembles everything into 19 items safely
        )

    @staticmethod
    def extract_accession(fields):

        col4 = field(fields, 3)
        col5 = field(fields, 4)
        col6 = field(fields, 5)

        # Routine patient
        if (
            str(col4).lower() == "undefined"
            and str(col5).lower() == "undefined"
        ):
            return col6

        # JCMB accession
        if col6 and str(col6).upper().startswith("JCMB"):
            return col6

        # 133 accession
        if col6 and str(col6).startswith("133"):
            return col6

        # ACTG patient
        return None

    # ---------------------------------------------------------
    # Returns patient identifier.
    #
    # Routine patient -> None
    #
    # ACTG:
    #
    # PT INITIALS:MA
    # 1243234F
    #
    # We store the ACTG ID (124....)
    # because it uniquely identifies the patient.
    # ---------------------------------------------------------

    @staticmethod
    def extract_patient_identifier(fields):

        initials = field(fields, 3)
        actg_id = field(fields, 4)

        if (
            initials
            and initials.upper().startswith("PT INITIALS")
        ):
            return actg_id

        return None

    @staticmethod
    def _patient_id(fields, patient_identifier=None):

        if patient_identifier is None:
            return None

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE patient_identifier=%s
            LIMIT 1
            """,
            (patient_identifier,)
        )

        existing = cursor.fetchone()

        if existing:
            return existing[0]

        cursor.execute(
            """
            INSERT INTO patients
            (
                patient_identifier,
                patient_initials,
                sex,
                date_of_birth,
                patient_program
            )
            VALUES
            (
                %s,%s,%s,%s,%s
            )
            RETURNING patient_id
            """,
            (
                patient_identifier,
                field(fields, 3).replace("PT INITIALS:", "").strip(),
                field(fields, 13),
                date_value(field(fields, 14)),
                "ACTG"
            )
        )

        return cursor.fetchone()[0]