from parser.record_factory import RecordFactory
from database.archive_writer import ArchiveWriter
from database.db import db
from database.raw_writer import RawWriter

class ArchiveReader:

    def __init__(self, filename):

        self.filename = filename

        self.factory = RecordFactory()

    def process(self):

        archive_id = None
        lines_read = 0
        parsed_ok = 0
        errors = 0

        try:
            with open(self.filename, encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    line = line.rstrip("\n")

                    if not line:
                        continue

                    lines_read += 1
                    fields = line.split("\t")

                    if archive_id is None:
                        if fields[0] == "0":
                            archive_id = ArchiveWriter.create_from_header(
                                self.filename,
                                fields
                            )
                        else:
                            archive_id = ArchiveWriter.create_minimal(
                                self.filename
                            )

                    raw_id = RawWriter.write(
                        archive_id,
                        line_number,
                        int(fields[0]) if fields[0].isdigit() else None,
                        line
                    )

                    processor = self.factory.create(fields)

                    processor.process(
                        archive_id,
                        raw_id,
                        fields
                    )

            if archive_id is not None:
                ArchiveWriter.log(
                    archive_id,
                    lines_read,
                    parsed_ok,
                    errors
                )

            db.commit()
            return archive_id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()
