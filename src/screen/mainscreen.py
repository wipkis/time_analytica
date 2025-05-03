from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainScreen(QWidget):
    main_window: QMainWindow

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.button_input = QPushButton("입력")
        self.button_input.clicked.connect(self.main_window.show_input_screen)

        self.button_analysis = QPushButton("통계")
        self.button_analysis.clicked.connect(self.main_window.show_analysis_screen)

        layout.addWidget(self.button_input)
        layout.addWidget(self.button_analysis)
        self.setLayout(layout)
