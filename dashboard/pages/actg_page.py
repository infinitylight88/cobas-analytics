from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from dashboard.services.analytics_service import AnalyticsService


class ACTGPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        ###########################################################

        title = QLabel("ACTG Analytics")

        title.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
                padding:8px;
            }
        """)

        layout.addWidget(title)

        ###########################################################

        self.refreshButton = QPushButton("Refresh")

        layout.addWidget(self.refreshButton)

        ###########################################################

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Study",
            "Samples",
            "HbA1c",
            "Latest Run"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        ###########################################################

        self.refreshButton.clicked.connect(
            self.refresh
        )

        self.refresh()

    ###############################################################

    def refresh(self):

        data = AnalyticsService.actg()

        self.table.setRowCount(len(data))

        for r, row in enumerate(data):

            self.table.setItem(
                r,
                0,
                QTableWidgetItem(
                    str(row.get("study", ""))
                )
            )

            self.table.setItem(
                r,
                1,
                QTableWidgetItem(
                    str(row.get("samples", ""))
                )
            )

            self.table.setItem(
                r,
                2,
                QTableWidgetItem(
                    str(row.get("hba1c", ""))
                )
            )

            self.table.setItem(
                r,
                3,
                QTableWidgetItem(
                    str(row.get("latest_run", ""))
                )
            )