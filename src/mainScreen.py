
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainScreen(QWidget):
    main_window:QMainWindow
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.button1 = QPushButton("입력")
        self.button1.clicked.connect(self.main_window.show_input_screen)

        layout.addWidget(self.button1)
        self.setLayout(layout)
