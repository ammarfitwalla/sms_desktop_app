import sys
import master_entry
from database import *
from base_class import BaseWindow
from PyQt5.QtCore import QDate, Qt
from datetime import datetime, date
from PyQt5.QtGui import QPainter, QImage, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QComboBox, QLineEdit, QDateEdit, QTextEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QTableWidget, QHBoxLayout, QMessageBox, QHeaderView, QTableWidgetItem, QAction, QWidget, \
    QMenuBar, QToolBar


class BillEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.set_default_state()
        self.init_ui()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

    def set_default_state(self):
        self.bill_id = None
        self.current_row = None
        self.operation = "insert"
        self.setWindowTitle("Bill Entry - Add")
        self.room_change = True

    def switch_to_master(self):
        self.close()
        self.master_page = master_entry.MasterEntry()
        self.master_page.show()
        print("Switching to Master")

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Create a toolbar
        toolbar = QToolBar("Main Toolbar")
        # Add 'Switch to Master' action
        switch_to_master_action = QAction('Go to Master Entry', self)
        switch_to_master_action.triggered.connect(self.switch_to_master)
        toolbar.addAction(switch_to_master_action)
        # Add the toolbar to the main layout
        main_layout.addWidget(toolbar)

        # Create a grid layout for the rest of the UI components
        layout = QGridLayout()
        main_layout.addLayout(layout)  # Add the grid layout to the main layout

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

        self.room_number_label = QLabel('Room Number')
        self.room_number_combo = QComboBox()

        self.cts_number_line = QLineEdit()
        self.cts_number_line.setReadOnly(True)
        self.cts_number_label = QLabel('CTS Number')

        self.tenant_name_combo = QComboBox()
        self.tenant_name_label = QLabel('Tenant Name')

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
        layout.addWidget(self.tenant_name_label, 2, 0)
        layout.addWidget(self.tenant_name_combo, 2, 1)

        # Row 4
        self.purpose_label = QLabel('Purpose For')
        self.purpose_line = QLineEdit()
        # self.purpose_line.setText('For Residence')
        layout.addWidget(self.purpose_label, 3, 0)
        layout.addWidget(self.purpose_line, 3, 1)

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
        layout.addWidget(self.rent_from_label, 3, 2)
        layout.addWidget(self.rent_from_date, 3, 3)
        layout.addWidget(self.rent_to_label, 3, 4)
        layout.addWidget(self.rent_to_date, 3, 5)

        self.rent_month_date.dateChanged.connect(self.update_rent_to_date)
        self.rent_from_date.dateChanged.connect(self.update_total_months)
        self.rent_to_date.dateChanged.connect(self.update_total_months)

        # Row 6
        self.amount_label = QLabel('@')
        self.amount_line = QLineEdit()
        # self.amount_line.setText('350')
        self.amount_line.textChanged.connect(self.update_total_rupees)
        layout.addWidget(self.amount_label, 4, 0)
        layout.addWidget(self.amount_line, 4, 1)

        # Row 7
        self.total_months_label = QLabel('Total Months')
        self.total_months_line = QLineEdit()
        self.total_months_line.setReadOnly(True)
        self.total_months_line.textChanged.connect(self.update_total_rupees)  # Connect to slot method
        layout.addWidget(self.total_months_label, 4, 2)
        layout.addWidget(self.total_months_line, 4, 3)

        # Row 8
        self.total_rupees_label = QLabel('Total Rupees')
        self.total_rupees_line = QLineEdit()
        self.total_rupees_line.setReadOnly(True)
        self.total_rupees_line.setText('0')
        layout.addWidget(self.total_rupees_label, 4, 4)
        layout.addWidget(self.total_rupees_line, 4, 5)

        # Row 9
        self.received_date_label = QLabel('Received Date')
        self.received_date = QDateEdit()
        self.received_date.setDate(QDate.currentDate())
        layout.addWidget(self.received_date_label, 5, 0)
        layout.addWidget(self.received_date, 5, 1)

        # Row 10
        self.extra_payment_label = QLabel('Extra Payment')
        self.extra_payment_line = QLineEdit()
        layout.addWidget(self.extra_payment_label, 5, 2)
        layout.addWidget(self.extra_payment_line, 5, 3)

        # Row 11
        self.agreement_date_label = QLabel('Agreement Date')
        self.agreement_date = QDateEdit()
        self.agreement_date.setDate(QDate.currentDate())
        layout.addWidget(self.agreement_date_label, 5, 4)
        layout.addWidget(self.agreement_date, 5, 5)

        self.notes_label = QLabel('Notes')
        self.notes_text = QLineEdit()

        # Add the QVBoxLayout to the main QGridLayout
        layout.addWidget(self.notes_label, 6, 0, 1, 5)
        layout.addWidget(self.notes_text, 6, 1, 1, 5)

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
        self.print_button.clicked.connect(self.print_data)  # You need to define the print_data method
        buttons_layout.addWidget(self.print_button)
        self.print_button.setDisabled(True)

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
                                   "Mobile", "DoD", "Agreement\nDate", "Gender", "Edit", "Print", "Delete"]

        self.bill_entry_table.setColumnCount(len(self.bill_table_columns))
        self.bill_entry_table.setHorizontalHeaderLabels(self.bill_table_columns)
        layout.addWidget(self.bill_entry_table, 9, 0, 1, 6)
        self.bill_entry_table.resizeColumnsToContents()

        # Ensure that the table does not stretch beyond the minimum required width
        self.bill_entry_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        # Optionally, if you want the table to resize automatically when the contents change:
        self.bill_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bill_entry_table.setShowGrid(True)  # Enable the display of grid lines between cells

        # Use setStyleSheet to define the grid line color and style
        self.bill_entry_table.setStyleSheet("gridline-color: rgb(192, 192, 192);")  # Light grey grid lines

        # You can also set border styles for the headers if desired
        self.bill_entry_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")
        self.bill_entry_table.verticalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")

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
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 3, btn_edit)

        # Print button
        btn_print = QPushButton('Print')
        btn_print.clicked.connect(lambda: self.print_record(row))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 2, btn_print)

        # Delete button
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.delete_record(row))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 1, btn_delete)

    def print_record(self, row):
        data = self.get_data_from_row(row)
        self.set_data_to_form(data)
        self.make_form_readonly()
        self.cts_number_line.setDisabled(True)
        self.operation = 'print'
        self.setWindowTitle("Bill Entry - Print")
        self.print_button.setEnabled(True)

    def make_form_readonly(self):
        # Iterate over all the form fields to set them to read-only
        for field in [self.received_date, self.rent_month_date, self.rent_from_date, self.rent_to_date,
                      self.amount_line, self.total_months_line, self.total_rupees_line,
                      self.book_number_line, self.bill_number_line, self.extra_payment_line,
                      self.purpose_line, self.agreement_date, self.house_number_combo,
                      self.room_number_combo, self.cts_number_line, self.notes_text]:
            if isinstance(field, QComboBox):
                field.setEnabled(False)
            else:
                field.setReadOnly(True)

    def make_form_editable(self):
        # Iterate over all the form fields to set them to editable
        for field in [self.received_date, self.rent_month_date, self.rent_from_date, self.rent_to_date,
                      self.amount_line, self.total_months_line, self.total_rupees_line,
                      self.book_number_line, self.bill_number_line, self.extra_payment_line,
                      self.purpose_line, self.agreement_date, self.house_number_combo,
                      self.room_number_combo, self.cts_number_line, self.notes_text]:
            if isinstance(field, QComboBox):
                field.setEnabled(True)
            elif isinstance(field, QDateEdit):
                field.setReadOnly(False)
            else:
                field.setReadOnly(False)
                field.setDisabled(False)

    def get_data_from_row(self, row):
        # Define column indices
        columns = {'RECEIVED_DATE': 0, 'HOUSE_NO': 1, 'ROOM_NO': 2, 'CTS_NO': 3, 'RENT_FROM': 5, 'RENT_TO': 6,
                   'RATE': 7, 'TOTAL_MONTHS': 8, 'TOTAL_AMOUNT': 9, 'BOOK_NO': 10, 'BILL_NO': 11, 'EXTRA_PAYMENT': 12,
                   'PURPOSE_FOR': 13, 'AGREEMENT_DATE': 16, 'BILL_ID': 0}

        # Fetch the data from the table row
        data = {
            key: self.bill_entry_table.item(row, col).text() if self.bill_entry_table.item(row, col) is not None else ""
            for key, col in columns.items()}

        # Fetch the bill_id
        data['BILL_ID'] = self.bill_entry_table.item(row, columns['BILL_ID']).data(
            Qt.UserRole) if self.bill_entry_table.item(row, columns['BILL_ID']) else None

        return data

    def set_data_to_form(self, data):
        # Fill the form fields with the data
        self.received_date.setDate(QDate.fromString(data['RECEIVED_DATE'], 'yyyy-MM-dd'))
        self.rent_from_date.setDate(QDate.fromString(data['RENT_FROM'], 'MMM-yyyy'))
        self.rent_to_date.setDate(QDate.fromString(data['RENT_TO'], 'MMM-yyyy'))
        self.amount_line.setText(data['RATE'])
        self.total_months_line.setText(data['TOTAL_MONTHS'])
        self.total_rupees_line.setText(data['TOTAL_AMOUNT'])
        self.book_number_line.setText(data['BOOK_NO'])
        self.bill_number_line.setText(data['BILL_NO'])
        self.extra_payment_line.setText(data['EXTRA_PAYMENT'])
        self.purpose_line.setText(data['PURPOSE_FOR'])
        self.agreement_date.setDate(QDate.fromString(data['AGREEMENT_DATE'], 'yyyy-MM-dd'))

        # Set comboboxes and line edits
        house_index = self.house_number_combo.findText(data['HOUSE_NO'])
        room_index = self.room_number_combo.findText(data['ROOM_NO'])
        self.house_number_combo.setCurrentIndex(house_index)
        self.room_number_combo.setCurrentIndex(room_index)
        self.cts_number_line.setText(data['CTS_NO'])

        # If additional data was fetched from the database
        if data['BILL_ID']:
            self.bill_id = data['BILL_ID']
            rent_month_date, notes = fetch_data_for_edit_record(data['BILL_ID'])
            if rent_month_date:
                self.rent_month_date.setDate(QDate.fromString(rent_month_date, 'MMM-yyyy'))
            if notes:
                self.notes_text.setText(notes)

    def edit_record(self, row):
        if self.operation == 'print':
            self.make_form_editable()
            self.print_button.setDisabled(True)
        data = self.get_data_from_row(row)
        self.set_data_to_form(data)
        self.house_number_combo.setDisabled(True)
        self.room_number_combo.setDisabled(True)
        self.cts_number_line.setDisabled(True)

        self.operation = 'update'
        self.setWindowTitle("Bill Entry - Edit")

    def delete_record(self, row):
        bill_id_item = self.bill_entry_table.item(row, 0)
        bill_id = bill_id_item.data(Qt.UserRole) if bill_id_item else None

        if bill_id is None:
            QMessageBox.warning(self, "Error", "Could not find the bill ID for row.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this bill?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success, message = delete_bill_by_id(bill_id)
            if success:
                QMessageBox.information(self, "Success", "Successfully deleted the record.")
                self.populate_table()
            else:
                QMessageBox.warning(self, "Error", f"Error deleting the record: {message}")
        else:
            print("Deletion cancelled.")

    def clear_form(self):
        self.make_form_editable()
        self.print_button.setDisabled(True)
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
        try:
            print("house started")
            current_house_id = self.house_number_combo.currentData()
            self.room_number_combo.clear()
            self.tenant_name_combo.clear()
            if current_house_id:
                rooms = get_rooms_data_by_house_id(current_house_id)
                for room in rooms:
                    room_name, room_id = room
                    self.room_number_combo.addItem(room_name, room_id)
                # Update room and tenant based on the first room if available
                if rooms:
                    self.room_number_combo.setCurrentIndex(0)
                    self.room_changed()
            print("house changed")
        except Exception as e:
            print(str(e))

    def room_changed(self):
        try:
            print('room started')
            current_room_id = self.room_number_combo.currentData()
            self.tenant_name_combo.clear()  # Clear tenants before adding new ones
            if current_room_id:
                cts_number = get_cts_number_by_room_id(current_room_id)
                self.cts_number_line.setText(cts_number)

                # Get tenants associated with the room and add to the tenant_name_combo
                tenants_data = get_tenants_data_by_room_id(current_room_id)
                print(tenants_data)
                added_tenant_idx = []
                for data in tenants_data:
                    tenant_name, tenant_id = data
                    self.tenant_name_combo.addItem(tenant_name, tenant_id)
                    added_tenant_idx.append(tenant_id)

                current_house_id = self.house_number_combo.currentData()
                print(current_house_id)
                rooms = get_rooms_data_by_house_id(current_house_id)
                for room in rooms:
                    room_name, room_id = room
                    tenants_data = get_tenants_data_by_room_id(room_id)
                    for data in tenants_data:
                        tenant_name, tenant_id = data
                        if tenant_id not in added_tenant_idx:
                            self.tenant_name_combo.addItem(tenant_name, tenant_id)
            else:
                self.cts_number_line.clear()
            print('room changed')
        except Exception as e:
            print(str(e))

    def tenant_changed(self):
        # self.room_number_combo.currentIndexChanged.disconnect(self.room_changed)
        if not self.room_change:
            current_tenant_id = self.tenant_name_combo.currentData()
            self.room_number_combo.clear()  # Clear rooms before adding new ones
            if current_tenant_id:
                # Get rooms associated with the tenant and add to the room_number_combo
                room_numbers = get_rooms_data_by_tenant_id(current_tenant_id)
                added_room_idx = []
                for room_number, room_id in room_numbers:
                    self.room_number_combo.addItem(room_number, room_id)
                    added_room_idx.append(room_id)

                # Automatically select the first room for the tenant if available
                if room_numbers:
                    cts_number = get_cts_number_by_room_id(room_numbers[0])  # Pass the first room_id
                    self.cts_number_line.setText(cts_number)

                current_house_id = self.house_number_combo.currentData()
                rooms = get_rooms_data_by_house_id(current_house_id)
                for room in rooms:
                    room_name, room_id = room
                    if room_id not in added_room_idx:
                        self.room_number_combo.addItem(room_name, room_id)
            else:
                self.cts_number_line.clear()
        else:
            print("in else")
            # current_room_id = self.room_number_combo.currentData()
            # self.tenant_name_combo.clear()  # Clear tenants before adding new ones
            # if current_room_id:
            #     # Get tenants associated with the room and add to the tenant_name_combo
            #     tenants_data = get_tenants_data_by_room_id(current_room_id)
            #     added_tenant_idx = []
            #     print(self.tenant_name_combo.currentData())
            #     for data in tenants_data:
            #         tenant_name, tenant_id = data
            #         self.tenant_name_combo.addItem(tenant_name, tenant_id)
            #         added_tenant_idx.append(tenant_id)
            #     current_house_id = self.house_number_combo.currentData()
            #     rooms = get_rooms_data_by_house_id(current_house_id)
            #     print(rooms)
            #     for room in rooms:
            #         room_name, room_id = room
            #         tenants_data = get_tenants_data_by_room_id(room_id)
            #         for data in tenants_data:
            #             tenant_name, tenant_id = data
            #             if tenant_id not in added_tenant_idx:
            #                 self.tenant_name_combo.addItem(tenant_name, tenant_id)
            # self.room_change = False

        # Reconnect the signal after the updates are done
        # self.room_number_combo.currentIndexChanged.connect(self.room_changed)

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

    def print_data(self):
        tenant_name = get_tenant_name_by_bill_id(self.bill_id)
        received_date_with_ordinal, received_month, received_year = get_date_month_year(
            self.received_date.date().toString("yyyy-MM-dd"))
        agreement_date_with_ordinal, agreement_month, agreement_year = get_date_month_year(
            self.agreement_date.date().toString("yyyy-MM-dd"))
        rent_from = convert_date_string(self.rent_from_date.date().toString("MMM-yyyy"))
        rent_to = convert_date_string(self.rent_to_date.date().toString("MMM-yyyy"))
        rent_from_to = rent_from + "   to   " + rent_to

        data = {"rent_month": self.rent_month_date.date().toString("MMM-yyyy"),
                "book_number": self.book_number_line.text(),
                "bill_number": self.bill_number_line.text(),
                "purpose_for": self.purpose_line.text(),
                "cts_number": self.cts_number_line.text(),
                "house_number": self.house_number_combo.currentText(),
                "room_number": self.room_number_combo.currentText(),
                "tenant_name": tenant_name,
                "rent_from_to": rent_from_to,
                "total_rupees": self.total_rupees_line.text(),
                "total_paise": "00.",
                "@": "@",
                "per_month": "per month",
                "at_the_rate_of": "Rs. " + self.amount_line.text() + "/-",
                "received_date_with_ordinal": received_date_with_ordinal,
                "received_month": received_month,
                "received_year": received_year,
                "agreement_date_with_ordinal": agreement_date_with_ordinal,
                "agreement_month": agreement_month,
                "agreement_year": agreement_year,
                "notes": self.notes_text.text()
                }

        bill_image_path = r'images/output_bill_blank_image.png'  # Replace with your image path
        bill_image = QImage(bill_image_path)

        # Draw text onto the image
        painter = QPainter(bill_image)
        painter.begin(bill_image)
        painter.setFont(QFont('Arial', 33))  # Choose a suitable font and size

        # Define positions for the text fields on the image (these will need to be adjusted)
        positions = {
            "rent_month": (600, 830),
            "book_number": (1135, 830),
            "bill_number": (1483, 830),
            "purpose_for": (235, 940),
            "cts_number": (1135, 940),
            "room_number": (600, 1055),
            "house_number": (1135, 1055),
            "tenant_name": (378, 1355),
            "rent_from_to": (747, 1465),
            "total_rupees": (1127, 1625),
            "total_paise": (1483, 1625),
            "@": (730, 1540),
            "at_the_rate_of": (665, 1595),
            "per_month": (665, 1640),
            "received_date_with_ordinal": (993, 1850),
            "received_month": (1260, 1850),
            "received_year": (1493, 1850),
            "agreement_date_with_ordinal": (490, 2160),
            "agreement_month": (697, 2160),
            "agreement_year": (956, 2160),
            "notes": (390, 2470)}

        for key, value in data.items():
            x, y = positions[key]
            painter.drawText(x, y, value)
            print(x, y, key)
            print('text drawn')

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.PageSize.A5)
        printer.setColorMode(QPrinter.Color)
        printer.setFullPage(False)
        printer.setOutputFormat(QPrinter.NativeFormat)

        # Assuming the printer is already set up correctly, start painting directly
        painter = QPainter()
        if painter.begin(printer):
            rect = painter.viewport()
            size = bill_image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(bill_image.rect())
            painter.drawImage(0, 0, bill_image)
            painter.end()
        else:
            print("Failed to start painting on printer.")

        print(f"Printer name: {printer.printerName()}")
        print(f"Page size: {printer.pageSize()}")
        print(f"Page rect: {printer.pageRect()}")
        print(f"Resolution: {printer.resolution()} DPI")
        print(f"Color mode: {'Color' if printer.colorMode() == QPrinter.Color else 'Grayscale'}")
        print(f"Is full page: {printer.fullPage()}")
        print(f"Output format: {printer.outputFormat()}")

        # Print the image
        # printer = QPrinter(QPrinter.HighResolution)
        # printer.setPageSize(QPrinter.A5)
        # printer.setColorMode(QPrinter.Color)
        # printer.setFullPage(True)
        #
        # print_dialog = QPrintDialog(printer)
        # if print_dialog.exec_() == QPrintDialog.Accepted:
        #     painter = QPainter(printer)
        #     painter.begin(printer)
        #     rect = painter.viewport()
        #     size = bill_image.size()
        #     size.scale(rect.size(), Qt.KeepAspectRatio)
        #     painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        #     painter.setWindow(bill_image.rect())
        #     painter.drawImage(0, 0, bill_image)
        #     painter.end()


def get_date_month_year(user_date):
    date_obj = datetime.strptime(user_date, "%Y-%m-%d")
    day = int(date_obj.strftime("%d"))  # Convert day to an integer to remove leading zeros
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    day_ordinal = str(day) + suffix
    return day_ordinal, date_obj.strftime("%B"), date_obj.strftime("%Y")


def convert_date_string(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%b-%Y")
        formatted_date = date_obj.strftime("%B %Y")
        return formatted_date
    except ValueError:
        return None  # Handle invalid date strings gracefully


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BillEntry()
    window.show()
    sys.exit(app.exec_())
