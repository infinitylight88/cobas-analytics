from PySide6.QtWidgets import QTableWidget


class ActivityTable(QTableWidget):

    def __init__(self):

        super().__init__()

        self.setAlternatingRowColors(True)

        self.verticalHeader().hide()

        self.setSelectionBehavior(
            self.SelectionBehavior.SelectRows
        )

        self.horizontalHeader().setStretchLastSection(True)