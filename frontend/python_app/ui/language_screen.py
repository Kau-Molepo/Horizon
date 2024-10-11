from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class LanguageScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('App Language')
        layout.addWidget(label)
