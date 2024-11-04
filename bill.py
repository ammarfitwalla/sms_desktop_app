import os
import sys
from datetime import datetime, date
from PyQt5 import QtCore
from PyQt5.QtCore import QDate, Qt, QSize
from PyQt5.QtGui import QPainter, QImage, QFont, QIcon, QIntValidator
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QLineEdit, QDateEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QTableWidget, QHBoxLayout, QMessageBox, QTableWidgetItem, QAction, \
    QMenuBar, QCheckBox, QSizePolicy, QCalendarWidget, QToolButton, QWidget
from utils import split_string, get_date_month_year, convert_date_string, check_dir
import master_entry
import database
from base_class import BaseWindow
import configparser


# class CustomDateEditWithButton(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # Main layout for the widget
#         layout = QHBoxLayout(self)
#
#         # Create the QDateEdit
#         self.date_edit = QDateEdit()
#         self.date_edit.setCalendarPopup(True)
#         self.date_edit.setDate(QDate.currentDate())
#
#         # Create a QToolButton that looks like a link or small button
#         self.today_button = QToolButton()
#         self.today_button.setText("Today’s Date")
#         self.today_button.setStyleSheet("QToolButton {color: blue; font-size: 14px;}")
#         self.today_button.setCursor(Qt.PointingHandCursor)
#         self.today_button.clicked.connect(self.set_today_date)
#
#         # Add widgets to layout
#         # layout.addWidget(QLabel("Received Date"))
#         layout.addWidget(self.date_edit)
#         layout.addWidget(self.today_button)
#
#     def set_today_date(self):
#         self.date_edit.setDate(QDate.currentDate())

