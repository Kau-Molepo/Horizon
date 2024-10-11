from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('About Us')
        layout.addWidget(label)
