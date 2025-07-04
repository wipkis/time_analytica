from PySide6.QtWidgets import QMainWindow, QStackedWidget

from recordmanager import RecordManager
from screen.analysis_screen import AnalysisScreen
from screen.inputscreen import InputScreen
from screen.mainscreen import MainScreen

CSV_PATH = "./res/202504.csv"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TimeAnalytica")
        self.setGeometry(100, 100, 1280, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_screen = MainScreen(
            to_analysis_screen=self.show_analysis_screen,
            to_input_screen=self.show_input_screen,
        )
        self.input_screen = InputScreen(
            record_manager=RecordManager(CSV_PATH), to_main_screen=self.show_main_screen
        )
        self.analysis_screen = AnalysisScreen(to_main_screen=self.show_main_screen)

        self.stack.addWidget(self.analysis_screen)
        self.stack.addWidget(self.input_screen)
        self.stack.addWidget(self.main_screen)

        self.stack.setCurrentWidget(self.main_screen)

    def show_analysis_screen(self):
        self.stack.setCurrentWidget(self.analysis_screen)

    def show_input_screen(self):
        self.stack.setCurrentWidget(self.input_screen)

    def show_main_screen(self):
        self.stack.setCurrentWidget(self.main_screen)
