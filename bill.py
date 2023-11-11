import sys
from datetime import datetime
from datetime import date
from database import *
from base_class import BaseWindow
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QComboBox, QLineEdit, QDateEdit, QTextEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QTableWidget, QHBoxLayout, QMessageBox, QHeaderView, QTableWidgetItem


class BillEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_default_state()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

    def set_default_state(self):
        self.operation = "insert"
        self.current_row = None
        self.setWindowTitle("Bill Entry - Add")
        self.bill_id = None

    def init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # Row 2
        self.rent_month_label = QLabel('Bill For Month Of')
        self.rent_month_date = QDateEdit()
        self.rent_month_date.setDisplayFormat('MMM-yyyy')
        self.rent_month_date.setDate(QDate.currentDate())
        layout.addWidget(self.rent_month_label, 0, 0)
        layout.addWidget(self.rent_month_date, 0, 1)  # Spanning across two columns for space

        # Row 3
        self.book_number_label = QLabel('Book Number')
        self.book_number_line = QLineEdit()
        self.bill_number_label = QLabel('Bill Number')
        self.bill_number_line = QLineEdit()
        # next_book_number, next_bill_number = self.calculate_next_numbers()
        # self.book_number_line.setText(str(next_book_number))
        # self.bill_number_line.setText(str(next_bill_number))
        layout.addWidget(self.book_number_label, 0, 2)
        layout.addWidget(self.book_number_line, 0, 3)
        layout.addWidget(self.bill_number_label, 0, 4)
        layout.addWidget(self.bill_number_line, 0, 5)

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
        layout.addWidget(self.house_number_label, 1, 0)
        layout.addWidget(self.house_number_combo, 1, 1)
        layout.addWidget(self.room_number_label, 1, 2)
        layout.addWidget(self.room_number_combo, 1, 3)
        layout.addWidget(self.cts_number_label, 1, 4)
        layout.addWidget(self.cts_number_line, 1, 5)

        # Row 4
        self.purpose_label = QLabel('Purpose For')
        self.purpose_line = QLineEdit()
        # self.purpose_line.setText('For Residence')
        layout.addWidget(self.purpose_label, 2, 0)
        layout.addWidget(self.purpose_line, 2, 1)

        # Row 5
        self.rent_from_label = QLabel('Rent From')
        self.rent_from_date = QDateEdit()
        self.rent_from_date.setDisplayFormat('MMM-yyyy')
        self.rent_from_date.setDate(QDate.currentDate())
        self.rent_to_label = QLabel('Rent To')
        self.rent_to_date = QDateEdit()
        self.rent_to_date.setDisplayFormat('MMM-yyyy')
        self.rent_to_date.setDate(QDate.currentDate())
        self.rent_to_date.setReadOnly(True)
        layout.addWidget(self.rent_from_label, 2, 2)
        layout.addWidget(self.rent_from_date, 2, 3)
        layout.addWidget(self.rent_to_label, 2, 4)
        layout.addWidget(self.rent_to_date, 2, 5)

        self.rent_month_date.dateChanged.connect(self.update_rent_to_date)
        self.rent_from_date.dateChanged.connect(self.update_total_months)
        self.rent_to_date.dateChanged.connect(self.update_total_months)

        # Row 6
        self.amount_label = QLabel('@')
        self.amount_line = QLineEdit()
        # self.amount_line.setText('350')
        self.amount_line.textChanged.connect(self.update_total_rupees)
        layout.addWidget(self.amount_label, 3, 0)
        layout.addWidget(self.amount_line, 3, 1)

        # Row 7
        self.total_months_label = QLabel('Total Months')
        self.total_months_line = QLineEdit()
        self.total_months_line.setReadOnly(True)
        self.total_months_line.textChanged.connect(self.update_total_rupees)  # Connect to slot method
        layout.addWidget(self.total_months_label, 3, 2)
        layout.addWidget(self.total_months_line, 3, 3)

        # Row 8
        self.total_rupees_label = QLabel('Total Rupees')
        self.total_rupees_line = QLineEdit()
        self.total_rupees_line.setReadOnly(True)
        self.total_rupees_line.setText('0')
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
        self.notes_text = QLineEdit()

        # Add the QVBoxLayout to the main QGridLayout
        layout.addWidget(self.notes_label, 5, 0, 1, 5)
        layout.addWidget(self.notes_text, 5, 1, 1, 5)

        buttons_layout = QHBoxLayout()

        # Create Submit Button
        self.submit_button = QPushButton('Save')
        self.submit_button.clicked.connect(self.submit_data)
        buttons_layout.addWidget(self.submit_button)

        # Create Clear Button
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_button)

        # Create Print Button
        self.print_button = QPushButton('Print')
        # self.print_button.clicked.connect(self.print_data)  # You need to define the print_data method
        buttons_layout.addWidget(self.print_button)

        layout.addLayout(buttons_layout, 7, 1, 1, 5)  # Assuming row 7 is where you want the buttons

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        search_label = QLabel("Search")
        layout.addWidget(search_label, 8, 0)
        layout.addWidget(self.search_bar, 8, 1, 1, -1)

        # Connect the search bar's textChanged signal to the filter_table method
        self.search_bar.textChanged.connect(self.filter_table)

        self.bill_entry_table = QTableWidget(self)
        self.bill_table_columns = ["Received\nDate", "House\nNo.", "Room\nNo.", "CTS\nNo.", "Name",
                                   "Rent\nFrom", "Rent\nTo", "@", "Total\nMonth(s)", "Total\nAmount",
                                   "Book\nNo.", "Bill\nNo.", "Extra\nPayment", "Purpose\nFor",
                                   "Mobile", "DoD", "Agreement\nDate", "Gender", "Edit", "Delete"]
        self.bill_entry_table.setColumnCount(len(self.bill_table_columns))
        self.bill_entry_table.setHorizontalHeaderLabels(self.bill_table_columns)
        layout.addWidget(self.bill_entry_table, 9, 0, 1, 6)
        self.bill_entry_table.resizeColumnsToContents()

        # Ensure that the table does not stretch beyond the minimum required width
        self.bill_entry_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        # Optionally, if you want the table to resize automatically when the contents change:
        self.bill_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.populate_table()

    def filter_table(self):
        search_term = self.search_bar.text().lower()
        self.populate_table(search_term)

    def populate_table(self, search_term=''):
        bill_entries = get_bill_table_data()

        # Filter the entries based on the search term
        if search_term:
            bill_entries = [
                entry for entry in bill_entries if
                search_term in (entry.get("Tenant Name", '') or '').lower() or
                search_term in (entry.get("House No.", '') or '').lower() or
                search_term in (entry.get("Room No.", '') or '').lower()
            ]

        # Clear the table before populating
        self.bill_entry_table.setRowCount(0)

        if bill_entries:
            # Get the column names from the keys of the first dictionary in the list
            column_names = list(bill_entries[0].keys())

            # Populate the table with rows
            for row_number, row_data in enumerate(bill_entries):
                self.bill_entry_table.insertRow(row_number)
                tenant_id = row_data["Bill ID"]
                for column_number, column_name in enumerate(column_names):
                    if column_name == "Bill ID":
                        continue
                    # Check for None and convert datetime.date to string
                    data = row_data.get(column_name, '')
                    if isinstance(data, date):
                        data = data.strftime('%Y-%m-%d')
                    elif data is None:
                        data = ''

                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.bill_entry_table.setItem(row_number, column_number, item)

                self.bill_entry_table.item(row_number, 0).setData(Qt.UserRole, tenant_id)
                # Add 'Edit' and 'Delete' buttons
                self.add_table_buttons(row_number)

    def add_table_buttons(self, row):
        btn_edit = QPushButton('Edit')
        btn_edit.clicked.connect(lambda: self.edit_record(row))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 2, btn_edit)

        # Delete button
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.delete_record(row))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 1, btn_delete)

    def edit_record(self, row):
        # Assuming the column indices are set as follows, adjust if your table is different
        RECEIVED_DATE_COL = 0
        HOUSE_NO_COL = 1
        ROOM_NO_COL = 2
        CTS_NO_COL = 3
        RENT_FROM_COL = 5
        RENT_TO_COL = 6
        RATE_COL = 7
        TOTAL_MONTHS_COL = 8
        TOTAL_AMOUNT_COL = 9
        BOOK_NO_COL = 10
        BILL_NO_COL = 11
        EXTRA_PAYMENT_COL = 12
        PURPOSE_FOR_COL = 13
        AGREEMENT_DATE_COL = 16

        # Fetch the data from the table row
        received_date_item = self.bill_entry_table.item(row, RECEIVED_DATE_COL)
        received_date = received_date_item.text() if received_date_item is not None else ""
        house_no = self.bill_entry_table.item(row, HOUSE_NO_COL).text()
        room_no = self.bill_entry_table.item(row, ROOM_NO_COL).text()
        cts_no = self.bill_entry_table.item(row, CTS_NO_COL).text()
        rent_from = self.bill_entry_table.item(row, RENT_FROM_COL).text()
        rent_to = self.bill_entry_table.item(row, RENT_TO_COL).text()
        rate = self.bill_entry_table.item(row, RATE_COL).text()
        total_months = self.bill_entry_table.item(row, TOTAL_MONTHS_COL).text()
        total_amount = self.bill_entry_table.item(row, TOTAL_AMOUNT_COL).text()
        book_no = self.bill_entry_table.item(row, BOOK_NO_COL).text()
        bill_no = self.bill_entry_table.item(row, BILL_NO_COL).text()
        extra_payment = self.bill_entry_table.item(row, EXTRA_PAYMENT_COL).text()
        purpose_for = self.bill_entry_table.item(row, PURPOSE_FOR_COL).text()
        agreement_date = self.bill_entry_table.item(row, AGREEMENT_DATE_COL).text()

        bill_id_item = self.bill_entry_table.item(row, 0)  # Assuming bill_id is stored in the first column
        self.bill_id = bill_id_item.data(Qt.UserRole) if bill_id_item else None

        if self.bill_id:
            rent_month_date, notes = fetch_data_for_edit_record(self.bill_id)
            if rent_month_date:
                self.rent_month_date.setDate(QDate.fromString(rent_month_date, 'MMM-yyyy'))
            if notes:
                self.notes_text.setText(notes)

        # Fill the form fields with the data
        self.received_date.setDate(QDate.fromString(received_date, 'yyyy-MM-dd'))
        self.rent_from_date.setDate(QDate.fromString(rent_from, 'MMM-yyyy'))
        self.rent_to_date.setDate(QDate.fromString(rent_to, 'MMM-yyyy'))
        self.amount_line.setText(rate)
        self.total_months_line.setText(total_months)
        self.total_rupees_line.setText(total_amount)
        self.book_number_line.setText(book_no)
        self.bill_number_line.setText(bill_no)
        self.extra_payment_line.setText(extra_payment)
        self.purpose_line.setText(purpose_for)
        self.agreement_date.setDate(QDate.fromString(agreement_date, 'yyyy-MM-dd'))

        # Disable the comboboxes and CTS number line edit as they should not be editable
        self.house_number_combo.setDisabled(True)
        self.room_number_combo.setDisabled(True)
        self.cts_number_line.setDisabled(True)

        # Now find and set the indexes of the combo boxes, you would have the logic to find the index based on the value
        # This is placeholder logic
        house_index = self.house_number_combo.findText(house_no)
        room_index = self.room_number_combo.findText(room_no)

        self.house_number_combo.setCurrentIndex(house_index)
        self.room_number_combo.setCurrentIndex(room_index)
        self.cts_number_line.setText(cts_no)

        self.operation = 'update'
        self.setWindowTitle("Bill Entry - Edit")

    def delete_record(self, row):
        # Placeholder for the logic to delete a record
        print(f"Delete record at row {row}")

    def clear_form(self):
        # Reset combo boxes to the first index
        self.house_number_combo.setEnabled(True)
        self.room_number_combo.setEnabled(True)
        self.cts_number_line.setEnabled(True)
        self.house_number_combo.setCurrentIndex(0)
        self.room_number_combo.setCurrentIndex(0)

        # Clear line edits
        self.book_number_line.clear()
        self.bill_number_line.clear()
        self.purpose_line.clear()
        self.amount_line.clear()
        self.total_rupees_line.clear()
        self.extra_payment_line.clear()
        self.notes_text.clear()

        # Reset the dates to current date
        current_date = QDate.currentDate()
        self.rent_month_date.setDate(current_date)
        self.rent_from_date.setDate(current_date)
        self.received_date.setDate(current_date)
        self.agreement_date.setDate(current_date)

        # Update fields
        self.room_changed()
        self.update_rent_to_date()
        self.update_total_months()
        self.update_total_rupees()
        self.operation = 'insert'
        self.bill_id = None
        self.setWindowTitle("Bill Entry - Add")


    def calculate_next_numbers(self):
        # Get the latest numbers from the database
        latest_book_number, latest_bill_number = get_latest_book_and_bill_numbers()

        # Logic to determine the next book and bill number
        if latest_bill_number == 100:
            # If the bill number has reached 100, increment the book number and reset bill number to 1
            next_book_number = latest_book_number + 1
            next_bill_number = 1
        else:
            # Otherwise, just increment the bill number
            next_book_number = latest_book_number
            next_bill_number = latest_bill_number + 1

        return next_book_number, next_bill_number

    def update_rent_to_date(self):
        rent_month_date = self.rent_month_date.date()
        self.rent_to_date.setDate(rent_month_date)

    def update_total_months(self):
        rent_from_date = self.rent_from_date.date()
        rent_to_date = self.rent_to_date.date()

        # Calculate the difference in months
        month_diff = ((rent_to_date.year() - rent_from_date.year()) * 12 +
                      rent_to_date.month() - rent_from_date.month() + 1)
        total_months = max(0, month_diff)

        # Update the total_months_line QLineEdit
        self.total_months_line.setText(str(total_months))
        return total_months

    def update_total_rupees(self):
        # Get the values from the amount and total months QLineEdit widgets
        amount_text = self.amount_line.text()
        total_months_text = self.total_months_line.text()

        try:
            # Convert the text to float values
            amount = float(amount_text)
            total_months = float(total_months_text)

            # Calculate the product
            total_rupees = amount * total_months

            # Update the total_rupees_line QLineEdit with the calculated value
            self.total_rupees_line.setText(str(total_rupees))
        except ValueError:
            # Handle the case where the input is not a valid float
            self.total_rupees_line.setText('0')

    def populate_houses_dropdown(self):
        houses = get_house_data()  # Replace with your DB call
        for house in houses:
            house_number, house_id = house[0], house[1]
            self.house_number_combo.addItem(house_number, house_id)

    def house_changed(self):
        current_house_id = self.house_number_combo.currentData()
        rooms = get_rooms_data_by_house_id(current_house_id)
        self.room_number_combo.clear()
        for room in rooms:
            room_name, room_id = room[0], room[1]
            self.room_number_combo.addItem(room_name, room_id)

    def room_changed(self):
        current_room_id = self.room_number_combo.currentData()
        if current_room_id:
            cts_number = get_cts_number_by_room_id(current_room_id)
            self.cts_number_line.setText(cts_number)
        else:
            self.cts_number_line.clear()

    def submit_data(self):
        mandatory_fields = [
            (self.book_number_line, "Book Number"),
            (self.bill_number_line, "Bill Number"),
            (self.house_number_combo, "House Number"),
            (self.room_number_combo, "Room Number"),
            (self.purpose_line, "Purpose For"),
            (self.amount_line, "@"),
        ]

        print("validating mandatory field")
        for field, field_name in mandatory_fields:
            if isinstance(field, QComboBox):
                if not field.currentText().strip():
                    QMessageBox.warning(self, "Missing Data", f"Please select a {field_name}.")
                    return
            elif not field.text().strip():  # Assuming QLineEdit or similar widgets for other fields
                QMessageBox.warning(self, "Missing Data", f"Please enter the {field_name}.")
                return

        print("validating @")
        if not self.validate_at_the_rate_of():
            QMessageBox.warning(self, "Wrong Data", "'@' should be a Positive Number only")
            return

        print("validating Total months")
        if not self.validate_total_months():
            QMessageBox.warning(self, "Wrong Data", "'Rent From' should be greater than 'Rent To' Date.")
            return

        print("validating rent from rent to")
        if not self.validate_rent_from_to_date():
            QMessageBox.warning(self, "Wrong Data", "'Rent From' Date already exists in Previous Bill.")
            return

        print("getting user data")
        total_months = self.total_months_line.text()
        house_number = self.house_number_combo.currentText()
        room_number = self.room_number_combo.currentText()
        cts_number = self.cts_number_line.text()
        rent_from = self.rent_from_date.date().toString("MMM-yyyy")
        rent_to = self.rent_to_date.date().toString("MMM-yyyy")
        rent_month = self.rent_month_date.date().toString("MMM-yyyy")
        book_number = self.book_number_line.text()
        bill_number = self.bill_number_line.text()
        purpose_for = self.purpose_line.text()
        at_the_rate_of = self.amount_line.text()
        total_rupees = self.total_rupees_line.text()
        received_date = self.received_date.date().toString("yyyy-MM-dd")
        extra_payment = self.extra_payment_line.text()
        agreement_date = self.agreement_date.date().toString("yyyy-MM-dd")
        notes = self.notes_text.text()

        if self.operation == "insert":
            print('before insert function')
            status, message = insert_bill_entry(rent_month, book_number, bill_number, house_number, room_number,
                                                cts_number, purpose_for, rent_from, rent_to, at_the_rate_of,
                                                total_months, total_rupees, received_date, extra_payment,
                                                agreement_date, notes)
            if status:
                QMessageBox.information(self, "Success", "Bill Data Inserted successfully!")
                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", str(message))
        else:
            status, message = update_bill_entry(self.bill_id, rent_month, book_number, bill_number, purpose_for,
                                                rent_from, rent_to, at_the_rate_of, total_months, total_rupees,
                                                received_date, extra_payment, agreement_date, notes)
            if status:
                QMessageBox.information(self, "Success", "Bill Data Updated successfully!")
                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", str(message))

        self.populate_table()
        self.setWindowTitle("Bill Entry - Add")
        # print(rent_month)
        # print(book_number)
        # print(bill_number)
        # print(house_number)
        # print(room_number)
        # print(cts_number)
        # print(rent_from)
        # print(rent_to)
        # print(at_the_rate_of)
        # print(total_months)
        # print(total_rupees)
        # print(str(received_date))
        # print(extra_payment)
        # print(str(agreement_date))
        # print(notes)

    def validate_at_the_rate_of(self):
        input_text = self.amount_line.text()

        if input_text.isdigit() and int(input_text) > 0:
            return True
        else:
            return False

    def validate_total_months(self):
        return True if int(self.total_months_line.text()) > 0 else False

    def validate_rent_from_to_date(self):
        house_number = self.house_number_combo.currentText()
        room_number = self.room_number_combo.currentText()
        cts_number = self.cts_number_line.text()
        rent_from = self.rent_from_date.date().toString("MMM-yyyy")

        previous_rent_from_date, previous_rent_to_date = get_last_from_and_to_dates(house_number, room_number,
                                                                                    cts_number, self.operation)

        if previous_rent_from_date and previous_rent_to_date:
            previous_rent_to = datetime.strptime(previous_rent_to_date, "%b-%Y")
            new_rent_from = datetime.strptime(rent_from, "%b-%Y")

            if previous_rent_to > new_rent_from:
                return False

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BillEntry()
    window.show()
    sys.exit(app.exec_())
