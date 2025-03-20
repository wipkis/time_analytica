
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class InputScreen(QWidget):
    main_window:QMainWindow
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

        self.text_list = []

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.undo_button)
        input_layout.addWidget(self.save_button)

        layout.addLayout(input_layout, 1)
        layout.addWidget(self.display_area, 2)

        self.setLayout(layout)

    def on_add_click(self):
        text = self.input_field.text().strip().replace(" ",",")
        if text:
            self.text_list.append(text)
            self.update_display()
            self.input_field.clear()

    def on_undo_click(self):
        if self.text_list:
            self.text_list.pop()
            self.update_display()

    def update_display(self):
        self.display_area.clear()
        self.display_area.append("\n".join(self.text_list))

    def on_save_click(self):
        print("\n".join(self.text_list))
        self.main_window.show_main_screen()
