# import sys
# import requests
# from PySide6.QtCore import Qt, QDate
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QPushButton,
#     QMessageBox, QDateEdit, QTextEdit, QStackedWidget, QHBoxLayout
# )

# API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual backend URL

# class LoginWindow(QWidget):
#     def __init__(self, switch_to_dashboard_callback, set_auth_token_callback):
#         super().__init__()
#         self.switch_to_dashboard_callback = switch_to_dashboard_callback
#         self.set_auth_token_callback = set_auth_token_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Login", alignment=Qt.AlignCenter))

#         self.email_input = QLineEdit(self)
#         self.email_input.setPlaceholderText("Email")
#         layout.addWidget(self.email_input)

#         self.password_input = QLineEdit(self)
#         self.password_input.setPlaceholderText("Password")
#         self.password_input.setEchoMode(QLineEdit.Password)
#         layout.addWidget(self.password_input)

#         self.login_button = QPushButton("Login", self)
#         self.login_button.clicked.connect(self.login)
#         layout.addWidget(self.login_button)

#         self.setLayout(layout)

#     def login(self):
#         email = self.email_input.text()
#         password = self.password_input.text()

#         if not email or not password:
#             QMessageBox.warning(self, "Input Error", "Email and password cannot be empty.")
#             return

#         try:
#             response = requests.post(f"{API_BASE_URL}/users/login", json={"email": email, "password": password})
#            # response.raise_for_status()  ## causes internal server error

#             data = response.json()
#             self.set_auth_token_callback(data["access_token"])  # Set the authentication token
#             self.switch_to_dashboard_callback()  # Switch to the dashboard
#         except requests.exceptions.HTTPError as http_err:
#             QMessageBox.warning(self, 'Error', f'Login failed. HTTP error: {http_err}')
#         except Exception as err:
#             QMessageBox.warning(self, 'Error', f'An error occurred: {err}')


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.auth_token = None
#         self.stacked_widget = QStackedWidget(self)

#         self.login_window = LoginWindow(self.switch_to_dashboard, self.set_auth_token)
#         self.dashboard = Dashboard(self.logout)
#         self.recruitment = RecruitmentModule(self.switch_to_dashboard)
#         self.onboarding = OnboardingModule(self.switch_to_dashboard)
#         self.payroll = PayrollModule(self.switch_to_dashboard)
#         self.performance = PerformanceModule(self.switch_to_dashboard)
#         self.analytics = AnalyticsModule(self.switch_to_dashboard)

#         self.stacked_widget.addWidget(self.login_window)  # Index 0
#         self.stacked_widget.addWidget(self.dashboard)  # Index 1
#         self.stacked_widget.addWidget(self.recruitment)  # Index 2
#         self.stacked_widget.addWidget(self.onboarding)  # Index 3
#         self.stacked_widget.addWidget(self.payroll)  # Index 4
#         self.stacked_widget.addWidget(self.performance)  # Index 5
#         self.stacked_widget.addWidget(self.analytics)  # Index 6

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.stacked_widget)

#     def set_auth_token(self, token):
#         self.auth_token = token
#         self.recruitment.set_auth_token(token)

#     def switch_to_dashboard(self):
#         print("Switching to dashboard")  # Add a print statement to track the function call
#         self.stacked_widget.setCurrentIndex(1)

#     def logout(self):
#         self.auth_token = None  # Clear the auth token
#         self.stacked_widget.setCurrentIndex(0)  # Go back to login screen


# class Dashboard(QWidget):
#     def __init__(self, logout_callback):
#         super().__init__()
#         self.logout_callback = logout_callback
#         self.initUI()  # Ensure the UI is initialized when the Dashboard is created

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Welcome to Horizon", alignment=Qt.AlignCenter))

#         self.recruitment_button = QPushButton("Recruitment Module", self)
#         self.recruitment_button.clicked.connect(self.switch_to_recruitment)
#         layout.addWidget(self.recruitment_button)

