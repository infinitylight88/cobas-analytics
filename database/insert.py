from database.db import db


class Insert:

    @staticmethod
    def raw_record(
            archive_id,
            line_number,
            record_type,
            raw_text):

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT raw_id
            FROM raw_records
            WHERE archive_id = %s
              AND line_number = %s
              AND record_type = %s
              AND raw_text = %s
            LIMIT 1
            """,
            (
                archive_id,
                line_number,
                record_type,
                raw_text
            )
        )

        existing = cursor.fetchone()

        if existing:
            return existing[0]

        cursor.execute(
            """
            INSERT INTO raw_records
            (
                archive_id,
                line_number,
                record_type,
                raw_text
            )
            VALUES
            (%s,%s,%s,%s)
            RETURNING raw_id
            """,
            (
                archive_id,
                line_number,
                record_type,
                raw_text
            )
        )

        return cursor.fetchone()[0]
