import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from ui.splash_screen import SplashScreen
from ui.login_screen import LoginScreen
from ui.signup_screen import SignupScreen
from ui.dashboard_screen import DashboardScreen
from ui.analytics_screen import AnalyticsScreen
from ui.payroll_screen import PayrollScreen
from ui.hr_screen import HrScreen
from ui.support_screen import SupportScreen
from ui.document_upload_screen import DocumentUploadScreen
from ui.profile_screen import ProfileScreen
from ui.notifications_screen import NotificationsScreen
from ui.language_screen import LanguageScreen
from ui.privacy_screen import PrivacyScreen
from ui.about_screen import AboutScreen

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.setStyle("Fusion")  # Set a default style

        self.window = QStackedWidget()
        self.window.setWindowTitle("Horizon")

        # Initialize screens
        self.splash_screen = SplashScreen(self.show_login_screen)  # Pass the transition handler
        self.login_screen = LoginScreen(self.handle_login_success)
        self.signup_screen = SignupScreen()
        self.dashboard_screen = DashboardScreen()
        self.analytics_screen = AnalyticsScreen()
        self.payroll_screen = PayrollScreen()
        self.hr_screen = HrScreen()
        self.support_screen = SupportScreen()
        self.document_upload_screen = DocumentUploadScreen()
        self.profile_screen = ProfileScreen()
        self.notifications_screen = NotificationsScreen()
        self.language_screen = LanguageScreen()
        self.privacy_screen = PrivacyScreen()
        self.about_screen = AboutScreen()

        # Add screens to the stacked widget
        self.window.addWidget(self.splash_screen)
        self.window.addWidget(self.login_screen)
        self.window.addWidget(self.signup_screen)
        self.window.addWidget(self.dashboard_screen)
        self.window.addWidget(self.analytics_screen)
        self.window.addWidget(self.payroll_screen)
        self.window.addWidget(self.hr_screen)
        self.window.addWidget(self.support_screen)
        self.window.addWidget(self.document_upload_screen)
        self.window.addWidget(self.profile_screen)
        self.window.addWidget(self.notifications_screen)
        self.window.addWidget(self.language_screen)
        self.window.addWidget(self.privacy_screen)
        self.window.addWidget(self.about_screen)

        # self.window.setFixedSize(800, 600)  # Set fixed size for the main window
        self.window.show()  # Show the main window

    def show_login_screen(self):
        """Transition to the Login Screen after the splash screen."""
        self.transition_to(self.login_screen)

    def handle_login_success(self, user_id, access_token, role):
        """Handle successful login and transition to the dashboard."""
        print(f"Login successful! User ID: {user_id}, Access Token: {access_token}, Role: {role}")
        self.transition_to(self.dashboard_screen)

    def transition_to(self, screen):
        """Handle screen transitions."""
        self.window.setCurrentWidget(screen)

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())
