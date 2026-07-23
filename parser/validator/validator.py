"""
=========================================================
Cobas Archive Validation

Runs after an import and checks whether the parser
stored every record correctly.

This validator is intended for development only.

Eventually it can become a Dashboard Health Check.
=========================================================
"""

from database.db import db


class Validator:

    @staticmethod
    def run():

        cursor = db.cursor()

        print("\n")
        print("=" * 70)
        print("COBAS IMPORT VALIDATION")
        print("=" * 70)

        Validator.patient_summary(cursor)
        Validator.qc_summary(cursor)
        Validator.calibration_summary(cursor)
        Validator.host_summary(cursor)

        print("=" * 70)
        print("Validation Finished")
        print("=" * 70)
        print()

    # --------------------------------------------------

    @staticmethod
    def patient_summary(cursor):

        print("\nPATIENT RESULTS")

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_results
        """)

        print("Total Results :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(DISTINCT sample_id)
            FROM patient_results
            WHERE sample_id IS NOT NULL
        """)

        print("Unique Samples :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(DISTINCT analyte_code)
            FROM patient_results
        """)

        print("Analytes :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_results
            WHERE assay_group='HBA1C'
        """)

        print("HbA1C Results :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_results
            WHERE patient_program='ACTG'
        """)

        print("ACTG Results :", cursor.fetchone()[0])

    # --------------------------------------------------

    @staticmethod
    def qc_summary(cursor):

        print("\nQC RESULTS")

        cursor.execute("""
            SELECT COUNT(*)
            FROM qc_results
        """)

        print("QC Rows :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(DISTINCT analyte_code)
            FROM qc_results
        """)

        print("QC Analytes :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(DISTINCT control_name)
            FROM qc_results
        """)

        print("QC Controls :", cursor.fetchone()[0])

    # --------------------------------------------------

    @staticmethod
    def calibration_summary(cursor):

        print("\nCALIBRATIONS")

        cursor.execute("""
            SELECT COUNT(*)
            FROM calibrations
        """)

        print("Calibration Rows :", cursor.fetchone()[0])

        cursor.execute("""
            SELECT COUNT(DISTINCT analyte_code)
            FROM calibrations
        """)

        print("Calibration Analytes :", cursor.fetchone()[0])

    # --------------------------------------------------

    @staticmethod
    def host_summary(cursor):

        print("\nHOST EVENTS")

        cursor.execute("""
            SELECT COUNT(*)
            FROM host_events
        """)

        print("Host Events :", cursor.fetchone()[0])