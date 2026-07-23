from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class ChartCard(QWidget):

    def __init__(self, title, chart):

        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel(title)

        label.setStyleSheet("""
        font-size:16px;
        font-weight:bold;
        """)

        layout.addWidget(label)

        layout.addWidget(chart)

        self.setStyleSheet("""
        QWidget{

            background:white;
            border-radius:12px;

        }
        """)