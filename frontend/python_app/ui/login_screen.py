import requests
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PySide6.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PySide6.QtGui import QMovie  # Import QMovie for GIF animations

API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual backend URL
LOGIN_ERROR = "Login failed. Please check your credentials."
INPUT_ERROR = "Email and password cannot be empty."
SUCCESS_MESSAGE = "Login successful!"

class LoginThread(QThread):
    update_status = Signal(dict)

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password

    def run(self):
        try:
            response = requests.post(f"{API_BASE_URL}/users/login", json={"email": self.email, "password": self.password})
            # response.raise_for_status()(causes server internal error)
            data = response.json()
            self.update_status.emit(data)
        except requests.exceptions.HTTPError as http_err:
            self.update_status.emit({"error": f"{LOGIN_ERROR} HTTP error: {http_err}"})
        except Exception as err:
            self.update_status.emit({"error": f"An error occurred: {err}"})

class LoginScreen(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.initUI()

    def initUI(self):
        # Set the background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(221, 0, 0))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title label
        title_label = QLabel("Admin Login", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        layout.addWidget(title_label)

        # Spacer for top margin
        layout.addItem(QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Email input field with icon
        self.email_input = QLineEdit(self)
        self.email_input.setFixedHeight(35)
        self.email_input.setPlaceholderText("Email")
        email_icon = QIcon("B:/PLP/Final Project/Horizon/frontend/python_app/assets/mail-svgrepo-com-white.png")
        self.email_input.addAction(email_icon, QLineEdit.LeadingPosition)
        self.email_input.setClearButtonEnabled(True)
        self.email_input.setStyleSheet("border-radius: 12px; padding: 8px; font-size: 18px; background-color: #424242;" "padding-left: 5px;")
        layout.addWidget(self.email_input)

        # Spacer for top margin
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Password input field with icon
        self.password_input = QLineEdit(self)
        self.password_input.setFixedHeight(35)
        self.password_input.setPlaceholderText("Password")
        password_icon = QIcon("B:/PLP/Final Project/Horizon/frontend/python_app/assets/lock-svgrepo-com-white.png")
        self.password_input.addAction(password_icon, QLineEdit.LeadingPosition)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setStyleSheet("border-radius: 12px; padding: 8px; font-size: 18px; background-color: #424242;" "padding-left: 5px;")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Spacer for top margin
        layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("border-radius: 12px; padding: 8px 100px; background-color: #4487ff; color: white; font-size: 18px; font-weight: bold;")
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.start_login_thread)
        layout.addWidget(self.login_button)
        layout.setAlignment(self.login_button, Qt.AlignHCenter)

        # Feedback message area
        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Loading animation label
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_movie = QMovie("B:/PLP/Final Project/Horizon/frontend/python_app/assets/loading.gif")  # Path to the loading GIF
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.hide()  # Hide initially
        layout.addWidget(self.loading_label)

        # Spacer for bottom margin
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)
        self.setWindowTitle("Login")

    def start_login_thread(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Validate input
        if not email or not password:
            self.feedback_label.setText(INPUT_ERROR)
            self.feedback_label.setStyleSheet("color: red;font-size: 16px;")
            return

        # Disable the login button and show the loading animation
        self.login_button.setEnabled(False)
        self.login_button.setHidden(True)
        self.feedback_label.setText("")
        self.loading_label.show()
        self.loading_movie.start()

        # Start login thread
        self.thread = LoginThread(email, password)
        self.thread.update_status.connect(self.handle_login_response)
        self.thread.start()

    def handle_login_response(self, response):
        # Stop the loading animation and re-enable the button
        self.loading_movie.stop()
        self.loading_label.hide()
        self.login_button.setEnabled(True)

        if "error" in response:
            self.feedback_label.setText(response["error"])
            self.feedback_label.setStyleSheet("color: red;")
        else:
            self.feedback_label.setText(SUCCESS_MESSAGE)
            self.feedback_label.setStyleSheet("color: green;")
            user_id = response.get("user_id")
            access_token = response.get("access_token")
            role = response.get("role")
            self.on_login_success(user_id, access_token, role)