from database.db import db
from database.value_utils import field, numeric, timestamp


class CalibrationWriter:
    """
    Stores every calibration performed by Cobas.

    These records later allow us to answer:

        • When was an analyte calibrated?
        • Which reagent lot was used?
        • Which calibration factor was applied?
        • How many calibrations per month?
    """

    @staticmethod
    def write(archive_id, raw_id, fields):

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM calibrations
            WHERE raw_id=%s
            """,
            (raw_id,)
        )

        if cursor.fetchone():
            return

        cursor.execute(
            """
            INSERT INTO calibrations
            (
                archive_id,
                raw_id,
                run_datetime,
                analyte_code,
                calibration_type,
                reagent_lot,
                units,
                upper_limit,
                lower_limit,
                slope,
                "offset",
                factor
            )

            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                archive_id,
                raw_id,

                timestamp(field(fields,1)),

                field(fields,2),

                field(fields,3),

                field(fields,6),

                field(fields,7),

                numeric(field(fields,14)),

                numeric(field(fields,15)),

                numeric(field(fields,20)),

                numeric(field(fields,23)),

                numeric(field(fields,19))
            )
        )