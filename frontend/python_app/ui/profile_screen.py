from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ProfileScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Profile')
        layout.addWidget(label)
