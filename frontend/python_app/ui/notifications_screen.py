from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class NotificationsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Notifications')
        layout.addWidget(label)
