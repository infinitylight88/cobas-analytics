from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from dashboard.widgets.data_table import DataTable
from dashboard.services.qc_service import QCService


class QCPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.table = DataTable()

        layout.addWidget(self.table)

        self.load()

    def load(self):

        rows = QCService.all()

        headers = [

            "Date",

            "Analyte",

            "Level",

            "Value",

            "Target"

        ]

        self.table.load(headers, rows)