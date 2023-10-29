import os

from PyQt5.QtWidgets import (QWidget, QComboBox, QFormLayout, QLabel, QLineEdit,
                             QVBoxLayout, QPushButton, QRadioButton, QDateEdit,
                             QGridLayout, QCheckBox, QMessageBox, QTableWidget,
                             QTableWidgetItem, QHBoxLayout, QCompleter)
import database
from datetime import date
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate, QSize
from base_class import BaseWindow


class MasterEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_default_state()

    def set_default_state(self):
        self.operation = "insert"
        self.current_row = None
        self.setWindowTitle("Master Entry - Add")

    def init_ui(self):
        layout = QFormLayout()

        # --------------------------- HOUSE NUMBER --------------------------- #
        self.house_number_combo = self.setup_combobox(database.get_house_numbers)

        # --------------------------- CTS NUMBER --------------------------- #
        self.cts_number_combo = self.setup_combobox(database.get_cts_numbers)

        # --------------------------- ROOM NUMBER --------------------------- #
        self.room_number_combo = self.setup_combobox(database.get_room_numbers)

        # --------------------------- TENANT ATTRIBUTES --------------------------- #
        self.tenant_name_input = QLineEdit(self)
        self.tenant_mobile_input = QLineEdit(self)
        self.tenant_dod_input = QDateEdit(self)
        self.tenant_dod_input.setDisplayFormat("dd-MM-yyyy")
        self.tenant_dod_input.setDate(QDate.currentDate())
        self.is_alive_checkbox = QCheckBox("Is Alive", self)
        self.is_alive_checkbox.stateChanged.connect(self.toggle_dod_input)
        self.notes_input = QLineEdit(self)
        self.male_rb = QRadioButton("Male", self)
        self.female_rb = QRadioButton("Female", self)

        # --------------------------- SUBMIT BUTTON --------------------------- #
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(self.handle_submission)

        # --------------------------- CLEAR FORM BUTTON --------------------------- #
        self.clear_form_btn = QPushButton("Clear Form", self)
        self.clear_form_btn.clicked.connect(self.clear_form)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")

        # Adding widgets to layout
        layout.addRow(QLabel("House Number"), self.house_number_combo)
        layout.addRow(QLabel("CTS Number"), self.cts_number_combo)
        layout.addRow(QLabel("Room Number"), self.room_number_combo)
        layout.addRow(QLabel("Tenant Name"), self.tenant_name_input)
        layout.addRow(QLabel("Tenant Mobile Number"), self.tenant_mobile_input)
        layout.addRow(self.is_alive_checkbox)
        layout.addRow(QLabel("Tenant Date of Death"), self.tenant_dod_input)
        layout.addRow(QLabel("Notes"), self.notes_input)

        gender_layout = QGridLayout()
        gender_layout.addWidget(self.male_rb, 0, 0)
        gender_layout.addWidget(self.female_rb, 0, 1)
        layout.addRow(QLabel("Tenant Gender"), gender_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.clear_form_btn)
        layout.addRow(button_layout)
        layout.addRow(QLabel("Search"), self.search_bar)
        self.search_bar.textChanged.connect(self.filter_table)

        self.master_entry_table = QTableWidget(self)
        self.master_entry_table.setColumnCount(10)  # Number of columns based on the fields you have
        self.master_entry_table.setHorizontalHeaderLabels(["House No.", "Room No.", "CTS No.", "Name",
                                                           "Mobile", "DoD", "Notes", "Gender", "Edit", "Delete"])
        layout.addRow(self.master_entry_table)
        self.populate_table()

        self.setLayout(layout)

    def setup_combobox(self, data_function):
        combo = QComboBox(self)
        combo.setEditable(True)
        completer = QCompleter(self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        combo.setCompleter(completer)
        data = data_function()
        combo.addItems(data)
        combo.setCurrentIndex(-1)
        completer.setModel(combo.model())
        return combo

    def refresh_combo_box(self, combo_box, data_function):
        combo_box.clear()
        data = data_function()
        combo_box.addItems(data)
        combo_box.setCurrentIndex(-1)

    def filter_table(self):
        search_term = self.search_bar.text().lower()
        self.populate_table(search_term)

    def handle_submission(self):
        try:
            if not self.validate_input():
                return
            house_number = self.house_number_combo.currentText()
            room_number = self.room_number_combo.currentText()
            cts_number = self.cts_number_combo.currentText()
            tenant_name = self.tenant_name_input.text()
            tenant_mobile = self.tenant_mobile_input.text()
            if self.is_alive_checkbox.isChecked():
                tenant_dod = None
            else:
                tenant_dod = self.tenant_dod_input.date().toString("yyyy-MM-dd")
            notes = self.notes_input.text()
            tenant_gender = "Male" if self.male_rb.isChecked() else "Female"

            if self.operation == "insert":
                status, message = database.insert_master_entry(house_number, cts_number, room_number, tenant_name,
                                                               tenant_mobile, tenant_dod, notes, tenant_gender)
                print(status, message)
                if status:
                    QMessageBox.information(self, "Success", "Data Inserted Successfully!")
                    self.clear_form()
                    self.refresh_combo_box(self.house_number_combo, database.get_house_numbers)
                    self.refresh_combo_box(self.room_number_combo, database.get_room_numbers)
                    self.refresh_combo_box(self.cts_number_combo, database.get_cts_numbers)
                else:
                    QMessageBox.warning(self, "Error", str(message))
            else:
                status, message = database.update_master_entry(self.old_house_number, self.old_cts_number,
                                                               self.old_room_number, house_number, cts_number,
                                                               room_number, tenant_name, tenant_mobile,
                                                               tenant_dod, notes, tenant_gender)
                if status:
                    QMessageBox.information(self, "Success", "Data Updated successfully!")
                    self.clear_form()
                    self.refresh_combo_box(self.house_number_combo, database.get_house_numbers)
                    self.refresh_combo_box(self.room_number_combo, database.get_room_numbers)
                    self.refresh_combo_box(self.cts_number_combo, database.get_cts_numbers)
                else:
                    QMessageBox.warning(self, "Error", str(message))

            self.populate_table()
            self.setWindowTitle("Master Entry - Add")

        except Exception as e:
            QMessageBox.critical(self, "Error", "Data not inserted!\nError: " + str(e))

    def clear_form(self):
        self.house_number_combo.setCurrentIndex(-1)
        self.cts_number_combo.setCurrentIndex(-1)
        self.room_number_combo.setCurrentIndex(-1)
        self.tenant_name_input.clear()
        self.tenant_mobile_input.clear()
        self.tenant_dod_input.setDate(QDate.currentDate())  # Resetting to the current date
        self.notes_input.clear()
        self.male_rb.setChecked(False)
        self.female_rb.setChecked(False)
        self.operation = "insert"  # Reset operation to insert after handling submission
        self.current_row = None
        self.setWindowTitle("Master Entry - Add")

    def populate_table(self, search_term=''):
        master_entries = database.get_all_master_entries()
        # master_entries = list(reversed(master_entries))

        if search_term:
            master_entries = [
                entry for entry in master_entries if
                search_term in entry['tenant_name'].lower() or
                search_term in str(entry['house_number']).lower() or
                search_term in str(entry['room_number']).lower()
            ]

        self.master_entry_table.setRowCount(len(master_entries))
        for row, entry in enumerate(master_entries):
            for col, value in enumerate(
                    [entry['house_number'], entry['room_number'], entry['cts_number'], entry['tenant_name'],
                     entry['tenant_mobile'], entry.get('tenant_dod', 'Alive'), entry['notes'], entry['tenant_gender']]):
                item = QTableWidgetItem("" if value is None else str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.master_entry_table.setItem(row, col, item)

            if entry.get('tenant_dod') and isinstance(entry['tenant_dod'], (str, date)):
                item = self.master_entry_table.item(row, 5)
                item.setText(entry['tenant_dod'].strftime('%d-%m-%Y'))

            edit_btn = QPushButton(self)
            edit_btn.setIcon(QIcon('icons' + os.sep + 'pen_icon.png'))
            edit_btn.setIconSize(QSize(20, 20))  # Adjust the size values as needed
            # edit_btn.setStyleSheet("QPushButton { color: blue; }")  # Change color as needed
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_entry(r))
            self.master_entry_table.setCellWidget(row, 8, edit_btn)

            delete_btn = QPushButton(self)
            delete_btn.setIcon(QIcon('icons' + os.sep + 'delete_icon1.png'))
            delete_btn.setIconSize(QSize(30, 30))
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_entry(r))
            self.master_entry_table.setCellWidget(row, 9, delete_btn)

        columns_to_adjust = [0, 1, 2, 3, 4, 5, 6, 7]  # Adjust indices as needed

        for col in columns_to_adjust:
            self.master_entry_table.resizeColumnToContents(col)

    def validate_input(self):
        mandatory_fields = [(self.house_number_combo.currentText(), "House Number"),
                            (self.room_number_combo.currentText(), "Room Number"),
                            (self.cts_number_combo.currentText(), "CTS Number"),
                            (self.tenant_name_input.text(), "Tenant Name")]

        if self.male_rb.isChecked() or self.female_rb.isChecked():
            gender = "Male" if self.male_rb.isChecked() else "Female"
        else:
            gender = ""

        mandatory_fields.append((gender, "Tenant Gender"))

        for value, field_name in mandatory_fields:
            if not value.strip():  # If value is empty or just whitespace
                QMessageBox.warning(self, "Input Error", f"Please fill {field_name}!")
                return False
        return True

    def edit_entry(self, row):
        # Fetch data from the selected row
        house_number = self.master_entry_table.item(row, 0).text()
        room_number = self.master_entry_table.item(row, 1).text()
        cts_number = self.master_entry_table.item(row, 2).text()
        tenant_name = self.master_entry_table.item(row, 3).text()
        tenant_mobile = self.master_entry_table.item(row, 4).text()
        tenant_dod = self.master_entry_table.item(row, 5).text()
        notes = self.master_entry_table.item(row, 6).text()
        tenant_gender = self.master_entry_table.item(row, 7).text()

        self.old_house_number = house_number
        self.old_cts_number = cts_number
        self.old_room_number = room_number

        # Populate the form fields
        self.house_number_combo.setCurrentText(house_number)
        self.cts_number_combo.setCurrentText(cts_number)
        self.room_number_combo.setCurrentText(room_number)
        self.tenant_name_input.setText(tenant_name)
        self.tenant_mobile_input.setText(tenant_mobile)
        # Convert the date from string to QDate and then set it
        # self.tenant_dod_input.setDate(QDate.fromString(tenant_dod, "dd-MM-yyyy"))
        if tenant_dod == "":
            self.is_alive_checkbox.setChecked(True)
            self.tenant_dod_input.clear()
        else:
            self.is_alive_checkbox.setChecked(False)
            self.tenant_dod_input.setDate(QDate.fromString(tenant_dod, "dd-MM-yyyy"))
            self.tenant_dod_input.setDate(QDate.currentDate())

        self.notes_input.setText(notes)
        if tenant_gender == "Male":
            self.male_rb.setChecked(True)
        else:
            self.female_rb.setChecked(True)

        self.operation = "update"
        self.current_row = row
        self.setWindowTitle("Master Entry - Edit")

    def delete_entry(self, row):
        # Confirmation Dialog
        choice = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this entry?",
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.No:
            return

        house_number = self.master_entry_table.item(row, 0).text()
        room_number = self.master_entry_table.item(row, 1).text()
        cts_number = self.master_entry_table.item(row, 2).text()

        try:
            database.delete_master_entry(house_number, cts_number, room_number)
            QMessageBox.information(self, "Success", "Tenant data deleted successfully!")
            self.populate_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Data not deleted!\nError: " + str(e))

    def toggle_dod_input(self, state):
        if state == Qt.Checked:
            self.tenant_dod_input.setDisabled(True)
            self.tenant_dod_input.clear()  # Clear any date that was inputted
        else:
            self.tenant_dod_input.setDisabled(False)
            self.tenant_dod_input.setDate(QDate.currentDate())
