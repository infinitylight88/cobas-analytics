from PySide6.QtWidgets import QWidget,QHBoxLayout,QPushButton


class Toolbar(QWidget):

    def __init__(self):

        super().__init__()

        layout=QHBoxLayout(self)

        layout.addStretch()

        self.refresh=QPushButton("Refresh")

        self.export=QPushButton("Export")

        layout.addWidget(self.refresh)

        layout.addWidget(self.export)