#         self.onboarding_button = QPushButton("Onboarding Module", self)
#         self.onboarding_button.clicked.connect(self.switch_to_onboarding)
#         layout.addWidget(self.onboarding_button)

#         self.payroll_button = QPushButton("Payroll Module", self)
#         self.payroll_button.clicked.connect(self.switch_to_payroll)
#         layout.addWidget(self.payroll_button)

#         self.performance_button = QPushButton("Performance Management Module", self)
#         self.performance_button.clicked.connect(self.switch_to_performance)
#         layout.addWidget(self.performance_button)

#         self.analytics_button = QPushButton("Analytics Module", self)
#         self.analytics_button.clicked.connect(self.switch_to_analytics)
#         layout.addWidget(self.analytics_button)

#         self.logout_button = QPushButton("Logout", self)
#         self.logout_button.clicked.connect(self.logout_callback)  # Handle logout
#         layout.addWidget(self.logout_button)

#         self.setLayout(layout)

#     def switch_to_recruitment(self):
#         self.parent().setCurrentIndex(2)

#     def switch_to_onboarding(self):
#         self.parent().setCurrentIndex(3)

#     def switch_to_payroll(self):
#         self.parent().setCurrentIndex(4)

#     def switch_to_performance(self):
#         self.parent().setCurrentIndex(5)

#     def switch_to_analytics(self):
#         self.parent().setCurrentIndex(6)


# class RecruitmentModule(QWidget):
#     def __init__(self, return_to_dashboard_callback):
#         super().__init__()
#         self.auth_token = None
#         self.return_to_dashboard_callback = return_to_dashboard_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Recruitment Module", alignment=Qt.AlignCenter))

#         self.job_title_input = QLineEdit(self)
#         self.job_title_input.setPlaceholderText("Job Title")
#         layout.addWidget(self.job_title_input)

#         self.job_description_input = QTextEdit(self)
#         self.job_description_input.setPlaceholderText("Job Description")
#         layout.addWidget(self.job_description_input)

#         self.add_job_button = QPushButton("Add Job", self)
#         self.add_job_button.clicked.connect(self.add_job)
#         layout.addWidget(self.add_job_button)

#         self.job_table = QTableWidget(self)
#         self.job_table.setColumnCount(2)
#         self.job_table.setHorizontalHeaderLabels(['Job Title', 'Job Description'])
#         layout.addWidget(self.job_table)

#         self.load_jobs_button = QPushButton("Load Job Postings", self)
#         self.load_jobs_button.clicked.connect(self.load_jobs)
#         layout.addWidget(self.load_jobs_button)

#         self.back_button = QPushButton("Back to Dashboard", self)
#         self.back_button.clicked.connect(self.return_to_dashboard_callback)
#         layout.addWidget(self.back_button)

#         self.setLayout(layout)

#     def set_auth_token(self, token):
#         self.auth_token = token

#     def add_job(self):
#         title = self.job_title_input.text()
#         description = self.job_description_input.toPlainText()

#         if not title or not description:
#             QMessageBox.warning(self, "Input Error", "Job title and description cannot be empty.")
#             return

#         headers = {"Authorization": f"Bearer {self.auth_token}"}
#         data = {"title": title, "description": description}

#         try:
#             response = requests.post(f"{API_BASE_URL}/jobs", json=data, headers=headers)
#             response.raise_for_status()
#             QMessageBox.information(self, 'Success', 'Job posted successfully.')
#             self.load_jobs()  # Reload the job postings
#         except requests.exceptions.HTTPError as http_err:
#             QMessageBox.warning(self, 'Error', f'Failed to post job. HTTP error: {http_err}')
#         except Exception as err:
#             QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

#     def load_jobs(self):
#         self.job_table.clearContents()
#         self.job_table.setRowCount(0)

#         headers = {"Authorization": f"Bearer {self.auth_token}"}
#         try:
#             response = requests.get(f"{API_BASE_URL}/jobs", headers=headers)
#             response.raise_for_status()

