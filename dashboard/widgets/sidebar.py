from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)


class Sidebar(QWidget):

    pageChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)

        self.setObjectName("Sidebar")

        layout = QVBoxLayout(self)

        title = QLabel("COBAS\nANALYTICS")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("SidebarTitle")

        layout.addWidget(title)

        self.buttons = {}

        pages = [
            "Dashboard",
            "Patients",
            "QC",
            "Calibrations",
            "Reports",
            "Settings"
        ]

        for page in pages:

            btn = QPushButton(page)
            btn.clicked.connect(
                lambda checked=False,
                p=page: self.pageChanged.emit(p)
            )

            layout.addWidget(btn)

            self.buttons[page] = btn

        layout.addStretch()