from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton, QRadioButton, QDateEdit, QGridLayout, QCheckBox
import database
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from base_class import BaseWindow
from PyQt5.QtWidgets import QHBoxLayout


class MasterEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.operation = "insert"  # By default, the operation is insert
        self.current_row = None  # To store the tenant_id when editing

    def init_ui(self):
        layout = QFormLayout()

        # --------------------------- HOUSE NUMBER --------------------------- #
        # House Number Combo Box
        self.house_number_combo = QComboBox(self)
        self.house_number_combo.setEditable(True)
        # Set up QCompleter for the ComboBox
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.house_number_combo.setCompleter(self.completer)
        # Load house numbers into ComboBox and Completer
        house_numbers = database.get_house_numbers()
        self.house_number_combo.addItems(house_numbers)
        self.house_number_combo.setCurrentIndex(-1)
        self.completer.setModel(self.house_number_combo.model())

        # --------------------------- ROOM NUMBER --------------------------- #
        self.room_number_combo = QComboBox(self)
        self.room_number_combo.setEditable(True)
        room_completer = QCompleter(self)
        room_completer.setCaseSensitivity(Qt.CaseInsensitive)
        room_completer.setFilterMode(Qt.MatchContains)
        self.room_number_combo.setCompleter(room_completer)
        room_numbers = database.get_room_numbers()
        self.room_number_combo.addItems(room_numbers)
        self.room_number_combo.setCurrentIndex(-1)
        room_completer.setModel(self.room_number_combo.model())

        # --------------------------- CTS NUMBER --------------------------- #
        self.cts_number_combo = QComboBox(self)
        self.cts_number_combo.setEditable(True)
        cts_completer = QCompleter(self)
        cts_completer.setCaseSensitivity(Qt.CaseInsensitive)
        cts_completer.setFilterMode(Qt.MatchContains)
        self.cts_number_combo.setCompleter(cts_completer)
        cts_numbers = database.get_cts_numbers()
        self.cts_number_combo.addItems(cts_numbers)
        self.cts_number_combo.setCurrentIndex(-1)
        cts_completer.setModel(self.cts_number_combo.model())

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

        # layout.addRow(self.submit_btn)
        # layout.addRow(self.clear_form_btn)
        # layout.addRow(self.submit_btn, self.clear_form_btn)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.clear_form_btn)
        layout.addRow(button_layout)

        self.master_entry_table = QTableWidget(self)
        self.master_entry_table.setColumnCount(10)  # Number of columns based on the fields you have
        self.master_entry_table.setHorizontalHeaderLabels(["House No.", "Room No.", "CTS No.", "Tenant Name", "Tenant Mobile", "Tenant DoD", "Notes", "Gender", "Edit", "Delete"])
        layout.addRow(self.master_entry_table)
        self.populate_table()

        self.setLayout(layout)

    def handle_submission(self):  # TODO: ADD VALIDATION OF EXISTING DATA
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
                # tenant_dod = self.tenant_dod_input.date().toString("yyyy-MM-dd")  # Convert QDate to string in "yyyy-MM-dd" format
            notes = self.notes_input.text()
            tenant_gender = "Male" if self.male_rb.isChecked() else "Female"

            if self.operation == "insert":
                database.insert_master_entry(house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender)
                QMessageBox.information(self, "Success", "Data inserted successfully!")
            else:
                database.update_master_entry(self.old_house_number, self.old_cts_number, self.old_room_number, house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender)
                self.operation = "insert"  # Reset operation to insert after handling submission
                self.current_row = None
                QMessageBox.information(self, "Success", "Data Updated successfully!")

            self.clear_form()
            self.populate_table()

        except Exception as e:
            QMessageBox.critical(self, "Error", "Data not inserted!\nError: " + str(e))

    def clear_form(self):
        # Clear all the input fields
        self.house_number_combo.setCurrentIndex(-1)
        self.cts_number_combo.setCurrentIndex(-1)
        self.room_number_combo.setCurrentIndex(-1)
        self.tenant_name_input.clear()
        self.tenant_mobile_input.clear()
        self.tenant_dod_input.setDate(QDate.currentDate())  # Resetting to the current date
        self.notes_input.clear()
        # Resetting gender radio buttons (assuming male as default)
        self.male_rb.setChecked(False)
        self.female_rb.setChecked(False)

    def populate_table(self):
        master_entries = database.get_all_master_entries()  # Assuming a method to fetch all entries

        self.master_entry_table.setRowCount(len(master_entries))

        for row, entry in enumerate(master_entries):
            self.master_entry_table.setItem(row, 0, QTableWidgetItem(entry['house_number']))
            self.master_entry_table.setItem(row, 1, QTableWidgetItem(entry['room_number']))
            self.master_entry_table.setItem(row, 2, QTableWidgetItem(entry['cts_number']))
            self.master_entry_table.setItem(row, 3, QTableWidgetItem(entry['tenant_name']))
            self.master_entry_table.setItem(row, 4, QTableWidgetItem(entry['tenant_mobile']))
            # self.master_entry_table.setItem(row, 5, QTableWidgetItem(entry['tenant_dod'].strftime('%d-%m-%Y')))
            if entry['tenant_dod']:
                self.master_entry_table.setItem(row, 5, QTableWidgetItem(entry['tenant_dod'].strftime('%d-%m-%Y')))
            else:
                self.master_entry_table.setItem(row, 5, QTableWidgetItem("Alive"))
            self.master_entry_table.setItem(row, 6, QTableWidgetItem(entry['notes']))
            self.master_entry_table.setItem(row, 7, QTableWidgetItem(entry['tenant_gender']))

            edit_btn = QPushButton("Edit", self)
            edit_btn.clicked.connect(lambda _, row=row: self.edit_entry(row))
            self.master_entry_table.setCellWidget(row, 8, edit_btn)

            delete_btn = QPushButton("Delete", self)
            delete_btn.clicked.connect(lambda _, row=row: self.delete_entry(row))
            self.master_entry_table.setCellWidget(row, 9, delete_btn)

    def validate_input(self):
        mandatory_fields = [(self.house_number_combo.currentText(), "House Number"), (self.room_number_combo.currentText(), "Room Number"), (self.cts_number_combo.currentText(), "CTS Number"), (self.tenant_name_input.text(), "Tenant Name")]

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
        if tenant_dod == "Alive":
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

    def delete_entry(self, row):
        # Confirmation Dialog
        choice = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.No:
            return

        house_number = self.master_entry_table.item(row, 0).text()
        room_number = self.master_entry_table.item(row, 1).text()
        cts_number = self.master_entry_table.item(row, 2).text()

        try:
            print(house_number, cts_number, room_number)
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
