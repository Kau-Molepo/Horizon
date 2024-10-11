from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PrivacyScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Privacy Policy')
        layout.addWidget(label)
