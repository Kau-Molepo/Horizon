from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SupportScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Support')
        layout.addWidget(label)
