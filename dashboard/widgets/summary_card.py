from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel
from PySide6.QtCore import Qt


class SummaryCard(QFrame):

    def __init__(self,title):

        super().__init__()

        self.setStyleSheet("""

        QFrame{

            background:white;

            border:1px solid #E5E7EB;

            border-radius:12px;

        }

        """)

        layout=QVBoxLayout(self)

        self.title=QLabel(title)

        self.title.setStyleSheet("""

        font-size:11px;

        color:#6B7280;

        """)

        self.value=QLabel("0")

        self.value.setAlignment(Qt.AlignCenter)

        self.value.setStyleSheet("""

        font-size:28px;

        font-weight:bold;

        color:#111827;

        """)

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.value)

    def setValue(self,value):

        self.value.setText(str(value))