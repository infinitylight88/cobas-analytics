from database.db import db


class RawWriter:

    @staticmethod
    def write(
            archive_id,
            line_number,
            record_code,
            raw_text
    ):

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO raw_records
            (
                archive_id,
                line_number,
                record_code,
                raw_text
            )
            VALUES(%s,%s,%s,%s)
            RETURNING raw_id
            """,
            (
                archive_id,
                line_number,
                record_code,
                raw_text
            )
        )

        return cursor.fetchone()[0]