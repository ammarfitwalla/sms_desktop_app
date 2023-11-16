from PyQt5.QtWidgets import QApplication
from login import LoginApp
from master_entry import MasterEntry

if __name__ == '__main__':
    app = QApplication([])

    login_window = LoginApp()
    master_entry_window = MasterEntry()

    if login_window.exec_() == LoginApp.Accepted:  # If login is successful
        master_entry_window.show()

    app.exec_()
    

