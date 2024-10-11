from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SplashScreen(QWidget):
    def __init__(self, on_splash_finished):
        super().__init__()

        self.on_splash_finished = on_splash_finished  # Callback to handle transition

        self.setWindowTitle("Splash Screen")
        # self.setFixedSize(800, 600)  # Set fixed size for the splash screen
        self.setAutoFillBackground(True)

        # Set gradient background
        gradient = QPalette()
        gradient.setColor(QPalette.Window, QColor("#2196F3"))  # Blue color
        self.setPalette(gradient)

        # Create layout and add logo and text
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # App Logo or Icon
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("font-size: 100px; color: white;")
        self.logo_label.setText("🌐")  # Replace with your app logo
        layout.addWidget(self.logo_label)

        # App Name
        self.app_name_label = QLabel("Horizon")
        self.app_name_label.setStyleSheet("font-size: 40px; font-weight: bold; color: white;")
        layout.addWidget(self.app_name_label)

        self.setLayout(layout)

        # Set up the fade-in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

        # Timer to trigger the transition after 3 seconds
        QTimer.singleShot(3000, self.handle_splash_finished)

    def handle_splash_finished(self):
        self.on_splash_finished()  # Call the transition method
        self.close()  # Close the splash screen
