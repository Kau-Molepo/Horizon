from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from ui.login_screen import LoginScreen

class SignupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Signup Screen')
        self.setGeometry(100, 100, 600, 400)
        
        # Layout setup
        layout = QVBoxLayout(self)
        label = QLabel('Signup')
        layout.addWidget(label)
        
        # Signup Button
        signup_button = QPushButton('Signup')
        signup_button.clicked.connect(self.show_login)
        layout.addWidget(signup_button)

    def show_login(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()
