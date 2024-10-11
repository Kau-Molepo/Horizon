from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HrScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Human Resources (HR)')
        layout.addWidget(label)
