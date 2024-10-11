from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from ui.login_screen import LoginScreen

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Splash Screen')
        self.setGeometry(100, 100, 600, 400)
        
        # Layout setup
        layout = QVBoxLayout(self)
        label = QLabel('Welcome to the Application!')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Timer to switch to login after 3 seconds
        QTimer.singleShot(3000, self.show_login)

    def show_login(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()