#             jobs = response.json()
#             for job in jobs:
#                 row_position = self.job_table.rowCount()
#                 self.job_table.insertRow(row_position)
#                 self.job_table.setItem(row_position, 0, QTableWidgetItem(job['title']))
#                 self.job_table.setItem(row_position, 1, QTableWidgetItem(job['description']))
#         except requests.exceptions.HTTPError as http_err:
#             QMessageBox.warning(self, 'Error', f'Failed to load job postings. HTTP error: {http_err}')
#         except Exception as err:
#             QMessageBox.warning(self, 'Error', f'An error occurred: {err}')


# class OnboardingModule(QWidget):
#     def __init__(self, return_to_dashboard_callback):
#         super().__init__()
#         self.return_to_dashboard_callback = return_to_dashboard_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Onboarding Module", alignment=Qt.AlignCenter))

#         self.employee_name_input = QLineEdit(self)
#         self.employee_name_input.setPlaceholderText("Employee Name")
#         layout.addWidget(self.employee_name_input)

#         self.date_of_joining_input = QDateEdit(self)
#         self.date_of_joining_input.setCalendarPopup(True)
#         self.date_of_joining_input.setDate(QDate.currentDate())
#         layout.addWidget(self.date_of_joining_input)

#         self.onboard_employee_button = QPushButton("Onboard Employee", self)
#         self.onboard_employee_button.clicked.connect(self.onboard_employee)
#         layout.addWidget(self.onboard_employee_button)

#         self.back_button = QPushButton("Back to Dashboard", self)
#         self.back_button.clicked.connect(self.return_to_dashboard_callback)
#         layout.addWidget(self.back_button)

#         self.setLayout(layout)

#     def onboard_employee(self):
#         employee_name = self.employee_name_input.text()
#         date_of_joining = self.date_of_joining_input.date().toString(Qt.ISODate)

#         if not employee_name:
#             QMessageBox.warning(self, "Input Error", "Employee name cannot be empty.")
#             return

#         # Add onboarding logic here

#         QMessageBox.information(self, 'Success', 'Employee onboarded successfully.')


# class PayrollModule(QWidget):
#     def __init__(self, return_to_dashboard_callback):
#         super().__init__()
#         self.return_to_dashboard_callback = return_to_dashboard_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Payroll Module", alignment=Qt.AlignCenter))

#         self.salary_input = QLineEdit(self)
#         self.salary_input.setPlaceholderText("Salary")
#         layout.addWidget(self.salary_input)

#         self.pay_button = QPushButton("Pay Salary", self)
#         self.pay_button.clicked.connect(self.pay_salary)
#         layout.addWidget(self.pay_button)

#         self.back_button = QPushButton("Back to Dashboard", self)
#         self.back_button.clicked.connect(self.return_to_dashboard_callback)
#         layout.addWidget(self.back_button)

#         self.setLayout(layout)

#     def pay_salary(self):
#         salary = self.salary_input.text()

#         if not salary:
#             QMessageBox.warning(self, "Input Error", "Salary cannot be empty.")
#             return

#         # Add payroll logic here

#         QMessageBox.information(self, 'Success', 'Salary paid successfully.')


# class PerformanceModule(QWidget):
#     def __init__(self, return_to_dashboard_callback):
#         super().__init__()
#         self.return_to_dashboard_callback = return_to_dashboard_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Performance Management Module", alignment=Qt.AlignCenter))

#         self.review_input = QTextEdit(self)
#         self.review_input.setPlaceholderText("Performance Review")
#         layout.addWidget(self.review_input)

#         self.submit_review_button = QPushButton("Submit Review", self)
#         self.submit_review_button.clicked.connect(self.submit_review)
#         layout.addWidget(self.submit_review_button)

#         self.back_button = QPushButton("Back to Dashboard", self)
#         self.back_button.clicked.connect(self.return_to_dashboard_callback)
#         layout.addWidget(self.back_button)

