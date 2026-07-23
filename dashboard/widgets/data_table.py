from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class DataTable(QTableWidget):

    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

    def load(self, headers, rows):
        self.setSortingEnabled(False)
        self.clearContents()
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setRowCount(len(rows))

        for r, row in enumerate(rows):
            # 🚀 Map UI headers to the exact SQLAlchemy model attributes
            # Adjust these if your PatientResult model uses different database column names!
            attributes = [
                "sample_id",  # Maps to 'Sample'
                "patient_id",  # Maps to 'Patient' (or 'patient_name' if it exists)
                "analyte_code",  # Maps to 'Analyte'
                "result_value",  # Maps to 'Result' (or 'value')
                "status",  # Maps to 'Status'
            ]

            for c, attr in enumerate(attributes):
                # Safely get the attribute value from the object
                val = getattr(row, attr, "")
                self.setItem(r, c, QTableWidgetItem(str(val)))

        self.setSortingEnabled(True)
