from database.db import db
from database.value_utils import field, numeric, timestamp


class QCWriter:
    """
    ============================================================================
    QC Writer

    Stores every Record 20 produced by the Cobas Integra.

    A QC record contains:

        • Date/time
        • Analyte
        • Control name (PCCC1 / PCCC2)
        • Control lot
        • Application code
        • Reagent lot
        • Units
        • Measured value
        • Assigned target value
        • SD
        • Lower limit
        • Upper limit

    This information will later power:

        ✓ Daily QC reports
        ✓ Levy Jennings charts
        ✓ Westgard Rules
        ✓ QC Coverage reports
        ✓ Lot-to-Lot verification
        ✓ ISO15189 evidence
        ✓ CAP inspections

    Every QC run is stored exactly once using raw_id.
    ============================================================================
    """

    @staticmethod
    def write(archive_id, raw_id, fields):

        cursor = db.cursor()

        # ------------------------------------------------------------------
        # Prevent duplicate imports
        # ------------------------------------------------------------------

        cursor.execute(
            """
            SELECT qc_id
            FROM qc_results
            WHERE raw_id=%s
            LIMIT 1
            """,
            (raw_id,)
        )

        existing = cursor.fetchone()

        values = (

            # ----------------------------------------------------------
            # Archive references
            # ----------------------------------------------------------

            archive_id,
            raw_id,

            # ----------------------------------------------------------
            # Date & Time
            # ----------------------------------------------------------

            timestamp(field(fields, 1)),

            # ----------------------------------------------------------
            # Test
            # ----------------------------------------------------------

            field(fields, 2),

            # ----------------------------------------------------------
            # QC Information
            # ----------------------------------------------------------

            field(fields, 3),        # PCCC1 / PCCC2
            field(fields, 4),        # Control Lot
            field(fields, 5),        # Application Code
            field(fields, 6),        # Reagent Lot

            # ----------------------------------------------------------
            # Units
            # ----------------------------------------------------------

            field(fields, 7),

            # ----------------------------------------------------------
            # Numerical QC values
            # ----------------------------------------------------------

            numeric(field(fields, 12)),      # Assigned Target

            numeric(field(fields, 10)),      # Instrument Result

            numeric(field(fields, 13)),      # SD

            numeric(field(fields, 16)),      # Lower Limit

            numeric(field(fields, 17)),      # Upper Limit

            # ----------------------------------------------------------
            # Dashboard Classification
            # ----------------------------------------------------------

            "QC",

            "CHEMISTRY",

            field(fields, 3),        # QC Level

            # ----------------------------------------------------------
            # Extra analytics
            # ----------------------------------------------------------

            numeric(field(fields, 11))       # Instrument Signal

        )

        # ==============================================================
        # Update existing record
        # ==============================================================

        if existing:

            cursor.execute(
                """
                UPDATE qc_results
                SET

                    archive_id=%s,
                    raw_id=%s,
                    run_datetime=%s,

                    analyte_code=%s,

                    control_name=%s,
                    control_lot=%s,

                    application_code=%s,
                    reagent_lot=%s,

                    units=%s,

                    assigned_value=%s,
                    measured_value=%s,
                    sd=%s,

                    lower_limit=%s,
                    upper_limit=%s,

                    activity_type=%s,
                    assay_group=%s,
                    qc_level=%s,

                    instrument_signal=%s

                WHERE qc_id=%s
                """,
                values + (existing[0],)
            )

            return

        # ==============================================================
        # Insert new QC record
        # ==============================================================

        cursor.execute(
            """
            INSERT INTO qc_results
            (

                archive_id,
                raw_id,
                run_datetime,

                analyte_code,

                control_name,
                control_lot,

                application_code,
                reagent_lot,

                units,

                assigned_value,
                measured_value,
                sd,

                lower_limit,
                upper_limit,

                activity_type,
                assay_group,
                qc_level,

                instrument_signal

            )

            VALUES
            (

                %s,%s,%s,

                %s,

                %s,%s,

                %s,%s,

                %s,

                %s,%s,%s,

                %s,%s,

                %s,%s,%s,

                %s

            )
            """,
            values
        )