class BillEntry(BaseWindow):
    def __init__(self):
        super().__init__()
        self.operation = "insert"
        self.init_ui()
        self.set_default_state()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.showMaximized()

    def set_default_state(self):
        self.bill_id = None
        self.current_row = None
        self.setWindowTitle("Bill Entry - Add")

    def switch_to_master(self):
        self.close()
        self.master_page = master_entry.MasterEntry()
        self.master_page.show()

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
        switch_to_master_action = QAction('Master Entry', self)
        switch_to_master_action.triggered.connect(self.switch_to_master)
        file_menu.addAction(switch_to_master_action)

        switch_to_reports_action = QAction('Reports', self)
        # switch_to_reports_action.triggered.connect(self.close)
        file_menu.addAction(switch_to_reports_action)

        # Add 'Exit' action under File menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        main_layout.setMenuBar(menubar)

        # ------------------------------------- Create grid layout ------------------------------------- #
        layout = QGridLayout()
        main_layout.addLayout(layout)

        self.bill_for_month_of_label = QLabel('Bill For Month Of')
        self.bill_for_month_of = QDateEdit()
        # self.bill_for_month_of.setCalendarPopup(True)  # Enable calendar popup
        self.bill_for_month_of.setDisplayFormat('MMM-yyyy')
        self.bill_for_month_of.setDate(QDate.currentDate())
        layout.addWidget(self.bill_for_month_of_label, 0, 0)
        layout.addWidget(self.bill_for_month_of, 0, 1)  # Spanning across two columns for space

        self.book_number_label = QLabel('Book Number')
        self.book_number_line = QLineEdit()
        self.book_number_line.setValidator(QIntValidator())

        self.bill_number_label = QLabel('Bill Number')
        self.bill_number_line = QLineEdit()
        self.bill_number_line.setValidator(QIntValidator())
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
        self.house_number_combo.addItem(" ")

        self.room_number_label = QLabel('Room Number')
        self.room_number_combo = QComboBox()

        self.cts_number_line = QLineEdit()
        self.cts_number_line.setReadOnly(True)
        self.cts_number_label = QLabel('CTS Number')

        self.tenant_name_combo = QComboBox()
        self.tenant_name_label = QLabel('Tenant Name')

        self.populate_houses_dropdown()  # This function populates the house_number_combo
        self.house_number_combo.currentIndexChanged.connect(self.house_changed)
        self.tenant_name_combo.currentIndexChanged.connect(self.tenant_changed)
        self.room_number_combo.currentIndexChanged.connect(self.room_changed)

        # Explicitly calling house_changed to update room and CTS fields based on the initially displayed house
        self.house_changed()
        self.tenant_changed()
        layout.addWidget(self.house_number_label, 1, 0)
        layout.addWidget(self.house_number_combo, 1, 1)
        layout.addWidget(self.room_number_label, 1, 2)
        layout.addWidget(self.room_number_combo, 1, 3)
        layout.addWidget(self.cts_number_label, 1, 4)
        layout.addWidget(self.cts_number_line, 1, 5)

        layout.addWidget(self.tenant_name_label, 2, 0)
        # layout.addWidget(self.tenant_name_combo, 2, 1, 1, 1)
        layout.addWidget(self.tenant_name_combo, 2, 1)

        # Row 3
        self.purpose_label = QLabel('Purpose For')
        self.purpose_line = QLineEdit()
        self.purpose_line.setText("For Residence")
        # self.purpose_line.setText('For Residence')
        layout.addWidget(self.purpose_label, 3, 0)
        layout.addWidget(self.purpose_line, 3, 1)

        self.rent_from_label = QLabel('Rent From')
        self.rent_from_date = QDateEdit()
        self.rent_from_date.setDisplayFormat('MMM-yyyy')
        self.rent_from_date.setDate(QDate.currentDate())
        self.rent_to_label = QLabel('Rent To')
        self.rent_to_date = QDateEdit()
        self.rent_to_date.setDisplayFormat('MMM-yyyy')
        self.rent_to_date.setDate(QDate.currentDate())
        # self.rent_to_date.setReadOnly(True)
        layout.addWidget(self.rent_from_label, 3, 2)
        layout.addWidget(self.rent_from_date, 3, 3)
        layout.addWidget(self.rent_to_label, 3, 4)
        layout.addWidget(self.rent_to_date, 3, 5)

        self.bill_for_month_of.dateChanged.connect(self.update_rent_to_date)
        self.rent_to_date.dateChanged.connect(self.update_bill_for_month_of_date)
        self.rent_from_date.dateChanged.connect(self.update_total_months)
        self.rent_to_date.dateChanged.connect(self.update_total_months)

        # Row 4
        self.at_the_rate_of_label = QLabel('@')
        self.at_the_rate_of = QLineEdit()
        self.at_the_rate_of.setValidator(QIntValidator())
        # self.at_the_rate_of.setText('350')
        self.at_the_rate_of.textChanged.connect(self.update_total_rupees)
        layout.addWidget(self.at_the_rate_of_label, 4, 0)
        layout.addWidget(self.at_the_rate_of, 4, 1)

        self.total_months_label = QLabel('Total Months')
        self.total_months_line = QLineEdit()
        self.total_months_line.setReadOnly(True)
        self.total_months_line.textChanged.connect(self.update_total_rupees)  # Connect to slot method
        layout.addWidget(self.total_months_label, 4, 2)
        layout.addWidget(self.total_months_line, 4, 3)

        self.total_rupees_label = QLabel('Total Rupees')
        self.total_rupees_line = QLineEdit()
        self.total_rupees_line.setReadOnly(True)
        self.total_rupees_line.setText('0')
        layout.addWidget(self.total_rupees_label, 4, 4)
        layout.addWidget(self.total_rupees_line, 4, 5)

        # Row 5
        # self.received_date_label = QLabel('Received Date')
        # self.received_date = QDateEdit()
        # self.received_date.setCalendarPopup(True)
        # self.received_date.setDate(QDate.currentDate())
        # layout.addWidget(self.received_date_label, 5, 0)
        # layout.addWidget(self.received_date, 5, 1)
        #
        # self.today_button = QToolButton()
        # self.today_button.setText("Today’s Date")
        # self.today_button.setStyleSheet("QToolButton {color: blue; font-size: 14px;}")
        # self.today_button.setCursor(Qt.PointingHandCursor)
        # self.today_button.clicked.connect(self.set_today_date)
        # layout.addWidget(self.today_button, 5, 2)

        # Label for received date
        self.received_date_label = QLabel('Received Date')
        layout.addWidget(self.received_date_label, 5, 0)

        # Create a horizontal layout to hold the date edit and button together
        date_layout = QHBoxLayout()

        # Date edit field
        self.received_date = QDateEdit()
        self.received_date.setCalendarPopup(True)
        self.received_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.received_date)

        # Today’s Date button
        self.today_button = QToolButton()
        self.today_button.setText("Today’s Date")
        self.today_button.setStyleSheet("QToolButton {color: blue; font-size: 14px;}")
        self.today_button.setCursor(Qt.PointingHandCursor)
        self.today_button.clicked.connect(self.set_today_date_in_received_date)
        date_layout.addWidget(self.today_button)

        # Add the horizontal layout to the main layout at row 5, column 1
        layout.addLayout(date_layout, 5, 1)

        # self.received_date_label = QLabel('Received Date')
        # self.custom_date_edit = CustomDateEditWithButton()
        # layout.addWidget(self.custom_date_edit)
        # layout.addWidget(self.received_date_label, 5, 0)
        # layout.addWidget(self.custom_date_edit, 5, 1)

        self.extra_payment_label = QLabel('Extra Payment')
        self.extra_payment_line = QLineEdit()
        self.extra_payment_line.setValidator(QIntValidator())
        self.extra_payment_line.setText(str(0))
        layout.addWidget(self.extra_payment_label, 5, 2)
        layout.addWidget(self.extra_payment_line, 5, 3)

        self.agreement_date_label = QLabel('Agreement Date')
        self.agreement_date = QDateEdit()
        self.agreement_date.setCalendarPopup(True)
        self.agreement_date.setDate(QDate.currentDate())
        layout.addWidget(self.agreement_date_label, 5, 4)

        # Checkbox to indicate date is not available
        self.is_alive_checkbox = QCheckBox("Date N/A", self)
        self.agreement_date.setDisabled(True)
        self.is_alive_checkbox.setChecked(True)
        self.is_alive_checkbox.stateChanged.connect(self.toggle_agreement_date_input)

        # Layout for Agreement Date and Checkbox
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.agreement_date)
        hlayout.addWidget(self.is_alive_checkbox)
        hlayout.setSpacing(10)
        layout.addLayout(hlayout, 5, 5)

        # Agreement Date "Today’s Date" Button
        self.agreement_today_button = QToolButton()
        self.agreement_today_button.setText("Today’s Date")
        self.agreement_today_button.setStyleSheet("QToolButton {color: blue; font-size: 14px;}")
        self.agreement_today_button.setCursor(Qt.PointingHandCursor)
        self.agreement_today_button.clicked.connect(self.set_today_date_in_agreement_date)
        hlayout.addWidget(self.agreement_today_button)

        # Adjusting size and alignment for Agreement Date label and date input
        self.agreement_date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.agreement_date_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.agreement_date.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.agreement_date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Row 6
        # Add the QVBoxLayout to the main QGridLayout
        self.notes_label = QLabel('Notes')
        self.notes_text = QLineEdit()
        layout.addWidget(self.notes_label, 6, 0, 1, 5)
        layout.addWidget(self.notes_text, 6, 1, 1, 5)

        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pen_icon_path = os.path.join(self.script_directory, 'icons', 'pen_icon.png')
        self.delete_icon_path = os.path.join(self.script_directory, 'icons', 'delete_icon1.png')
        self.printer_icon_path = os.path.join(self.script_directory, 'icons', 'printer_icon.png')

        # Row 7
        buttons_layout = QHBoxLayout()

        # Create Submit Button
        self.submit_button = QPushButton('Save')
        self.submit_button.clicked.connect(self.submit_data)
        buttons_layout.addWidget(self.submit_button)

        # Create Clear Button
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_button)

        self.edit_button = QPushButton('Edit')
        # self.edit_button.setIcon(QIcon(self.pen_icon_path))
        # self.edit_button.setIconSize(QSize(20, 20))
        self.edit_button.clicked.connect(self.edit_record)
        buttons_layout.addWidget(self.edit_button)
        self.edit_button.setDisabled(True)

        # Create Print Button
        self.print_button = QPushButton('Print')
        self.print_button.clicked.connect(self.print_data)  # You need to define the print_data method
        # self.print_button.setIcon(QIcon(self.printer_icon_path))
        # self.print_button.setIconSize(QSize(20, 20))
        buttons_layout.addWidget(self.print_button)
        self.print_button.setDisabled(True)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_record)
        # self.delete_button.setIcon(QIcon(self.delete_icon_path))
        # self.delete_button.setIconSize(QSize(20, 20))
        buttons_layout.addWidget(self.delete_button)
        self.delete_button.setDisabled(True)

        layout.addLayout(buttons_layout, 7, 1, 1, 5)  # Assuming row 7 is where you want the buttons

        # Row 8
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.rr_bill_path = os.path.join(self.script_directory, 'images', 'output_bill_blank_image.png')
        # self.rr_bill_path = os.path.join(self.script_directory, 'images', 'rr_bill.jpg')

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        search_label = QLabel("Search")
        layout.addWidget(search_label, 8, 0)
        layout.addWidget(self.search_bar, 8, 1, 1, -1)

        # Row 9
        # Connect the search bar's textChanged signal to the filter_table method
        self.search_bar.textChanged.connect(self.filter_table)

        self.bill_entry_table = QTableWidget(self)

        self.bill_table_columns = ["Received Date", "House No.", "Room No.", "CTS No.", "Name",
                                   "Rent From", "Rent To", "@", "Total Months", "Total Amount",
                                   "Book No.", "Bill No.", "Extra Payment", "Purpose For",
                                   "Mobile", "DoD", "Agreement Date", "Notes", "Gender"]
        #
        # self.bill_table_columns = ["Received\nDate", "House\nNo.", "Room\nNo.", "CTS\nNo.", "Name",
        #                            "Rent\nFrom", "Rent\nTo", "@", "Total\nMonths", "Total\nAmount",
        #                            "Book\nNo.", "Bill\nNo.", "Extra\nPayment", "Purpose\nFor",
        #                            "Mobile", "DoD", "Agreement\nDate", "Notes", "Gender"]

        self.bill_table_columns_to_display = [i.replace(" ", "\n") if " " in i else i for i in self.bill_table_columns]

        self.bill_entry_table.setColumnCount(len(self.bill_table_columns))
        self.bill_entry_table.setHorizontalHeaderLabels(self.bill_table_columns_to_display)
        layout.addWidget(self.bill_entry_table, 9, 0, 1, 6)

        self.bill_entry_table.setSortingEnabled(True)
        self.bill_entry_table.setShowGrid(True)  # Enable the display of grid lines between cells

        # Use setStyleSheet to define the grid line color and style
        self.bill_entry_table.setStyleSheet("gridline-color: rgb(192, 192, 192);")  # Light grey grid lines

        # You can also set border styles for the headers if desired
        self.bill_entry_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")
        self.bill_entry_table.verticalHeader().setStyleSheet(
            "QHeaderView::section {border: 0.5px solid rgb(192, 192, 192);}")

        # name_column_index = self.bill_table_columns.index("Name")
        # name_column_width = 100
        # self.bill_entry_table.setColumnWidth(name_column_index, name_column_width)

        self.bill_entry_table.itemClicked.connect(self.print_record)

        self.config = configparser.ConfigParser()
        self.base_folder = 'sms_data'
        check_dir(self.base_folder)
        self.config_file = os.path.join(self.base_folder, 'config.ini')
        self.load_config()
        self.adjust_columns()
        self.bill_entry_table.horizontalHeader().sectionResized.connect(self.column_resized)
        self.populate_table()
        self.update_total_months()

    def load_config(self):
        # Load existing configuration file if it exists
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            if 'BillColumnWidths' not in self.config.sections():
                self.create_config_section('BillColumnWidths')
        else:
            self.create_config_section('BillColumnWidths')

    def create_config_section(self, section_name):
        self.config[section_name] = {}
        self.save_config()

    def adjust_columns(self):
        # Adjust columns based on stored column widths
        for logical_index, column_name in enumerate(self.bill_table_columns):
            if 'BillColumnWidths' in self.config and column_name in self.config['BillColumnWidths']:
                column_width = int(self.config['BillColumnWidths'][column_name])
                self.bill_entry_table.setColumnWidth(logical_index, column_width)

    def column_resized(self, logical_index, new_size):
        # User has resized a column, save the new size
        try:
            column_name = self.bill_table_columns[logical_index]
            self.config.set('BillColumnWidths', column_name, str(new_size))
            self.save_config()
        except Exception as e:
            print("error", str(e))

    def save_config(self):
        # Save current column widths to configuration
        for logical_index, column_name in enumerate(self.bill_table_columns):
            column_width = self.bill_entry_table.columnWidth(logical_index)
            self.config.set('BillColumnWidths', column_name, str(column_width))

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    # Functions to handle today date setting
    def set_today_date_in_received_date(self):
        """Set today’s date in the received_date field"""
        self.received_date.setDate(QDate.currentDate())

    def set_today_date_in_agreement_date(self):
        """Set today’s date in the agreement_date field"""
        self.agreement_date.setDate(QDate.currentDate())

    def toggle_agreement_date_input(self, state):
        """Enable or disable the agreement date input based on the checkbox state."""
        if state == Qt.Checked:
            self.agreement_date.setDisabled(True)
            self.agreement_date.clear()  # Clear the date if Date N/A is checked
            self.agreement_date.setDate(QDate.currentDate())
        else:
            self.agreement_date.setDisabled(False)

    def filter_table(self):
        search_term = self.search_bar.text().lower()
        self.populate_table(search_term)

    def populate_table(self, search_term=''):
        bill_entries = database.get_all_bill_entries()

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

                    # Set tooltip for the "Name" column
                    # if column_name == "Tenant Name":  # Replace with your actual column name
                    item.setToolTip(str(data))
                self.bill_entry_table.item(row_number, 0).setData(Qt.UserRole, tenant_id)
                # Add 'Edit' and 'Delete' buttons
                # self.add_table_buttons(row_number)

            # # columns_to_adjust = [i for i in range(len(column_names))]  # Adjust indices as needed
            # columns_to_adjust = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18]  # Adjust indices as needed
            #
            # for col in columns_to_adjust:
            #     self.bill_entry_table.resizeColumnToContents(col)
            #
            # self.bill_entry_table.setColumnWidth(4, 250)
            # self.bill_entry_table.setColumnWidth(2, 80)
            # self.bill_entry_table.setColumnWidth(13, 80)
            # self.bill_entry_table.setColumnWidth(17, 100)

    def add_table_buttons(self, row):
        btn_edit = QPushButton(self)
        btn_edit.clicked.connect(lambda: self.edit_record(row))
        btn_edit.setIcon(QIcon(self.pen_icon_path))
        btn_edit.setIconSize(QSize(20, 20))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 3, btn_edit)
        btn_edit.setFixedWidth(50)

        # Print button
        btn_print = QPushButton(self)
        btn_print.clicked.connect(lambda: self.print_record(row))
        btn_print.setIcon(QIcon(self.printer_icon_path))
        btn_print.setIconSize(QSize(40, 40))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 2, btn_print)
        btn_print.setFixedWidth(50)

        # Delete button
        btn_delete = QPushButton(self)
        btn_delete.clicked.connect(lambda: self.delete_record(row))
        btn_delete.setIcon(QIcon(self.delete_icon_path))
        btn_delete.setIconSize(QSize(30, 30))
        self.bill_entry_table.setCellWidget(row, len(self.bill_table_columns) - 1, btn_delete)
        btn_delete.setFixedWidth(50)

        button_columns = [len(self.bill_table_columns) - 3, len(self.bill_table_columns) - 2,
                          len(self.bill_table_columns) - 1]
        for col in button_columns:
            self.bill_entry_table.setColumnWidth(col, 50)

    def make_form_readonly(self):
        # Iterate over all the form fields to set them to read-only
        for field in [self.received_date, self.bill_for_month_of, self.rent_from_date, self.rent_to_date,
                      self.at_the_rate_of, self.total_months_line, self.total_rupees_line,
                      self.book_number_line, self.bill_number_line, self.extra_payment_line,
                      self.purpose_line, self.agreement_date, self.house_number_combo,
                      self.room_number_combo, self.tenant_name_combo, self.cts_number_line, self.notes_text,
                      self.submit_button, self.is_alive_checkbox, self.today_button, self.agreement_today_button]:
            if isinstance(field, QComboBox):
                field.setEnabled(False)
            elif isinstance(field, QPushButton):
                field.setDisabled(True)
            elif isinstance(field, QCheckBox):
                field.setDisabled(True)
            elif isinstance(field, QToolButton):
                field.setDisabled(True)
            else:
                field.setReadOnly(True)

    def make_form_editable(self):
        # Iterate over all the form fields to set them to editable
        for field in [self.received_date, self.bill_for_month_of, self.rent_from_date, self.rent_to_date,
                      self.at_the_rate_of, self.total_months_line, self.total_rupees_line,
                      self.book_number_line, self.bill_number_line, self.extra_payment_line,
                      self.purpose_line, self.agreement_date, self.house_number_combo,
                      self.room_number_combo, self.cts_number_line, self.tenant_name_combo, self.notes_text,
                      self.submit_button, self.is_alive_checkbox, self.agreement_today_button, self.today_button]:
            if isinstance(field, QComboBox):
                field.setEnabled(True)
            elif isinstance(field, QDateEdit):
                field.setReadOnly(False)
            elif isinstance(field, QPushButton):
                field.setDisabled(False)
            elif isinstance(field, QCheckBox):
                field.setDisabled(False)
            elif isinstance(field, QToolButton):
                field.setDisabled(False)
            else:
                field.setReadOnly(False)
                field.setDisabled(False)

    def get_data_from_row(self, row):
        # Define column indices
        columns = {'RECEIVED_DATE': 0, 'HOUSE_NO': 1, 'ROOM_NO': 2, 'CTS_NO': 3, 'TENANT_NAME': 4, 'RENT_FROM': 5,
                   'RENT_TO': 6, 'AT_THE_RATE_OF': 7, 'TOTAL_MONTHS': 8, 'TOTAL_AMOUNT': 9, 'BOOK_NO': 10,
                   'BILL_NO': 11, 'EXTRA_PAYMENT': 12, 'PURPOSE_FOR': 13, 'AGREEMENT_DATE': 16,
                   'BILL_ID': 0}

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
        # Check if the key is present before accessing it
        if 'RECEIVED_DATE' in data:
            self.received_date.setDate(QDate.fromString(data['RECEIVED_DATE'], 'yyyy-MM-dd'))
            # bill_for_month_of

        if 'BILL_FOR_MONTH_OF' in data:
            self.bill_for_month_of.setDate(QDate.fromString(data['BILL_FOR_MONTH_OF'], 'MMM-yyyy'))

        if 'RENT_FROM' in data:
            self.rent_from_date.setDate(QDate.fromString(data['RENT_FROM'], 'MMM-yyyy'))

        if 'RENT_TO' in data:
            self.rent_to_date.setDate(QDate.fromString(data['RENT_TO'], 'MMM-yyyy'))

        if 'AT_THE_RATE_OF' in data:
            self.at_the_rate_of.setText(str(data['AT_THE_RATE_OF']))

        if 'TOTAL_MONTHS' in data:
            self.total_months_line.setText(str(data['TOTAL_MONTHS']))

        if 'TOTAL_AMOUNT' in data:
            self.total_rupees_line.setText(str(data['TOTAL_AMOUNT']))

        if 'BOOK_NO' in data:
            self.book_number_line.setText(str(data['BOOK_NO']))

        if 'BILL_NO' in data:
            self.bill_number_line.setText(str(data['BILL_NO']))

        if 'EXTRA_PAYMENT' in data:
            self.extra_payment_line.setText(str(data['EXTRA_PAYMENT']))

        if 'PURPOSE_FOR' in data:
            self.purpose_line.setText(data['PURPOSE_FOR'])

        if 'AGREEMENT_DATE' in data:
            if data["AGREEMENT_DATE"] == "":
                self.is_alive_checkbox.setChecked(True)
                self.agreement_date.clear()
            else:
                self.is_alive_checkbox.setChecked(False)
                self.agreement_date.setDate(QDate.fromString(data["AGREEMENT_DATE"], "yyyy-MM-dd"))

        if 'NOTES' in data:
            self.notes_text.setText(data['NOTES'])

        if 'HOUSE_NO' in data:
            self.house_number_combo.setCurrentText(data['HOUSE_NO'])

        if 'TENANT_NAME' in data:
            tenant_name = data['TENANT_NAME']
            if tenant_name:
                index = self.tenant_name_combo.findText(tenant_name)
                if index != -1:
                    self.tenant_name_combo.setCurrentIndex(index)
                else:
                    self.tenant_name_combo.addItem(tenant_name)
                    self.tenant_name_combo.setCurrentIndex(self.tenant_name_combo.count() - 1)
            # self.tenant_name_combo.setCurrentText(data['TENANT_NAME'])

        if 'ROOM_NO' in data:
            room_no = data['ROOM_NO']
            if room_no:
                index = self.room_number_combo.findText(room_no)
                if index != -1:
                    self.room_number_combo.setCurrentIndex(index)
                else:
                    self.room_number_combo.addItem(room_no)
                    self.room_number_combo.setCurrentIndex(self.room_number_combo.count() - 1)
            # self.room_number_combo.setCurrentText(data['ROOM_NO'])

        if 'CTS_NO' in data:
            self.cts_number_line.setText(data['CTS_NO'])

        # If additional data was fetched from the database
        if 'BILL_ID' in data and data['BILL_ID']:
            self.bill_id = data['BILL_ID']
            bill_for_month_of, notes = database.fetch_data_for_edit_record(data['BILL_ID'])
            if bill_for_month_of:
                self.bill_for_month_of.setDate(QDate.fromString(bill_for_month_of, 'MMM-yyyy'))
            if notes:
                self.notes_text.setText(notes)

    def print_record(self, row):
        self.operation = 'print'
        data = self.get_data_from_row(row.row())
        self.set_data_to_form(data)
        self.make_form_readonly()
        self.cts_number_line.setDisabled(True)
        self.setWindowTitle("Bill Entry - Print")
        self.print_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.edit_button.setEnabled(True)

    # def edit_record(self, row):
    #     if self.operation == 'print':
    #         self.make_form_editable()
    #         self.print_button.setDisabled(True)
    #     data = self.get_data_from_row(row.row())
    #     self.set_data_to_form(data)
    #     self.house_number_combo.setDisabled(True)
    #     self.tenant_name_combo.setDisabled(True)
    #     self.room_number_combo.setDisabled(True)
    #     self.cts_number_line.setDisabled(True)
    #
    #     self.operation = 'update'
    #     self.setWindowTitle("Bill Entry - Edit")

    def edit_record(self):
        self.make_form_editable()
        self.print_button.setDisabled(True)
        self.house_number_combo.setDisabled(True)
        self.tenant_name_combo.setDisabled(True)
        self.room_number_combo.setDisabled(True)
        self.cts_number_line.setDisabled(True)
        self.operation = 'update'
        self.setWindowTitle("Bill Entry - Edit")

    def delete_record(self):

        if self.bill_id is None:
            QMessageBox.warning(self, "Error", "Could not find the bill ID for row.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this bill?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success, message = database.delete_bill_by_id(self.bill_id)
            if success:
                # time.sleep(1)
                self.populate_table()
                self.clear_form()
                QMessageBox.information(self, "Success", "Successfully deleted the record.")
            else:
                QMessageBox.warning(self, "Error", f"Error deleting the record: {message}")
        else:
            print("Deletion cancelled.")

    def clear_form(self):
        self.make_form_editable()
        self.print_button.setDisabled(True)
        self.edit_button.setDisabled(True)
        self.delete_button.setDisabled(True)
        # self.rent_to_date.setReadOnly(True)
        self.house_number_combo.setCurrentIndex(0)
        self.tenant_name_combo.setCurrentIndex(0)
        self.room_number_combo.setCurrentIndex(0)

        # Clear line edits
        self.book_number_line.clear()
        self.bill_number_line.clear()
        self.purpose_line.clear()
        self.at_the_rate_of.clear()
        self.total_rupees_line.clear()
        self.extra_payment_line.setText(str(0))
        self.notes_text.clear()

        # Reset the dates to current date
        current_date = QDate.currentDate()
        self.bill_for_month_of.setDate(current_date)
        self.rent_from_date.setDate(current_date)
        self.received_date.setDate(current_date)
        self.agreement_date.setDate(current_date)

        # Update fields
        self.tenant_changed()
        self.room_changed()
        self.update_rent_to_date()
        self.update_total_months()
        self.update_total_rupees()

        self.operation = 'insert'
        self.purpose_line.setText("For Residence")
        self.bill_id = None
        self.setWindowTitle("Bill Entry - Add")
        self.is_alive_checkbox.setChecked(True)
        self.agreement_date.clear()

    def calculate_next_numbers(self):
        # Get the latest numbers from the database
        latest_book_number, latest_bill_number = database.get_latest_book_and_bill_numbers()

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
        bill_for_month_of = self.bill_for_month_of.date()
        self.rent_to_date.setDate(bill_for_month_of)

    def update_bill_for_month_of_date(self):
        rent_to_date = self.rent_to_date.date()
        self.bill_for_month_of.setDate(rent_to_date)

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
        at_the_rate_of_text = self.at_the_rate_of.text()
        total_months_text = self.total_months_line.text()

        try:
            # Convert the text to float values
            at_the_rate_of_text = float(at_the_rate_of_text)
            total_months = float(total_months_text)

            # Calculate the product
            total_rupees = at_the_rate_of_text * total_months

            # Update the total_rupees_line QLineEdit with the calculated value
            self.total_rupees_line.setText(str(total_rupees))
        except ValueError:
            # Handle the case where the input is not a valid float
            self.total_rupees_line.setText(str(0))

    def populate_houses_dropdown(self):
        houses = database.get_house_data()
        for house in houses:
            house_number, house_id = house[0], house[1]
            self.house_number_combo.addItem(house_number, house_id)

    def house_changed(self):
        if self.operation == 'print':
            return
        current_house_id = self.house_number_combo.currentData()
        rooms = database.get_rooms_data_by_house_id(current_house_id)
        self.tenant_name_combo.clear()
        for room in rooms:
            room_id = room[1]
            tenant_name, tenant_id = database.get_tenants_data_by_room_id(room_id)
            if tenant_name and tenant_id:
                self.tenant_name_combo.addItem(tenant_name, tenant_id)

    def tenant_changed(self):
        if self.operation == 'print':
            return
        current_tenant_id = self.tenant_name_combo.currentData()
        self.room_number_combo.clear()
        if current_tenant_id:
            room_name, room_id = database.get_room_data_by_tenant_id(current_tenant_id)
            self.room_number_combo.addItem(room_name, room_id)
            if self.operation == 'insert':
                last_bill_data = database.get_last_bill_data_by_tenant_id(current_tenant_id)
                if last_bill_data:
                    # TODO: MATCH THE NAMES BETWEEN DB AND INIT_UI. MAKE THE NAMES COMMON. FIX BELOW CODE ONCE DONE
                    set_data = {'RECEIVED_DATE': last_bill_data['received_date'].strftime('%Y-%m-%d'),
                                'RENT_FROM': last_bill_data['rent_from'], 'BOOK_NO': last_bill_data['book_number'],
                                'RENT_TO': last_bill_data['rent_to'],
                                'AT_THE_RATE_OF': last_bill_data['at_the_rate_of'],
                                'TOTAL_MONTHS': last_bill_data['total_months'],
                                'BILL_NO': last_bill_data['bill_number'],
                                'BILL_FOR_MONTH_OF': last_bill_data['bill_for_month_of'],
                                'TOTAL_AMOUNT': last_bill_data['total_rupees'],
                                'EXTRA_PAYMENT': last_bill_data['extra_payment'], 'NOTES': last_bill_data['notes'],
                                'PURPOSE_FOR': last_bill_data['purpose_for'],
                                'AGREEMENT_DATE': last_bill_data['agreement_date'].strftime('%Y-%m-%d') if
                                last_bill_data['agreement_date'] else ""}
                    self.set_data_to_form(set_data)
                else:
                    current_date = QDate.currentDate()
                    self.bill_for_month_of.setDate(current_date)
                    self.rent_from_date.setDate(current_date)
                    self.received_date.setDate(current_date)
                    self.agreement_date.setDate(current_date)
                    self.book_number_line.clear()
                    self.bill_number_line.clear()
                    self.purpose_line.clear()
                    self.at_the_rate_of.clear()
                    self.total_rupees_line.clear()
                    self.extra_payment_line.setText(str(0))
                    self.notes_text.clear()
                    self.update_rent_to_date()
                    self.update_total_months()
                    self.update_total_rupees()
                    self.is_alive_checkbox.setChecked(True)
                    self.agreement_date.clear()
        else:
            self.room_number_combo.clear()

    def room_changed(self):
        current_room_id = self.room_number_combo.currentData()
        if current_room_id:
            cts_number = database.get_cts_number_by_room_id(current_room_id)
            self.cts_number_line.setText(cts_number)
            self.cts_number_line.setReadOnly(True)
        else:
            self.cts_number_line.clear()

    def submit_data(self):
        mandatory_fields = [
            (self.book_number_line, "Book Number"),
            (self.bill_number_line, "Bill Number"),
            (self.house_number_combo, "House Number"),
            (self.room_number_combo, "Room Number"),
            (self.purpose_line, "Purpose For"),
            (self.at_the_rate_of, "@"),
            (self.extra_payment_line, "Extra Payment"),
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

        print("getting user data...")
        total_months = self.total_months_line.text()
        rent_from = self.rent_from_date.date().toString("MMM-yyyy")
        rent_to = self.rent_to_date.date().toString("MMM-yyyy")
        bill_for_month_of = self.bill_for_month_of.date().toString("MMM-yyyy")
        book_number = self.book_number_line.text()
        bill_number = self.bill_number_line.text()
        purpose_for = self.purpose_line.text()
        at_the_rate_of = self.at_the_rate_of.text()
        total_rupees = self.total_rupees_line.text()
        received_date = self.received_date.date().toString("yyyy-MM-dd")
        extra_payment = self.extra_payment_line.text()
        if self.is_alive_checkbox.isChecked():
            agreement_date = None
        else:
            agreement_date = self.agreement_date.date().toString("yyyy-MM-dd")

        notes = self.notes_text.text()
        current_tenant_id = self.tenant_name_combo.currentData()
        if self.operation == "insert":
            reply = QMessageBox.question(self, 'Add Bill',
                                         "Are you sure you want to Add this bill?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                status, message = database.insert_bill_entry(bill_for_month_of, book_number, bill_number, purpose_for,
                                                             rent_from,
                                                             rent_to,
                                                             at_the_rate_of, total_months, total_rupees, received_date,
                                                             extra_payment, agreement_date, notes, current_tenant_id)
                if status:
                    QMessageBox.information(self, "Success", "Bill Data Inserted successfully!")
                    self.clear_form()
                else:
                    QMessageBox.warning(self, "Error", str(message))

        else:
            status, message = database.update_bill_entry(self.bill_id, bill_for_month_of, book_number, bill_number,
                                                         purpose_for,
                                                         rent_from, rent_to, at_the_rate_of, total_months, total_rupees,
                                                         received_date, extra_payment, agreement_date, notes)
            if status:
                QMessageBox.information(self, "Success", "Bill Data Updated successfully!")
                # self.clear_form()
                self.make_form_readonly()
                self.print_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Error", str(message))

        self.populate_table()
        self.setWindowTitle("Bill Entry - Add")

    def validate_at_the_rate_of(self):
        input_text = self.at_the_rate_of.text()

        if input_text.isdigit() and int(input_text) > 0:
            return True

        return False

    def validate_total_months(self):
        return True if int(self.total_months_line.text()) > 0 else False

    def validate_rent_from_to_date(self):
        house_number = self.house_number_combo.currentText()
        room_number = self.room_number_combo.currentText()
        cts_number = self.cts_number_line.text()
        rent_from = self.rent_from_date.date().toString("MMM-yyyy")
        if self.operation == "insert":
            previous_rent_from_date, previous_rent_to_date = database.get_last_from_and_to_dates(house_number,
                                                                                                 room_number,
                                                                                                 cts_number,
                                                                                                 self.operation)

            if previous_rent_from_date and previous_rent_to_date:
                previous_rent_to = datetime.strptime(previous_rent_to_date, "%b-%Y")
                new_rent_from = datetime.strptime(rent_from, "%b-%Y")
                if previous_rent_to >= new_rent_from:
                    return False
        else:
            pass
            # previous_rent_from_date, previous_rent_to_date, next_rent_from_date, next_rent_to_date = get_adjacent_from_and_to_dates(
            #     house_number, room_number, cts_number)
            #
            # print(previous_rent_from_date, previous_rent_to_date, next_rent_from_date, next_rent_to_date)

        return True

    def print_data(self):
        tenant_name = database.get_tenant_name_by_bill_id(self.bill_id)
        tenant_name_first_set, tenant_name_second_set = split_string(tenant_name, 45)
        received_date_with_ordinal, received_month, received_year = get_date_month_year(
            self.received_date.date().toString("yyyy-MM-dd"))
        rent_from = convert_date_string(self.rent_from_date.date().toString("MMM-yyyy"))
        rent_to = convert_date_string(self.rent_to_date.date().toString("MMM-yyyy"))
        if rent_from == rent_to:
            rent_from_to = rent_from
        else:
            rent_from_to = rent_from + "      to      " + rent_to

        room_number_first_set, room_number_second_set = split_string(self.room_number_combo.currentText(), 21)

        data = {"bill_for_month_of": self.bill_for_month_of.date().toString("MMM-yyyy"),
                "book_number": self.book_number_line.text(),
                "bill_number": self.bill_number_line.text(),
                "purpose_for": self.purpose_line.text(),
                "cts_number": self.cts_number_line.text(),
                "house_number": self.house_number_combo.currentText(),
                "rent_from_to": rent_from_to,
                "total_rupees": self.total_rupees_line.text(),
                "total_paise": "00.",
                "@": "@",
                "per_month": "per month",
                "at_the_rate_of": "Rs. " + self.at_the_rate_of.text() + "/-",
                "received_date_with_ordinal": received_date_with_ordinal,
                "received_month": received_month,
                "received_year": received_year,
                "notes": self.notes_text.text()
                }

        bill_image = QImage(self.rr_bill_path)

        # Draw text onto the image
        painter = QPainter(bill_image)
        painter.begin(bill_image)
        font = QFont('Arial', 31)
        font.setWeight(QFont.Bold)
        painter.setFont(font)  # Choose a suitable font and size

        # Define positions for the text fields on the image (these will need to be adjusted)
        positions = {
            "bill_for_month_of": (600, 830),
            "book_number": (1165, 830),
            "bill_number": (1500, 830),
            "purpose_for": (230, 940),
            "cts_number": (1165, 940),
            "house_number": (1165, 1055),
            "rent_from_to": (747, 1475),
            "total_rupees": (1140, 1635),
            "total_paise": (1500, 1635),
            "@": (730, 1550),
            "at_the_rate_of": (675, 1605),
            "per_month": (675, 1650),
            "received_date_with_ordinal": (999, 1880),
            "received_month": (1266, 1880),
            "received_year": (1499, 1880),
            "notes": (390, 2470)}

        if tenant_name_second_set:
            data["tenant_name_first_set"] = tenant_name_first_set
            data["tenant_name_second_set"] = tenant_name_second_set
            positions["tenant_name_first_set"] = (378, 1305)
            positions["tenant_name_second_set"] = (378, 1355)
        else:
            data["tenant_name_first_set"] = tenant_name_first_set
            positions["tenant_name_first_set"] = (378, 1355)

        if room_number_second_set:
            data["room_number_first_set"] = room_number_first_set
            data["room_number_second_set"] = room_number_second_set
            positions["room_number_first_set"] = (560, 1000)
            positions["room_number_second_set"] = (560, 1055)
        else:
            data["room_number_first_set"] = room_number_first_set
            positions["room_number_first_set"] = (560, 1055)

        if not self.is_alive_checkbox.isChecked():
            agreement_date = self.agreement_date.date().toString("yyyy-MM-dd")
            agreement_date_with_ordinal, agreement_month, agreement_year = get_date_month_year(agreement_date)
            data["agreement_date_with_ordinal"] = agreement_date_with_ordinal
            data["agreement_month"] = agreement_month
            data["agreement_year"] = agreement_year
            positions["agreement_date_with_ordinal"] = (490, 2160)
            positions["agreement_month"] = (697, 2160)
            positions["agreement_year"] = (956, 2160)

        for key, value in data.items():
            x, y = positions[key]
            painter.drawText(x, y, value)

        # bill_image.save("output.png")

        printer = QPrinter(QPrinter.HighResolution)
        #        print_dialog = QPrintDialog(printer)
        #        if print_dialog.exec_() == QPrintDialog.Accepted:
        printer.setPageSize(QPrinter.PageSize.A5)
        printer.setColorMode(QPrinter.Color)
        printer.setFullPage(False)
        printer.setOutputFormat(QPrinter.NativeFormat)

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
            QMessageBox.warning(self, "Error", "Failed to start writing on bill.")

        # print(f"Printer name: {printer.printerName()}")
        # print(f"Page size: {printer.pageSize()}")
        # print(f"Page rect: {printer.pageRect()}")
        # print(f"Resolution: {printer.resolution()} DPI")
        # print(f"Color mode: {'Color' if printer.colorMode() == QPrinter.Color else 'Grayscale'}")
        # print(f"Is full page: {printer.fullPage()}")
        # print(f"Output format: {printer.outputFormat()}")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BillEntry()
    window.show()
    sys.exit(app.exec_())
