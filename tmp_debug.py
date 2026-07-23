from unittest.mock import patch
from database.patient_writer import PatientWriter

class FakeCursor:
    def __init__(self):
        self.executed = []
        self.fetchone_calls = 0
    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        print('EXEC', sql.strip().splitlines()[0])
    def fetchone(self):
        self.fetchone_calls += 1
        result = (1,) if self.fetchone_calls == 1 else None
        print('FETCHONE', result)
        return result

cursor = FakeCursor()
class FakeDb:
    def cursor(self):
        return cursor

with patch('database.patient_writer.db', FakeDb()), patch.object(PatientWriter, '_patient_id', return_value=77):
    PatientWriter.write(1, 2, ['40','2026-05-04 16:02:04','ALB2','PT INITIALS:BM','1243217A','7','SER','g/dL','','','3.9','0.01412','R','F','2000-06-14'])
print('EXECUTED', cursor.executed)
