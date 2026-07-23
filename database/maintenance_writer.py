from database.db import db
from database.value_utils import field, timestamp


class MaintenanceWriter:
    """
    Stores maintenance records.

    Examples

        Probe Wash
        Daily Maintenance
        Weekly Maintenance
        Calibration Check
    """

    @staticmethod
    def write(archive_id, raw_id, fields):

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM maintenance
            WHERE raw_id=%s
            """,
            (raw_id,)
        )

        if cursor.fetchone():
            return

        cursor.execute(
            """
            INSERT INTO maintenance
            (
                archive_id,
                raw_id,
                run_datetime,
                maintenance_type,
                maintenance_code,
                description
            )

            VALUES
            (
                %s,%s,%s,%s,%s,%s
            )
            """,
            (
                archive_id,
                raw_id,
                timestamp(field(fields, 1)),
                field(fields, 2),
                field(fields, 3),
                field(fields, 4)
            )
        )