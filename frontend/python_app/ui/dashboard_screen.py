import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget,
    QPushButton, QHBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy
)

class DashboardScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_layout = QHBoxLayout()

        # Title for Main Content Area
        self.main_title = QLabel("Main Content Area")
        self.main_title.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        
        # Stacked widget for content area
        self.stacked_widget = QStackedWidget()

        # Adding different screens to the stacked widget
        self.analytics_screen = QLabel("Analytics Screen")
        self.payroll_screen = QLabel("Payroll Screen")
        self.hr_screen = QLabel("HR Screen")
        self.support_screen = QLabel("Support Screen")
        self.document_upload_screen = QLabel("Document Upload Screen")
        self.profile_screen = QLabel("Profile Screen")
        self.notifications_screen = QLabel("Notifications Screen")
        self.language_screen = QLabel("Language Screen")
        self.privacy_screen = QLabel("Privacy Screen")
        self.about_screen = QLabel("About Screen")

        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.analytics_screen)
        self.stacked_widget.addWidget(self.payroll_screen)
        self.stacked_widget.addWidget(self.hr_screen)
        self.stacked_widget.addWidget(self.support_screen)
        self.stacked_widget.addWidget(self.document_upload_screen)
        self.stacked_widget.addWidget(self.profile_screen)
        self.stacked_widget.addWidget(self.notifications_screen)
        self.stacked_widget.addWidget(self.language_screen)
        self.stacked_widget.addWidget(self.privacy_screen)
        self.stacked_widget.addWidget(self.about_screen)

        # Layout for content area
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.main_title)
        content_layout.addWidget(self.stacked_widget)

        # Central widget for main content
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # Create left drawer with spacing between buttons
        self.left_drawer = self.create_drawer([
            ("Analytics", self.show_analytics),
            ("Payroll", self.show_payroll),
            ("HR", self.show_hr),
            ("Support", self.show_support),
            ("Upload Document", self.show_document_upload),
            ("Profile", self.show_profile),
        ])

        # Create right drawer with spacing between buttons
        self.right_drawer = self.create_drawer([
            ("Notifications", self.show_notifications),
            ("Language", self.show_language),
            ("Privacy", self.show_privacy),
            ("About", self.show_about),
            ("Toggle Theme", self.toggle_theme_button)  # Add Theme Toggle Button to the right drawer
        ])

        # Add widgets to main layout
        main_layout.addWidget(self.left_drawer)
        main_layout.addWidget(content_widget)
        main_layout.addWidget(self.right_drawer)

        # Set main layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Ensure light mode is the default
        self.current_theme = "light"
        self.apply_theme("light")

    def create_drawer(self, items):
        """ Helper function to create a drawer with buttons """
        drawer = QFrame()
        drawer.setFixedWidth(250)
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Space between buttons

        for text, callback in items:
            button = QPushButton(text)
            button.setStyleSheet(self.get_button_style(theme="light"))
            button.clicked.connect(callback)
            layout.addWidget(button)

        layout.addStretch()  # Push items to top
        drawer.setLayout(layout)
        drawer.setStyleSheet("""
            background-color: lightgrey;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
        """)
        return drawer

    def get_button_style(self, theme="light"):
        """ Generate button styles based on the current theme """
        if theme == "light":
            return """
                QPushButton {
                    background-color: white;
                    color: black;
                    border: 1px solid #ccc;
                    padding: 10px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #444;
                    color: white;
                    border: 1px solid #555;
                    padding: 10px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """

    def show_analytics(self):
        self.stacked_widget.setCurrentIndex(0)
        self.main_title.setText("Analytics Screen")

    def show_payroll(self):
        self.stacked_widget.setCurrentIndex(1)
        self.main_title.setText("Payroll Screen")

    def show_hr(self):
        self.stacked_widget.setCurrentIndex(2)
        self.main_title.setText("HR Screen")

    def show_support(self):
        self.stacked_widget.setCurrentIndex(3)
        self.main_title.setText("Support Screen")

    def show_document_upload(self):
        self.stacked_widget.setCurrentIndex(4)
        self.main_title.setText("Document Upload Screen")

    def show_profile(self):
        self.stacked_widget.setCurrentIndex(5)
        self.main_title.setText("Profile Screen")

    def show_notifications(self):
        self.stacked_widget.setCurrentIndex(6)
        self.main_title.setText("Notifications Screen")

    def show_language(self):
        self.stacked_widget.setCurrentIndex(7)
        self.main_title.setText("Language Screen")

    def show_privacy(self):
        self.stacked_widget.setCurrentIndex(8)
        self.main_title.setText("Privacy Screen")

    def show_about(self):
        self.stacked_widget.setCurrentIndex(9)
        self.main_title.setText("About Screen")

    def toggle_theme_button(self):
        # Toggle between light and dark themes
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        # Set the window background and font colors
        if theme == "light":
            self.setStyleSheet("background-color: white; color: black;")
        else:
            self.setStyleSheet("background-color: #333; color: white;")

        # Update drawer styles
        for drawer in [self.left_drawer, self.right_drawer]:
            drawer.setStyleSheet(f"""
                background-color: {'lightgrey' if theme == 'light' else '#444'};
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            """)

        # Update button styles
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            button.setStyleSheet(self.get_button_style(theme=theme))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardScreen()
    window.show()
    sys.exit(app.exec())
