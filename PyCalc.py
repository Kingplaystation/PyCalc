import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import math

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.square_buttons = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyCalc')
        self.setGeometry(300, 300, 300, 400)
        self.update_style()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 10)
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon('settings_icon.png'))
        self.settings_button.clicked.connect(self.show_settings_menu)
        self.settings_button.setFixedSize(40, 40)
        self.update_settings_button_style()
        top_layout.addWidget(self.settings_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.update_display_style()
        layout.addWidget(self.display)

        buttons = [
            'C', '±', '%', '÷', 
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '√', '=',
            '⌫'
        ]

        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(5)
        for i in range(4):
            col_layout = QVBoxLayout()
            col_layout.setSpacing(5)
            for j in range(5):
                index = i + 4*j
                if index < len(buttons):
                    button = QPushButton(buttons[index])
                    button.clicked.connect(self.on_click)
                    button.setFixedSize(60, 60)
                    self.update_button_style(button)
                    col_layout.addWidget(button)
            grid_layout.addLayout(col_layout)

        backspace_button = QPushButton('⌫')
        backspace_button.clicked.connect(self.on_click)
        backspace_button.setFixedSize(60, 60)
        self.update_button_style(backspace_button)
        grid_layout.addWidget(backspace_button)

        layout.addLayout(grid_layout)

        self.setLayout(layout)

    def update_style(self):
        self.setStyleSheet(f"background-color: {'#2D2D2D' if self.dark_mode else '#F2F2F2'};")

    def update_display_style(self):
        self.display.setStyleSheet(f"""
            background-color: {'#3D3D3D' if self.dark_mode else '#FFFFFF'};
            color: {'#FFFFFF' if self.dark_mode else '#000000'};
            font-size: 24px;
            padding: 10px;
            margin-bottom: 10px;
            border: none;
            border-radius: 5px;
        """)

    def update_button_style(self, button):
        border_radius = "5px" if self.square_buttons else "30px"
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#4D4D4D' if self.dark_mode else '#E6E6E6'};
                color: {'#FFFFFF' if self.dark_mode else '#000000'};
                font-size: 18px;
                border: none;
                border-radius: {border_radius};
            }}
            QPushButton:hover {{
                background-color: {'#5D5D5D' if self.dark_mode else '#D4D4D4'};
            }}
            QPushButton:pressed {{
                background-color: {'#6D6D6D' if self.dark_mode else '#BFBFBF'};
            }}
        """)

    def update_settings_button_style(self):
        self.settings_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#4D4D4D' if self.dark_mode else '#E6E6E6'};
                color: {'white' if self.dark_mode else 'black'};
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: {'#5D5D5D' if self.dark_mode else '#D4D4D4'};
            }}
            QPushButton:pressed {{
                background-color: {'#6D6D6D' if self.dark_mode else '#BFBFBF'};
            }}
        """)

    def on_click(self):
        button = self.sender()
        current_text = self.display.text()

        if button.text() == '=':
            try:
                expression = current_text.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif button.text() == 'C':
            self.display.clear()
        elif button.text() == '±':
            try:
                value = float(current_text)
                self.display.setText(str(-value))
            except:
                self.display.setText('Error')
        elif button.text() == '%':
            try:
                value = float(current_text)
                self.display.setText(str(value / 100))
            except:
                self.display.setText('Error')
        elif button.text() == '√':
            try:
                value = float(current_text)
                self.display.setText(str(math.sqrt(value)))
            except:
                self.display.setText('Error')
        elif button.text() == '⌫':
            self.display.setText(current_text[:-1])
        else:
            self.display.setText(current_text + button.text())

    def show_settings_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(f"QMenu {{ background-color: {'#4D4D4D' if self.dark_mode else '#E6E6E6'}; color: {'white' if self.dark_mode else 'black'}; }}")
        dark_mode_action = menu.addAction("Toggle Dark Mode")
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        square_buttons_action = menu.addAction("Toggle Square Buttons")
        square_buttons_action.triggered.connect(self.toggle_square_buttons)
        about_action = menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_style()
        self.update_display_style()
        self.update_settings_button_style()
        for child in self.findChildren(QPushButton):
            if child != self.settings_button:
                self.update_button_style(child)

    def toggle_square_buttons(self):
        self.square_buttons = not self.square_buttons
        for child in self.findChildren(QPushButton):
            if child != self.settings_button:
                self.update_button_style(child)

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About PyCalc")
        about_box.setText("This is a simple calculator application created with PyQt5.\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.")
        about_box.setStyleSheet(f"QMessageBox {{ background-color: {'#2D2D2D' if self.dark_mode else '#F2F2F2'}; color: {'white' if self.dark_mode else 'black'}; }}")
        about_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
