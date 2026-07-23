from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from dashboard.widgets.data_table import DataTable
from dashboard.services.calibration_service import CalibrationService


class CalibrationPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.table = DataTable()

        layout.addWidget(self.table)

        self.load()

    def load(self):

        rows = CalibrationService.all()

        headers = [

            "Date",

            "Assay",

            "Lot",

            "Status"

        ]

        self.table.load(headers, rows)