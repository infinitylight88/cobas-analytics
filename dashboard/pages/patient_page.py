from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit
)

from dashboard.widgets.data_table import DataTable
from dashboard.services.patient_service import PatientService


class PatientPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search accession..."
        )

        self.refreshButton = QPushButton("Refresh")

        top.addWidget(self.search)
        top.addWidget(self.refreshButton)

        layout.addLayout(top)

        self.table = DataTable()

        layout.addWidget(self.table)

        self.refreshButton.clicked.connect(
            self.load
        )

        self.load()

    def load(self):

        rows = PatientService.all()

        headers = [
            "Sample",
            "Patient",
            "Analyte",
            "Result",
            "Status"
        ]

        self.table.load(headers, rows)