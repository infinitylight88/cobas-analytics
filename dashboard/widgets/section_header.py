from PySide6.QtWidgets import QLabel


class SectionHeader(QLabel):

    def __init__(self,text):

        super().__init__(text)

        self.setStyleSheet("""

        font-size:16px;

        font-weight:bold;

        color:#111827;

        padding-top:12px;

        padding-bottom:6px;

        """)