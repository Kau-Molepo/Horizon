from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DocumentUploadScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Document Upload')
        layout.addWidget(label)
