import sys
import requests
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QPushButton, 
    QMessageBox, QDateEdit, QTextEdit, QStackedWidget, QHBoxLayout
)

API_BASE_URL = "http://localhost:8000"  # Replace with your actual backend URL

class LoginWindow(QWidget):
    def __init__(self, switch_to_dashboard_callback, set_auth_token_callback):
        super().__init__()
        self.switch_to_dashboard_callback = switch_to_dashboard_callback
        self.set_auth_token_callback = set_auth_token_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Login", alignment=Qt.AlignCenter))

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
            response.raise_for_status()

            data = response.json()
            self.set_auth_token_callback(data["token"])  # Set the authentication token
            self.switch_to_dashboard_callback()  # Switch to the dashboard
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Login failed. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class Dashboard(QWidget):
    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to Horizon HR Dashboard", alignment=Qt.AlignCenter))

        self.recruitment_button = QPushButton("Recruitment Module", self)
        self.recruitment_button.clicked.connect(self.switch_to_recruitment)
        layout.addWidget(self.recruitment_button)

        self.onboarding_button = QPushButton("Onboarding Module", self)
        self.onboarding_button.clicked.connect(self.switch_to_onboarding)
        layout.addWidget(self.onboarding_button)

        self.payroll_button = QPushButton("Payroll Module", self)
        self.payroll_button.clicked.connect(self.switch_to_payroll)
        layout.addWidget(self.payroll_button)

        self.performance_button = QPushButton("Performance Management Module", self)
        self.performance_button.clicked.connect(self.switch_to_performance)
        layout.addWidget(self.performance_button)

        self.analytics_button = QPushButton("Analytics Module", self)
        self.analytics_button.clicked.connect(self.switch_to_analytics)
        layout.addWidget(self.analytics_button)

        self.setLayout(layout)

    def switch_to_recruitment(self):
        self.parent().setCurrentIndex(2)

    def switch_to_onboarding(self):
        self.parent().setCurrentIndex(3)

    def switch_to_payroll(self):
        self.parent().setCurrentIndex(4)

    def switch_to_performance(self):
        self.parent().setCurrentIndex(5)

    def switch_to_analytics(self):
        self.parent().setCurrentIndex(6)

