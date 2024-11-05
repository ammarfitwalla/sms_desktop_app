from PyQt5.QtWidgets import QApplication
from src.login import LoginApp
from src.bill import BillEntry

if __name__ == '__main__':
    app = QApplication([])

    login_window = LoginApp()

    if login_window.exec_() == LoginApp.Accepted:  # If login is successful
        window = BillEntry()
        window.show()
    app.exec_()
    

