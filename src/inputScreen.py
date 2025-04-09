import re

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from recordManager import RecordManager

RECODE_REGREX = r"^(?:[01][0-9]|2[0-3])[0-5][0-9] [^\s]+(?: [^\s]+)?(?: [^\s]+)?$"


class InputScreen(QWidget):
    TIME_INPUT_REGEX = (
        r"^(?:[01][0-9]|2[0-3])[0-5][0-9] [^\s]+(?: [^\s]+)?(?: [^\s]+)?$"
    )

    def __init__(self, main_window: QMainWindow, recode_manager: RecordManager):
        super().__init__()
        self.main_window = main_window
        self.recode_manager = recode_manager

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("여기에 입력하세요")
        self.input_field.returnPressed.connect(self.on_add_click)

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.on_add_click)

        self.undo_button = QPushButton("되돌리기")
        self.undo_button.clicked.connect(self.on_undo_click)

        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.on_save_click)

        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        self.display_area.setStyleSheet("border: 1px solid black; padding: 1px;")

        self.update_display()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.undo_button)
        input_layout.addWidget(self.save_button)

        layout = QHBoxLayout()
        layout.addLayout(input_layout, 1)
        layout.addWidget(self.display_area, 2)

        self.setLayout(layout)

    def on_add_click(self):
        text = self.input_field.text().strip()
        if not re.match(self.TIME_INPUT_REGEX, text):
            QMessageBox.warning(self, "형식 오류", "HHMM 행동 카테고리(옵션)")
            self.input_field.clear()
            return

        fields = text.split(" ")
        self.recode_manager.add_row(fields)
        self.update_display()
        self.input_field.clear()

    def on_undo_click(self):
        self.recode_manager.undo()
        self.update_display()

    def on_save_click(self):
        self.recode_manager.save()
        self.main_window.show_main_screen()

    def update_display(self):
        self.display_area.setText(self.recode_manager.to_string())
