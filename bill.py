import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QComboBox, QLineEdit, QDateEdit, QTextEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QTableWidget, QHBoxLayout
from base_class import BaseWindow
from database import *


class BillEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # Row 1
        self.house_number_label = QLabel('House Number')
        self.house_number_combo = QComboBox()
        # self.populate_houses_dropdown()

        self.room_number_label = QLabel('Room Number')
        self.room_number_combo = QComboBox()

        self.cts_number_label = QLabel('CTS Number')
        self.cts_number_line = QLineEdit()
        self.cts_number_line.setReadOnly(True)

        self.populate_houses_dropdown()  # This function populates the house_number_combo
        self.house_number_combo.currentIndexChanged.connect(self.house_changed)
        self.room_number_combo.currentIndexChanged.connect(self.room_changed)

        # Explicitly calling house_changed to update room and CTS fields based on the initially displayed house
        self.house_changed()
        layout.addWidget(self.house_number_label, 0, 0)
        layout.addWidget(self.house_number_combo, 0, 1)
        layout.addWidget(self.room_number_label, 0, 2)
        layout.addWidget(self.room_number_combo, 0, 3)
        layout.addWidget(self.cts_number_label, 0, 4)
        layout.addWidget(self.cts_number_line, 0, 5)

        # Row 2
        self.rent_month_label = QLabel('Rent For Month Of')
        self.rent_month_date = QDateEdit()
        self.rent_month_date.setDate(QDate.currentDate())
        layout.addWidget(self.rent_month_label, 1, 0)
        layout.addWidget(self.rent_month_date, 1, 1)  # Spanning across two columns for space

        # Row 3
        self.book_number_label = QLabel('Book Number')
        self.book_number_line = QLineEdit()
        self.bill_number_label = QLabel('Bill Number')
        self.bill_number_line = QLineEdit()
        layout.addWidget(self.book_number_label, 1, 2)
        layout.addWidget(self.book_number_line, 1, 3)
        layout.addWidget(self.bill_number_label, 1, 4)
        layout.addWidget(self.bill_number_line, 1, 5)

        # Row 4
        self.purpose_label = QLabel('Purpose For')
        self.purpose_line = QLineEdit()
        self.purpose_line.setText('For Residence')
        layout.addWidget(self.purpose_label, 2, 0)
        layout.addWidget(self.purpose_line, 2, 1)

        # Row 5
        self.rent_from_label = QLabel('Rent From')
        self.rent_from_date = QDateEdit()
        self.rent_from_date.setDate(QDate.currentDate())
        self.rent_to_label = QLabel('Rent To')
        self.rent_to_date = QDateEdit()
        layout.addWidget(self.rent_from_label, 2, 2)
        layout.addWidget(self.rent_from_date, 2, 3)
        layout.addWidget(self.rent_to_label, 2, 4)
        layout.addWidget(self.rent_to_date, 2, 5)

        self.rent_month_date.dateChanged.connect(self.update_rent_to_date)

        # Row 6
        self.amount_label = QLabel('@')
        self.amount_line = QLineEdit()
        self.amount_line.setText('350')
        layout.addWidget(self.amount_label, 3, 0)
        layout.addWidget(self.amount_line, 3, 1)

        # Row 7
        self.total_months_label = QLabel('Total Months')
        self.total_months_line = QLineEdit()
        layout.addWidget(self.total_months_label, 3, 2)
        layout.addWidget(self.total_months_line, 3, 3)

        # Row 8
        self.total_rupees_label = QLabel('Total Rupees')
        self.total_rupees_line = QLineEdit()
        layout.addWidget(self.total_rupees_label, 3, 4)
        layout.addWidget(self.total_rupees_line, 3, 5)

        # Row 9
        self.received_date_label = QLabel('Received Date')
        self.received_date = QDateEdit()
        self.received_date.setDate(QDate.currentDate())
        layout.addWidget(self.received_date_label, 4, 0)
        layout.addWidget(self.received_date, 4, 1)

        # Row 10
        self.extra_payment_label = QLabel('Extra Payment')
        self.extra_payment_line = QLineEdit()
        layout.addWidget(self.extra_payment_label, 4, 2)
        layout.addWidget(self.extra_payment_line, 4, 3)

        # Row 11
        self.agreement_date_label = QLabel('Agreement Date')
        self.agreement_date = QDateEdit()
        self.agreement_date.setDate(QDate.currentDate())
        layout.addWidget(self.agreement_date_label, 4, 4)
        layout.addWidget(self.agreement_date, 4, 5)

        self.notes_label = QLabel('Notes')
        self.notes_text = QTextEdit()
        self.notes_text.setFixedHeight(50)  # Set the fixed height for the QTextEdit

        # Add the QVBoxLayout to the main QGridLayout
        layout.addWidget(self.notes_label, 5, 0, 1, 5)
        layout.addWidget(self.notes_text, 5, 1, 1, 5)

        buttons_layout = QHBoxLayout()

        # Create Submit Button
        self.submit_button = QPushButton('Submit')
        # self.submit_button.clicked.connect(self.get_data)
        buttons_layout.addWidget(self.submit_button)

        # Create Print Button
        self.print_button = QPushButton('Print')
        # self.print_button.clicked.connect(self.print_data)  # You need to define the print_data method
        buttons_layout.addWidget(self.print_button)

        # Add the QHBoxLayout to the main QGridLayout, spanning across all 6 columns
        layout.addLayout(buttons_layout, 7, 1, 1, 5)  # Assuming row 7 is where you want the buttons

        self.bill_entry_table = QTableWidget(self)
        self.bill_entry_table.setColumnCount(10)  # Number of columns based on the fields you have
        self.bill_entry_table.setHorizontalHeaderLabels(["House No.", "Room No.", "CTS No.", "Name",
                                                         "Mobile", "DoD", "Notes", "Gender", "Edit", "Delete"])
        layout.addWidget(self.bill_entry_table, 8, 0, 1, 6)

    def update_rent_to_date(self, selected_date):
        """
        Slot to handle the dateChanged signal of the rent_month_date.
        It sets the date of rent_to_date to be the same as the selected_date.
        """
        self.rent_to_date.setDate(selected_date)

    def populate_houses_dropdown(self):
        houses = get_house_data()  # Replace with your DB call
        for house in houses:
            house_number, house_id = house[0], house[1]
            self.house_number_combo.addItem(house_number, house_id)

    def house_changed(self):
        current_house_id = self.house_number_combo.currentData()
        rooms = get_rooms_data_by_house_id(current_house_id)  # Replace with your DB call
        self.room_number_combo.clear()
        for room in rooms:
            room_name, room_id = room[0], room[1]
            print(room_name, room_id)
            self.room_number_combo.addItem(room_name, room_id)

    def room_changed(self):
        current_room_id = self.room_number_combo.currentData()
        cts_number = self.get_cts_number(current_room_id)  # Replace with your DB call
        self.cts_number_line.setText(cts_number)

    def get_houses_data(self):
        return [{'name': 'House A', 'id': 1}, {'name': 'House B', 'id': 2}]

    def get_cts_number(self, room_id):
        # This should return the CTS number based on the room_id
        return 'CTS1234'

    def get_data(self):
        data = {
            "house_number": self.house_number_combo.currentText(),
            "room_number": self.room_number_combo.currentText(),
            "cts_number": self.cts_number_line.text(),
            "tenant_name": self.tenant_name_line.text(),
            "bill_month": self.bill_month_date.date().toString('MMMM, yyyy'),
            "book_number": self.book_number_spin.value(),
            "bill_number": self.bill_number_spin.value(),
            "purpose": self.purpose_line.text(),
            "rent_from": self.rent_from_date.date().toString('MMMM, yyyy'),
            "rent_to": self.rent_to_date.date().toString('MMMM, yyyy'),
            "amount": self.amount_spin.value(),
            "total_months": self.total_months_spin.value(),
            "total_rupees": self.total_rupees_line.text(),
            "received_date": self.received_date.date().toString('MMMM, yyyy'),
            "extra_payment": self.extra_payment_spin.value(),
            "agreement_date": self.agreement_date.date().toString('MMMM, yyyy'),
            "notes": self.notes_text.toPlainText(),
        }
        print(data)
        return data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BillEntry()
    window.show()
    sys.exit(app.exec_())
