from database.db import db
from database.value_utils import field, timestamp


class HostWriter:
    """
    Stores Cobas host communication events.

    These are NOT patient results.

    Examples

        Host Connected
        Download Complete
        Rack Loaded
        Instrument Ready
    """

    @staticmethod
    def write(archive_id, raw_id, fields):

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM host_events
            WHERE raw_id=%s
            """,
            (raw_id,)
        )

        if cursor.fetchone():
            return

        cursor.execute(
            """
            INSERT INTO host_events
            (
                archive_id,
                raw_id,
                run_datetime,
                event_code,
                event_text
            )

            VALUES
            (
                %s,%s,%s,%s,%s
            )
            """,
            (
                archive_id,
                raw_id,
                timestamp(field(fields, 1)),
                field(fields, 2),
                field(fields, 3)
            )
        )