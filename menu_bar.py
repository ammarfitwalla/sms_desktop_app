from PyQt5.QtWidgets import QMenuBar, QAction


class CustomMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent  # Store the parent, can be used for signal-slot connections

        master_menu = QAction('Master', self)
        master_menu.triggered.connect(self.parent.display_master)  # Connect to the parent's method
        self.addAction(master_menu)

        bill_menu = QAction('Bill', self)
        bill_menu.triggered.connect(self.parent.display_bill)  # Connect to the parent's method
        self.addAction(bill_menu)
