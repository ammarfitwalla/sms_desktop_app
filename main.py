from PyQt5.QtWidgets import QApplication
from login import LoginApp
from master_entry import MasterEntry
from bill import BillEntry

if __name__ == '__main__':
    app = QApplication([])

    login_window = LoginApp()

    if login_window.exec_() == LoginApp.Accepted:  # If login is successful
        BillEntry()

    app.exec_()
    

