from typing import Callable

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class AnalysisScreen(QWidget):

    def __init__(self, *, to_main_screen: Callable):
        super().__init__()

        layout = QVBoxLayout()
        self.button1 = QPushButton("뒤로")
        self.button1.clicked.connect(to_main_screen)

        layout.addWidget(self.button1)
        self.setLayout(layout)
