from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import database
from PyQt5.QtWidgets import QDialog
from base_class import BaseWindow
from PyQt5.QtGui import QFont


class LoginApp(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        font = QFont()
        font.setPointSize(14)  # You can adjust this value as needed
        self.setFont(font)
        current_size = self.size()
        new_width = int(current_size.width() * 1.5)
        new_height = int(current_size.height() * 1.5)
        self.resize(new_width, new_height)

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.setWindowTitle("Login")
        self.show()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if database.check_credentials(username, password):
            self.accept()  # Close the login window upon successful login
        else:
            QMessageBox.warning(self, "Error", "Incorrect username or password!")
