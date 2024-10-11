from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnalyticsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Analytics')
        layout.addWidget(label)
