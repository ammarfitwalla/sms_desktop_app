import os
import sys
import configparser
from PyQt5.QtWidgets import (QVBoxLayout, QMenuBar, QAction,
                             QFormLayout, QLabel, QLineEdit, QDateEdit, QCheckBox,
                             QPushButton, QRadioButton, QGridLayout, QHBoxLayout,
                             QTableWidget, QComboBox, QCompleter, QMessageBox, QTableWidgetItem, QApplication)
from db import database
from datetime import date
from PyQt5.QtCore import Qt, QDate
from src.base_class import BaseWindow
from utils.utils import check_dir
from src import bill


class MasterEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_default_state()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.showMaximized()

    def set_default_state(self):
        self.row_idx = None
        self.current_row = None
        self.operation = "insert"
        self.setWindowTitle("Master Entry - Add")

    def switch_to_bill(self):
        self.close()
        self.bill_page = bill.BillEntry()
        self.bill_page.show()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Create a menu bar
        menubar = QMenuBar(self)
        menubar.setStyleSheet(
            """
            QMenuBar {
                background-color: white;
                border-bottom: 1px solid #c1c1c1;
            }
            QMenuBar::item {
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #c1c1c1;
                color: black;
            }
            """
        )

        # Create a File menu
        file_menu = menubar.addMenu('File')
        menubar.addMenu('About')
        menubar.addMenu('Help')

        # Add 'Switch to Master' action under File menu
        switch_to_bill_action = QAction('Bill Entry', self)
        switch_to_bill_action.triggered.connect(self.switch_to_bill)
        file_menu.addAction(switch_to_bill_action)

        switch_to_reports_action = QAction('Reports', self)
        # switch_to_reports_action.triggered.connect(self.close)
        file_menu.addAction(switch_to_reports_action)

        # Add 'Exit' action under File menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        main_layout.setMenuBar(menubar)

        # Create a grid layout for the rest of the UI components
        # layout = QGridLayout()
        layout = QFormLayout()
        main_layout.addLayout(layout)  # Add the grid layout to the main layout

        # --------------------------- HOUSE NUMBER --------------------------- #
        self.house_number_combo = self.setup_combobox(database.get_house_numbers)

        # --------------------------- ROOM NUMBER --------------------------- #
        self.room_number_combo = self.setup_combobox(database.get_room_numbers)

        # --------------------------- CTS NUMBER --------------------------- #
        self.cts_number_combo = self.setup_combobox(database.get_cts_numbers)

        # --------------------------- TENANT ATTRIBUTES --------------------------- #
        self.tenant_name_input = QLineEdit(self)
        self.tenant_mobile_input = QLineEdit(self)
        self.tenant_dod_input = QDateEdit(self)
        self.tenant_dod_input.setDisplayFormat("dd-MM-yyyy")
        self.tenant_dod_input.setCalendarPopup(True)
        self.tenant_dod_input.setDate(QDate.currentDate())
        self.is_alive_checkbox = QCheckBox("Is Alive", self)
        self.is_alive_checkbox.stateChanged.connect(self.toggle_dod_input)
        self.notes_input = QLineEdit(self)
        self.male_rb = QRadioButton("Male", self)
        self.female_rb = QRadioButton("Female", self)
        self.others_rb = QRadioButton("Others", self)

        # --------------------------- SUBMIT BUTTON --------------------------- #
        self.submit_btn = QPushButton("Save", self)
        self.submit_btn.clicked.connect(self.handle_submission)

        # --------------------------- SUBMIT BUTTON --------------------------- #
        self.new_tenant_old_room_btn = QPushButton("Update (New Tenant - Old Room)", self)
        self.new_tenant_old_room_btn.setStyleSheet("color: red;")  # Set text color to red
        self.new_tenant_old_room_btn.clicked.connect(self.on_new_tenant_old_room)

        # --------------------------- CLEAR FORM BUTTON --------------------------- #
        self.clear_form_btn = QPushButton("Clear Form", self)
        self.clear_form_btn.clicked.connect(self.clear_form)

        # --------------------------- EDIT FORM BUTTON --------------------------- #
        # self.edit_btn = QPushButton("Edit", self)
        # self.edit_btn.clicked.connect(self.clear_form)

        # --------------------------- DELETE ENTRY BUTTON --------------------------- #
        self.delete_btn = QPushButton("Delete", self)
        self.delete_btn.clicked.connect(self.delete_entry)

        # --------------------------- ICONS PATH --------------------------- #
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pen_icon_path = os.path.join(self.script_directory, '../icons', 'pen_icon.png')
        self.delete_icon_path = os.path.join(self.script_directory, '../icons', 'delete_icon1.png')

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")

        # Adding widgets to layout
        layout.addRow(QLabel("House Number"), self.house_number_combo)
        layout.addRow(QLabel("Room Number"), self.room_number_combo)
        layout.addRow(QLabel("CTS Number"), self.cts_number_combo)
        layout.addRow(QLabel("Tenant Name"), self.tenant_name_input)
        layout.addRow(QLabel("Tenant Mobile Number"), self.tenant_mobile_input)
        layout.addRow(self.is_alive_checkbox)
        layout.addRow(QLabel("Tenant Date of Death"), self.tenant_dod_input)
        layout.addRow(QLabel("Notes"), self.notes_input)

        gender_layout = QGridLayout()
        gender_layout.addWidget(self.male_rb, 0, 0)
        gender_layout.addWidget(self.female_rb, 0, 1)
        gender_layout.addWidget(self.others_rb, 0, 2)
        layout.addRow(QLabel("Tenant Gender"), gender_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.clear_form_btn)
        button_layout.addWidget(self.new_tenant_old_room_btn)
        # button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        layout.addRow(button_layout)

        layout.addRow(QLabel("Search"), self.search_bar)
        self.search_bar.textChanged.connect(self.filter_table)

        self.master_entry_table = QTableWidget(self)
        self.master_entry_table_columns = ["House No.", "Room No.", "CTS No.", "Name",
                                           "Mobile", "DoD", "Notes", "Gender"]
        self.master_entry_table.setColumnCount(
            len(self.master_entry_table_columns))  # Number of columns based on the fields you have
        self.master_entry_table.setHorizontalHeaderLabels(self.master_entry_table_columns)
        layout.addRow(self.master_entry_table)
        self.master_entry_table.setSortingEnabled(True)
        self.master_entry_table.setShowGrid(True)  # Enable the display of grid lines between cells
        self.master_entry_table.itemClicked.connect(self.edit_entry)

        # Use setStyleSheet to define the grid line color and style
        self.master_entry_table.setStyleSheet("gridline-color: rgb(192, 192, 192);")  # Light grey grid lines

        # You can also set border styles for the headers if desired
        self.master_entry_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")
        self.master_entry_table.verticalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")

        self.config = configparser.ConfigParser()
        # self.base_folder = 'sms_data'
        # check_dir(self.base_folder)
        self.config_file = 'config.ini'
        self.load_config()
        self.adjust_columns()
        self.master_entry_table.horizontalHeader().sectionResized.connect(self.column_resized)
        self.populate_table()

        self.setLayout(layout)
        main_layout.addLayout(layout)

    def load_config(self):
        # Load existing configuration file if it exists
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            if 'MasterColumnWidths' not in self.config.sections():
                self.create_config_section('MasterColumnWidths')
        else:
            self.create_config_section('MasterColumnWidths')

    def create_config_section(self, section_name):
        self.config[section_name] = {}
        self.save_config()

    def adjust_columns(self):
        # Adjust columns based on stored column widths
        for logical_index, column_name in enumerate(self.master_entry_table_columns):
            if 'MasterColumnWidths' in self.config and column_name in self.config['MasterColumnWidths']:
                column_width = int(self.config['MasterColumnWidths'][column_name])
                self.master_entry_table.setColumnWidth(logical_index, column_width)

    def column_resized(self, logical_index, new_size):
        # User has resized a column, save the new size
        try:
            column_name = self.master_entry_table_columns[logical_index]
            self.config.set('MasterColumnWidths', column_name, str(new_size))
            self.save_config()
        except Exception as e:
            print("error", str(e))

    def save_config(self):
        # Save current column widths to configuration
        for logical_index, column_name in enumerate(self.master_entry_table_columns):
            column_width = self.master_entry_table.columnWidth(logical_index)
            self.config.set('MasterColumnWidths', column_name, str(column_width))

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

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
            if self.male_rb.isChecked():
                tenant_gender = "M"
            elif self.female_rb.isChecked():
                tenant_gender = "F"
            else:
                tenant_gender = "O"

            if self.operation == "insert":
                status, message = database.insert_master_entry(house_number, cts_number, room_number, tenant_name,
                                                               tenant_mobile, tenant_dod, notes, tenant_gender)
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
        self.others_rb.setChecked(False)
        self.operation = "insert"  # Reset operation to insert after handling submission
        self.current_row = None
        self.setWindowTitle("Master Entry - Add")

    def on_new_tenant_old_room(self):
        if not self.validate_input():
            return
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, "Confirm Update",
            "Are you sure you want to update the new tenant over the old tenant for the old room?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Call the database update method
            self.update_tenant_for_old_room()

    def update_tenant_for_old_room(self):
        # Collect tenant details from the UI
        house_number = self.house_number_combo.currentText()
        room_number = self.room_number_combo.currentText()
        cts_number = self.cts_number_combo.currentText()
        tenant_name = self.tenant_name_input.text()
        tenant_mobile = self.tenant_mobile_input.text()
        tenant_dod = None if self.is_alive_checkbox.isChecked() else self.tenant_dod_input.date().toString("yyyy-MM-dd")
        notes = self.notes_input.text()

        # Determine tenant gender based on selected radio button
        if self.male_rb.isChecked():
            tenant_gender = "M"
        elif self.female_rb.isChecked():
            tenant_gender = "F"
        else:
            tenant_gender = "O"

        # Retrieve the old tenant ID based on house, CTS, and room number
        old_tenant_id = database.get_tenant_id_by_house_cts_room_number(house_number, cts_number, room_number)

        if old_tenant_id:
            # Check if the old tenant's name matches the new tenant's name
            old_tenant_name = database.get_tenant_name_by_tenant_id(old_tenant_id)
            if old_tenant_name == tenant_name:
                QMessageBox.critical(self, "Error", "Old Tenant Name is the same as the New Tenant Name!")
                return

            # Update old tenant's current status to False
            status, message = database.update_current_tenant_status(old_tenant_id, 'False')
            if not status:
                QMessageBox.warning(self, "Error", str(message))
            else:
                # Update the new tenant details for the old room
                status, message = database.update_new_tenant_to_old_room(
                    house_number, cts_number, room_number, tenant_name,
                    tenant_mobile, tenant_dod, notes, tenant_gender
                )
                if status:
                    QMessageBox.information(self, "Success", str(message))
                else:
                    QMessageBox.warning(self, "Error", str(message))

            self.clear_form()
            self.refresh_combo_box(self.house_number_combo, database.get_house_numbers)
            self.refresh_combo_box(self.room_number_combo, database.get_room_numbers)
            self.refresh_combo_box(self.cts_number_combo, database.get_cts_numbers)

        else:
            # Insert new tenant details as a new entry if no old tenant is found
            status, message = database.insert_master_entry(
                house_number, cts_number, room_number, tenant_name,
                tenant_mobile, tenant_dod, notes, tenant_gender
            )
            if status:
                QMessageBox.information(self, "Success", "Data Inserted Successfully!")
                self.clear_form()
                self.refresh_combo_box(self.house_number_combo, database.get_house_numbers)
                self.refresh_combo_box(self.room_number_combo, database.get_room_numbers)
                self.refresh_combo_box(self.cts_number_combo, database.get_cts_numbers)
            else:
                QMessageBox.warning(self, "Error", str(message))

            # Final notification to confirm the new tenant addition
            QMessageBox.information(self, "Success", f"New tenant '{tenant_name}' added")

        self.populate_table()

    def populate_table(self, search_term=''):
        master_entries = database.get_all_master_entries()

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
                item.setToolTip(str(value))

                self.master_entry_table.setItem(row, col, item)

            if entry.get('tenant_dod') and isinstance(entry['tenant_dod'], (str, date)):
                item = self.master_entry_table.item(row, 5)
                item.setText(entry['tenant_dod'].strftime('%d-%m-%Y'))

            # edit_btn = QPushButton(self)
            # edit_btn.setIcon(QIcon(self.pen_icon_path))
            # edit_btn.setIconSize(QSize(20, 20))
            # edit_btn.clicked.connect(lambda checked, r=row: self.edit_entry(r))
            # self.master_entry_table.setCellWidget(row, 8, edit_btn)
            # edit_btn.setFixedWidth(50)
            # self.master_entry_table.setColumnWidth(8, 50)
            #
            # delete_btn = QPushButton(self)
            # delete_btn.setIcon(QIcon(self.delete_icon_path))
            # delete_btn.setIconSize(QSize(30, 30))
            # delete_btn.clicked.connect(lambda checked, r=row: self.delete_entry(r))
            # self.master_entry_table.setCellWidget(row, 9, delete_btn)
            # delete_btn.setFixedWidth(50)
            # self.master_entry_table.setColumnWidth(9, 50)

        # columns_to_adjust = [0, 1, 2, 4, 5, 6, 7]  # Adjust indices as needed
        #
        # for col in columns_to_adjust:
        #     self.master_entry_table.resizeColumnToContents(col)
        #
        # self.master_entry_table.setColumnWidth(3, 300)
        # self.master_entry_table.setColumnWidth(6, 300)
        # self.master_entry_table.setColumnWidth(1, 80)

        # self.adjust_columns()

    def validate_input(self):
        mandatory_fields = [(self.house_number_combo.currentText(), "House Number"),
                            (self.room_number_combo.currentText(), "Room Number"),
                            (self.cts_number_combo.currentText(), "CTS Number"),
                            (self.tenant_name_input.text(), "Tenant Name")]

        if self.male_rb.isChecked() or self.female_rb.isChecked() or self.others_rb.isChecked():
            if self.male_rb.isChecked():
                gender = "Male"
            elif self.female_rb.isChecked():
                gender = "Female"
            else:
                gender = "Others"
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
        self.row_idx = row.row()
        house_number = self.master_entry_table.item(self.row_idx, 0).text()
        room_number = self.master_entry_table.item(self.row_idx, 1).text()
        cts_number = self.master_entry_table.item(self.row_idx, 2).text()
        tenant_name = self.master_entry_table.item(self.row_idx, 3).text()
        tenant_mobile = self.master_entry_table.item(self.row_idx, 4).text()
        tenant_dod = self.master_entry_table.item(self.row_idx, 5).text()
        notes = self.master_entry_table.item(self.row_idx, 6).text()
        tenant_gender = self.master_entry_table.item(self.row_idx, 7).text()

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

        self.notes_input.setText(notes)
        if tenant_gender == "M":
            self.male_rb.setChecked(True)
        elif tenant_gender == 'F':
            self.female_rb.setChecked(True)
        else:
            self.others_rb.setChecked(True)

        self.operation = "update"
        self.current_row = row
        self.setWindowTitle("Master Entry - Edit")

    def delete_entry(self):
        choice = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this Tenant?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return
        try:
            house_number = self.master_entry_table.item(self.row_idx, 0).text()
            room_number = self.master_entry_table.item(self.row_idx, 1).text()
            cts_number = self.master_entry_table.item(self.row_idx, 2).text()
            database.delete_master_entry(house_number, cts_number, room_number)
            self.populate_table()
            self.clear_form()
            QMessageBox.information(self, "Success", "Tenant deleted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", "Data not deleted!\nError: " + str(e))

    def toggle_dod_input(self, state):
        if state == Qt.Checked:
            self.tenant_dod_input.setDisabled(True)
            self.tenant_dod_input.clear()  # Clear any date that was inputted
        else:
            self.tenant_dod_input.setDisabled(False)
            self.tenant_dod_input.setDate(QDate.currentDate())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MasterEntry()
    window.show()
    sys.exit(app.exec_())
