from typing import Callable

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class MainScreen(QWidget):

    def __init__(self,*, to_analysis_screen: Callable, to_input_screen: Callable):
        super().__init__()

        layout = QVBoxLayout()
        self.button_input = QPushButton("입력")
        self.button_input.clicked.connect(to_input_screen)

        self.button_analysis = QPushButton("통계")
        self.button_analysis.clicked.connect(to_analysis_screen)

        layout.addWidget(self.button_input)
        layout.addWidget(self.button_analysis)
        self.setLayout(layout)
