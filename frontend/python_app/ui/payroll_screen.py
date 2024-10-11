from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PayrollScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Payroll')
        layout.addWidget(label)
