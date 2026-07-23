import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget
)

from dashboard.pages.dashboard_page import DashboardPage
from dashboard.pages.patient_page import PatientPage
from dashboard.pages.qc_page import QCPage
from dashboard.pages.calibration_page import CalibrationPage
from dashboard.pages.actg_page import ACTGPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cobas Analytics")
        self.resize(1650, 900)

        container = QWidget()
        self.setCentralWidget(container)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        ##########################################################
        # LEFT SIDEBAR
        ##########################################################

        self.menu = QListWidget()

        self.menu.setFixedWidth(240)

        self.menu.setStyleSheet("""

            QListWidget{
                background:#1f2937;
                color:white;
                border:none;
                font-size:14px;
                padding-top:20px;
            }

            QListWidget::item{
                height:42px;
                padding-left:18px;
            }

            QListWidget::item:selected{
                background:#2563eb;
            }

            QListWidget::item:hover{
                background:#374151;
            }

        """)

        pages = [

            "Dashboard",
            "Patients",
            "Quality Control",
            "Calibrations",
            "ACTG Results"

        ]

        for p in pages:

            item = QListWidgetItem(p)

            item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter
            )

            self.menu.addItem(item)

        ##########################################################
        # RIGHT CONTENT
        ##########################################################

        self.stack = QStackedWidget()

        self.stack.setStyleSheet("""

            QStackedWidget{
                background:#f5f7fb;
            }

        """)

        ##########################################################
        # PAGES
        ##########################################################

        self.dashboardPage = DashboardPage()

        self.patientPage = PatientPage()

        self.qcPage = QCPage()

        self.calibrationPage = CalibrationPage()

        self.actg = ACTGPage()

        self.stack.addWidget(
            self.dashboardPage
        )

        self.stack.addWidget(
            self.patientPage
        )

        self.stack.addWidget(
            self.qcPage
        )

        self.stack.addWidget(
            self.calibrationPage
        )

        self.stack.addWidget(
            self.actg
        )

        

        layout.addWidget(self.menu)

        layout.addWidget(
            self.stack,
            stretch=1
        )

        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = MainWindow()

    window.show()

    sys.exit(app.exec())