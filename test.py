# from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QDateEdit, QPushButton, QLabel
# from PyQt5.QtCore import QDate
#
# class CustomDateWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.layout = QVBoxLayout(self)
#
#         # Date edit setup
#         self.date_edit = QDateEdit(self)
#         self.date_edit.setCalendarPopup(True)
#         self.date_edit.setDate(QDate.currentDate())
#         self.date_edit.setButtonSymbols(QDateEdit.NoButtons)  # Hide the default buttons
#
#         # Custom buttons for the date edit
#         self.up_button = QPushButton("▲", self)
#         self.down_button = QPushButton("▼", self)
#
#         # Connect buttons to their functions
#         self.up_button.clicked.connect(self.increment_date)
#         self.down_button.clicked.connect(self.decrement_date)
#
#         # Button layout
#         button_layout = QHBoxLayout()
#         button_layout.addWidget(self.up_button)
#         button_layout.addWidget(self.down_button)
#
#         # Combine date edit and buttons in the layout
#         self.layout.addWidget(self.date_edit)
#         self.layout.addLayout(button_layout)
#
#     def increment_date(self):
#         current_date = self.date_edit.date()
#         new_date = current_date.addDays(1)  # Increase the date by one day
#         self.date_edit.setDate(new_date)
#
#     def decrement_date(self):
#         current_date = self.date_edit.date()
#         new_date = current_date.addDays(-1)  # Decrease the date by one day
#         self.date_edit.setDate(new_date)
#
# if __name__ == "__main__":
#     app = QApplication([])
#     widget = CustomDateWidget()
#     widget.show()
#     app.exec_()

import re

def f1(data):
    p = re.compile('(?P[A-Z]{2,3}) (?P[0-9]{3})')
    return p.search(data)

obj = f1('CS 101')