class RecruitmentModule(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_token = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Recruitment Module", alignment=Qt.AlignCenter))

        self.job_title_input = QLineEdit(self)
        self.job_title_input.setPlaceholderText("Job Title")
        layout.addWidget(self.job_title_input)

        self.job_description_input = QTextEdit(self)
        self.job_description_input.setPlaceholderText("Job Description")
        layout.addWidget(self.job_description_input)

        self.add_job_button = QPushButton("Add Job", self)
        self.add_job_button.clicked.connect(self.add_job)
        layout.addWidget(self.add_job_button)

        self.job_table = QTableWidget(self)
        self.job_table.setColumnCount(2)
        self.job_table.setHorizontalHeaderLabels(['Job Title', 'Job Description'])
        layout.addWidget(self.job_table)

        self.load_jobs_button = QPushButton("Load Job Postings", self)
        self.load_jobs_button.clicked.connect(self.load_jobs)
        layout.addWidget(self.load_jobs_button)

        self.setLayout(layout)

    def set_auth_token(self, token):
        self.auth_token = token

    def add_job(self):
        title = self.job_title_input.text()
        description = self.job_description_input.toPlainText()

        if not title or not description:
            QMessageBox.warning(self, "Input Error", "Job title and description cannot be empty.")
            return

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        data = {"title": title, "description": description}

        try:
            response = requests.post(f"{API_BASE_URL}/jobs", json=data, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Job posted successfully.')
            self.load_jobs()  # Reload the job postings
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to post job. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

    def load_jobs(self):
        self.job_table.clearContents()
        self.job_table.setRowCount(0)

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = requests.get(f"{API_BASE_URL}/jobs", headers=headers)
            response.raise_for_status()

            jobs = response.json()
            for job in jobs:
                row_position = self.job_table.rowCount()
                self.job_table.insertRow(row_position)
                self.job_table.setItem(row_position, 0, QTableWidgetItem(job['title']))
                self.job_table.setItem(row_position, 1, QTableWidgetItem(job['description']))
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to load job postings. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class OnboardingModule(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Onboarding Module", alignment=Qt.AlignCenter))

        self.employee_name_input = QLineEdit(self)
        self.employee_name_input.setPlaceholderText("Employee Name")
        layout.addWidget(self.employee_name_input)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.start_date_input)

        self.onboarding_notes_input = QTextEdit(self)
        self.onboarding_notes_input.setPlaceholderText("Onboarding Notes")
        layout.addWidget(self.onboarding_notes_input)

        self.submit_button = QPushButton("Submit Onboarding Info", self)
        self.submit_button.clicked.connect(self.submit_onboarding_info)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_onboarding_info(self):
        name = self.employee_name_input.text()
        start_date = self.start_date_input.date().toString(Qt.ISODate)
        notes = self.onboarding_notes_input.toPlainText()

        if not name or not notes:
            QMessageBox.warning(self, "Input Error", "Name and notes cannot be empty.")
            return

        data = {
            "employee_name": name,
            "start_date": start_date,
            "onboarding_notes": notes
        }

        try:
            response = requests.post(f"{API_BASE_URL}/onboarding", json=data)
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Onboarding info submitted successfully.')
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to submit onboarding info. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class PayrollModule(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Payroll Module", alignment=Qt.AlignCenter))

        self.payroll_table = QTableWidget(self)
        self.payroll_table.setColumnCount(3)
        self.payroll_table.setHorizontalHeaderLabels(['Employee Name', 'Salary', 'Pay Period'])
        layout.addWidget(self.payroll_table)

        self.update_payroll_button = QPushButton("Update Payroll Data", self)
        self.update_payroll_button.clicked.connect(self.update_payroll_data)
        layout.addWidget(self.update_payroll_button)

        self.setLayout(layout)

    def update_payroll_data(self):
        self.payroll_table.clearContents()
        self.payroll_table.setRowCount(0)

        try:
            response = requests.get(f"{API_BASE_URL}/payroll")
            response.raise_for_status()

            payroll_data = response.json()
            for entry in payroll_data:
                row_position = self.payroll_table.rowCount()
                self.payroll_table.insertRow(row_position)
                self.payroll_table.setItem(row_position, 0, QTableWidgetItem(entry['employee_name']))
                self.payroll_table.setItem(row_position, 1, QTableWidgetItem(str(entry['salary'])))
                self.payroll_table.setItem(row_position, 2, QTableWidgetItem(entry['pay_period']))
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to load payroll data. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class PerformanceModule(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Performance Management Module", alignment=Qt.AlignCenter))

        self.employee_name_input = QLineEdit(self)
        self.employee_name_input.setPlaceholderText("Employee Name")
        layout.addWidget(self.employee_name_input)

        self.performance_score_input = QLineEdit(self)
        self.performance_score_input.setPlaceholderText("Performance Score")
        layout.addWidget(self.performance_score_input)

        self.add_performance_button = QPushButton("Add Performance Data", self)
        self.add_performance_button.clicked.connect(self.add_performance_data)
        layout.addWidget(self.add_performance_button)

        self.performance_table = QTableWidget(self)
        self.performance_table.setColumnCount(2)
        self.performance_table.setHorizontalHeaderLabels(['Employee Name', 'Performance Score'])
        layout.addWidget(self.performance_table)

        self.load_performance_button = QPushButton("Load Performance Data", self)
        self.load_performance_button.clicked.connect(self.load_performance_data)
        layout.addWidget(self.load_performance_button)

        self.setLayout(layout)

    def add_performance_data(self):
        name = self.employee_name_input.text()
        score = self.performance_score_input.text()

        if not name or not score:
            QMessageBox.warning(self, "Input Error", "Employee name and score cannot be empty.")
            return

        data = {"employee_name": name, "performance_score": score}

        try:
            response = requests.post(f"{API_BASE_URL}/performance", json=data)
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Performance data added successfully.')
            self.load_performance_data()  # Reload the performance data
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to add performance data. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

    def load_performance_data(self):
        self.performance_table.clearContents()
        self.performance_table.setRowCount(0)

        try:
            response = requests.get(f"{API_BASE_URL}/performance")
            response.raise_for_status()

            performance_data = response.json()
            for entry in performance_data:
                row_position = self.performance_table.rowCount()
                self.performance_table.insertRow(row_position)
                self.performance_table.setItem(row_position, 0, QTableWidgetItem(entry['employee_name']))
                self.performance_table.setItem(row_position, 1, QTableWidgetItem(str(entry['performance_score'])))
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to load performance data. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class AnalyticsModule(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Analytics Module", alignment=Qt.AlignCenter))

        self.analytics_text = QLabel("Analytics data will be displayed here.", alignment=Qt.AlignCenter)
        layout.addWidget(self.analytics_text)

        self.load_analytics_button = QPushButton("Load Analytics", self)
        self.load_analytics_button.clicked.connect(self.load_analytics)
        layout.addWidget(self.load_analytics_button)

        self.setLayout(layout)

    def load_analytics(self):
        try:
            response = requests.get(f"{API_BASE_URL}/analytics")
            response.raise_for_status()

            analytics_data = response.json()
            # Display analytics data in a suitable format, e.g., graphs, tables, etc.
            self.analytics_text.setText(str(analytics_data))
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.warning(self, 'Error', f'Failed to load analytics data. HTTP error: {http_err}')
        except Exception as err:
            QMessageBox.warning(self, 'Error', f'An error occurred: {err}')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.auth_token = None
        self.stacked_widget = QStackedWidget(self)

        self.login_window = LoginWindow(self.switch_to_dashboard, self.set_auth_token)
        self.dashboard = Dashboard()
        self.recruitment = RecruitmentModule()
        self.onboarding = OnboardingModule()
        self.payroll = PayrollModule()
        self.performance = PerformanceModule()
        self.analytics = AnalyticsModule()

        self.stacked_widget.addWidget(self.login_window)  # Index 0
        self.stacked_widget.addWidget(self.dashboard)  # Index 1
        self.stacked_widget.addWidget(self.recruitment)  # Index 2
        self.stacked_widget.addWidget(self.onboarding)  # Index 3
        self.stacked_widget.addWidget(self.payroll)  # Index 4
        self.stacked_widget.addWidget(self.performance)  # Index 5
        self.stacked_widget.addWidget(self.analytics)  # Index 6

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

    def set_auth_token(self, token):
        self.auth_token = token
        self.recruitment.set_auth_token(token)

    def switch_to_dashboard(self):
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
