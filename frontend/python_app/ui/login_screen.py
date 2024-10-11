import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox

API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual backend URL

class LoginScreen(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Login", alignment=Qt.AlignCenter))

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Email and password cannot be empty.")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/users/login", json={"email": email, "password": password})
            response.raise_for_status()

            data = response.json()
            self.on_login_success(data["access_token"])
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Login failed. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')