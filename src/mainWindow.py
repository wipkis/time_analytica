
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from inputScreen import InputScreen
from mainScreen import MainScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TimeAnalytica")
        self.setGeometry(100, 100, 1280, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_screen = MainScreen(self)
        self.input_screen = InputScreen(self)

        self.stack.addWidget(self.main_screen)
        self.stack.addWidget(self.input_screen)

        self.stack.setCurrentWidget(self.main_screen)

    def show_input_screen(self):
        self.stack.setCurrentWidget(self.input_screen)

    def show_main_screen(self):
        self.stack.setCurrentWidget(self.main_screen)
