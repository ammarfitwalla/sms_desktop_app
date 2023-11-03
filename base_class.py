from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont

class BaseWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.adjust_window_size()
        self.set_default_font()

    def adjust_window_size(self):
        current_size = self.size()
        new_width = int(current_size.width() * 2)
        new_height = int(current_size.height() * 2)
        self.resize(new_width, new_height)

    def set_default_font(self):
        font = QFont()
        font.setPointSize(12)  # You can adjust this value as needed
        self.setFont(font)
