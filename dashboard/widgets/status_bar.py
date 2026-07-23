from PySide6.QtWidgets import QWidget,QHBoxLayout,QLabel


class StatusBar(QWidget):

    def __init__(self):

        super().__init__()

        layout=QHBoxLayout(self)

        self.status=QLabel("Ready")

        layout.addWidget(self.status)

        layout.addStretch()

    def setStatus(self,text):

        self.status.setText(text)