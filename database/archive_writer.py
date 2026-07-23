import os

from database.db import db
from database.value_utils import field, date_value


class ArchiveWriter:

    @staticmethod
    def create_from_header(filename, fields):

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO archive_files
            (
                filename,
                archive_start,
                archive_end,
                archive_version,
                operator_name
            )
            VALUES (%s,%s,%s,%s,%s)
            RETURNING archive_id
            """,
            (
                os.path.basename(filename),
                date_value(field(fields,4)),
                date_value(field(fields,5)),
                field(fields,3),
                field(fields,9)
            )
        )

        return cursor.fetchone()[0]


    @staticmethod
    def create_minimal(filename):

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO archive_files(filename)
            VALUES(%s)
            RETURNING archive_id
            """,
            (os.path.basename(filename),)
        )

        return cursor.fetchone()[0]


    @staticmethod
    def log(
            archive_id,
            lines_read,
            parsed_ok,
            errors,
            parser_version="1.0"
    ):

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO parser_log
            (
                archive_id,
                lines_read,
                parsed_ok,
                errors,
                parser_version
            )
            VALUES(%s,%s,%s,%s,%s)
            """,
            (
                archive_id,
                lines_read,
                parsed_ok,
                errors,
                parser_version
            )
        )