from parser.archive_reader import ArchiveReader

ARCHIVE_FILE = "archive/I400 plus Archive 05_01_2026 - 05_31_2026.txt"

reader = ArchiveReader(ARCHIVE_FILE)
archive_id = reader.process()

print(f"\nFinished. archive_id={archive_id}")
