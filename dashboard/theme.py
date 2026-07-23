PRIMARY = "#2563EB"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"

BACKGROUND = "#F4F6F9"

CARD = "#FFFFFF"

SIDEBAR = "#1F2937"

TEXT = "#111827"

SUBTEXT = "#6B7280"

BORDER = "#E5E7EB"

FONT = "Segoe UI"

STYLE = f"""

QMainWindow{{
background:{BACKGROUND};
}}

QWidget{{
font-family:{FONT};
font-size:10pt;
}}

QPushButton{{
background:{PRIMARY};
color:white;
padding:8px;
border-radius:8px;
}}

QPushButton:hover{{
background:#1D4ED8;
}}

QTableWidget{{
background:white;
gridline-color:{BORDER};
selection-background-color:#DBEAFE;
}}

QHeaderView::section{{
background:#F3F4F6;
padding:8px;
font-weight:bold;
}}

"""