#         self.setLayout(layout)

#     def submit_review(self):
#         review = self.review_input.toPlainText()

#         if not review:
#             QMessageBox.warning(self, "Input Error", "Performance review cannot be empty.")
#             return

#         # Add performance review logic here

#         QMessageBox.information(self, 'Success', 'Performance review submitted successfully.')


# class AnalyticsModule(QWidget):
#     def __init__(self, return_to_dashboard_callback):
#         super().__init__()
#         self.return_to_dashboard_callback = return_to_dashboard_callback
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Analytics Module", alignment=Qt.AlignCenter))

#         self.generate_report_button = QPushButton("Generate Report", self)
#         self.generate_report_button.clicked.connect(self.generate_report)
#         layout.addWidget(self.generate_report_button)

#         self.back_button = QPushButton("Back to Dashboard", self)
#         self.back_button.clicked.connect(self.return_to_dashboard_callback)
#         layout.addWidget(self.back_button)

#         self.setLayout(layout)

#     def generate_report(self):
#         # Add analytics report generation logic here
#         QMessageBox.information(self, 'Success', 'Report generated successfully.')


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     main_window = MainWindow()
#     main_window.show()

#     sys.exit(app.exec())

import sys
from PySide6.QtWidgets import QApplication
from ui.login_screen import LoginScreen
from ui.signup_screen import SignupScreen  # Added import
from ui.dashboard_screen import DashboardScreen
from ui.payroll_screen import PayrollScreen
from ui.analytics_screen import AnalyticsScreen
from ui.hr_screen import HrScreen  # Added import
from ui.support_screen import SupportScreen  # Added import
from ui.document_upload_screen import DocumentUploadScreen  # Added import
from ui.profile_screen import ProfileScreen  # Added import
from ui.notifications_screen import NotificationsScreen  # Added import
from ui.language_screen import LanguageScreen  # Added import
from ui.privacy_screen import PrivacyScreen  # Added import
from ui.about_screen import AboutScreen  # Added import

class MainWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_window = None
        self.auth_token = None

    def start(self):
        self.show_login()
        return self.app.exec()

    def show_login(self):
        self.current_window = LoginScreen(self.on_login_success)
        self.current_window.show()

    def on_login_success(self, token):
        self.auth_token = token
        self.show_dashboard()

    def show_dashboard(self):
        self.current_window.close()
        self.current_window = DashboardScreen(
            self.auth_token,
            self.show_login,
            self.show_payroll,
            self.show_analytics,
            self.show_hr,  # Added method for HR screen
            self.show_support,  # Added method for Support screen
            self.show_document_upload,  # Added method for Document Upload screen
            self.show_profile,  # Added method for Profile screen
            self.show_notifications,  # Added method for Notifications screen
            self.show_language,  # Added method for Language settings
            self.show_privacy,  # Added method for Privacy policy
            self.show_about  # Added method for About us
        )
        self.current_window.show()

    def show_payroll(self):
        self.current_window.close()
        self.current_window = PayrollScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_analytics(self):
        self.current_window.close()
        self.current_window = AnalyticsScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_hr(self):
        self.current_window.close()
        self.current_window = HrScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_support(self):
        self.current_window.close()
        self.current_window = SupportScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_document_upload(self):
        self.current_window.close()
        self.current_window = DocumentUploadScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_profile(self):
        self.current_window.close()
        self.current_window = ProfileScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_notifications(self):
        self.current_window.close()
        self.current_window = NotificationsScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_language(self):
        self.current_window.close()
        self.current_window = LanguageScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_privacy(self):
        self.current_window.close()
        self.current_window = PrivacyScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

    def show_about(self):
        self.current_window.close()
        self.current_window = AboutScreen(self.auth_token, self.show_dashboard)
        self.current_window.show()

if __name__ == "__main__":
    main_window = MainWindow()
    sys.exit(main_window.start())
