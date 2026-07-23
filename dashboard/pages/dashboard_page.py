from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
)

from dashboard.widgets.summary_card import SummaryCard
from dashboard.widgets.section_header import SectionHeader
from dashboard.widgets.toolbar import Toolbar
from dashboard.widgets.activity_table import ActivityTable
from dashboard.widgets.status_bar import StatusBar

from dashboard.services.dashboard_service import DashboardService


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        root = QVBoxLayout(self)

        self.toolbar = Toolbar()

        root.addWidget(self.toolbar)

        cards = QHBoxLayout()

        self.archive = SummaryCard("Archives")

        self.patient = SummaryCard("Patients")

        self.qc = SummaryCard("QC")

        self.cal = SummaryCard("Calibrations")

        cards.addWidget(self.archive)

        cards.addWidget(self.patient)

        cards.addWidget(self.qc)

        cards.addWidget(self.cal)

        root.addLayout(cards)

        root.addWidget(SectionHeader("Recent Activity"))

        self.table = ActivityTable()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Patients",
            "QC",
            "Calibration",
            "Archive"
        ])

        root.addWidget(self.table)

        self.status = StatusBar()

        root.addWidget(self.status)

        self.toolbar.refresh.clicked.connect(self.refresh)

        self.refresh()

    def refresh(self):

        summary = DashboardService.summary()

        self.archive.setValue(summary["archives"])

        self.patient.setValue(summary["patients"])

        self.qc.setValue(summary["qc"])

        self.cal.setValue(summary["calibrations"])

        activity = DashboardService.activity()

        self.table.setRowCount(len(activity))

        for r, row in enumerate(activity):

            self.table.setItem(
                r,0,
                QTableWidgetItem(str(row["date"]))
            )

            self.table.setItem(
                r,1,
                QTableWidgetItem(str(row["patients"]))
            )

            self.table.setItem(
                r,2,
                QTableWidgetItem(str(row["qc"]))
            )

            self.table.setItem(
                r,3,
                QTableWidgetItem(str(row["calibrations"]))
            )

            self.table.setItem(
                r,4,
                QTableWidgetItem(str(row["archives"]))
            )

        self.status.setStatus("Connected to API")