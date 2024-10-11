# dashboard_screen.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from ui.analytics_screen import AnalyticsScreen
from ui.payroll_screen import PayrollScreen
from ui.hr_screen import HrScreen
from ui.support_screen import SupportScreen
from ui.document_upload_screen import DocumentUploadScreen
from ui.profile_screen import ProfileScreen

class DashboardScreen(QMainWindow):
    def __init__(self, auth_token, show_login, show_payroll, show_analytics, show_hr, show_support, show_document_upload, show_profile, show_notifications, show_language, show_privacy, show_about):
        super().__init__()
        self.setWindowTitle('Dashboard')
        self.setGeometry(100, 100, 800, 600)

        self.auth_token = auth_token
        self.show_login = show_login
        self.show_payroll = show_payroll
        self.show_analytics = show_analytics
        self.show_hr = show_hr
        self.show_support = show_support
        self.show_document_upload = show_document_upload
        self.show_profile = show_profile
        self.show_notifications = show_notifications
        self.show_language = show_language
        self.show_privacy = show_privacy
        self.show_about = show_about
        
        # Central widget with stacked pages for each screen
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Add all screens
        self.analytics_screen = AnalyticsScreen()
        self.stacked_widget.addWidget(self.analytics_screen)

        self.payroll_screen = PayrollScreen()
        self.stacked_widget.addWidget(self.payroll_screen)

        self.hr_screen = HrScreen()
        self.stacked_widget.addWidget(self.hr_screen)

        self.support_screen = SupportScreen()
        self.stacked_widget.addWidget(self.support_screen)

        self.document_upload_screen = DocumentUploadScreen()
        self.stacked_widget.addWidget(self.document_upload_screen)

        self.profile_screen = ProfileScreen()
        self.stacked_widget.addWidget(self.profile_screen)

        # Optionally, add a sidebar menu or navigation
        # For now, it defaults to the first screen

    def switch_screen(self, index):
        self.stacked_widget.setCurrentIndex(index)
