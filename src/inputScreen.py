import re

import pandas as pd
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

from util import diff_minutes

CSV_PATH = "./res/202504.csv"
RECODE_REGREX = r"^(?:[01][0-9]|2[0-3])[0-5][0-9] [^\s]+(?: [^\s]+)?(?: [^\s]+)?$"


class InputScreen(QWidget):
    main_window: QMainWindow

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QHBoxLayout()

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
        self.recode_list = pd.read_csv(CSV_PATH, index_col=False, dtype=str)
        self.display_area.setText(self.recode_list.to_csv(sep="\t", index=False))

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.undo_button)
        input_layout.addWidget(self.save_button)

        layout.addLayout(input_layout, 1)
        layout.addWidget(self.display_area, 2)

        self.setLayout(layout)

    def on_undo_click(self):
        if not self.recode_list.empty:
            self.recode_list = self.recode_list.iloc[:-1]
            self.update_display()

    def update_display(self):
        self.display_area.clear()
        self.display_area.setText(self.recode_list.to_csv(sep="\t", index=False))

    def on_save_click(self):
        self.recode_list.to_csv(CSV_PATH, index=False)
        self.main_window.show_main_screen()

    def on_add_click(self):
        text = self.input_field.text().strip()
        if re.match(RECODE_REGREX, text) is None:
            QMessageBox.warning(self, "형식 오류", "HHMM 행동 카테고리(옵션)")
            self.input_field.clear()
            return

        prev = self.recode_list.iloc[-1]
        fields = text.split(" ")
        new_row = pd.DataFrame([self.build_row(prev["date"], fields)])
        self.update_last_duration(fields[0])

        self.recode_list = pd.concat([self.recode_list, new_row], ignore_index=True)
        self.update_display()
        self.input_field.clear()

    def build_row(self, prev_date, fields):
        return {
            "date": prev_date,
            "time": fields[0],
            "duration": 0,
            "act": fields[1],
            **({"category_1": fields[2]} if len(fields) > 2 else {}),
            **({"category_2": fields[3]} if len(fields) > 3 else {}),
        }

    def update_last_duration(self, new_time):
        if len(self.recode_list) >= 1:
            last_idx = self.recode_list.index[-1]
            prev_time = self.recode_list.at[last_idx, "time"]
            self.recode_list.at[last_idx, "duration"] = diff_minutes(
                prev_time, new_time
            )
