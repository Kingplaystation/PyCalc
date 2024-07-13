import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import math

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyCalc')
        self.setGeometry(300, 300, 300, 400)
        self.update_style()

        layout = QVBoxLayout()

        # Add settings button to top left corner
        top_layout = QHBoxLayout()
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon('settings_icon.png'))  # Make sure to have a settings icon image file
        self.settings_button.clicked.connect(self.show_settings_menu)
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
            '0', '.', '√', '='
        ]

        grid_layout = QHBoxLayout()
        for i in range(4):
            col_layout = QVBoxLayout()
            for j in range(5):
                index = i + 4*j
                if index < len(buttons):
                    button = QPushButton(buttons[index])
                    button.clicked.connect(self.on_click)
                    self.update_button_style(button)
                    col_layout.addWidget(button)
            grid_layout.addLayout(col_layout)

        layout.addLayout(grid_layout)

        self.setLayout(layout)

    def update_style(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #2D2D2D;")
        else:
            self.setStyleSheet("background-color: #F2F2F2;")

    def update_display_style(self):
        if self.dark_mode:
            self.display.setStyleSheet("background-color: #3D3D3D; color: #FFFFFF; font-size: 24px; padding: 10px; margin: 10px; border: none;")
        else:
            self.display.setStyleSheet("background-color: #FFFFFF; color: #000000; font-size: 24px; padding: 10px; margin: 10px; border: none;")

    def update_button_style(self, button):
        if self.dark_mode:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4D4D4D;
                    color: #FFFFFF;
                    font-size: 18px;
                    border: none;
                    padding: 15px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #5D5D5D;
                }
                QPushButton:pressed {
                    background-color: #6D6D6D;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #E6E6E6;
                    color: #000000;
                    font-size: 18px;
                    border: none;
                    padding: 15px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #D4D4D4;
                }
                QPushButton:pressed {
                    background-color: #BFBFBF;
                }
            """)

    def update_settings_button_style(self):
        if self.dark_mode:
            self.settings_button.setStyleSheet("""
                QPushButton {
                    background-color: #4D4D4D;
                    color: white;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #5D5D5D;
                }
                QPushButton:pressed {
                    background-color: #6D6D6D;
                }
            """)
        else:
            self.settings_button.setStyleSheet("""
                QPushButton {
                    background-color: #E6E6E6;
                    color: black;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #D4D4D4;
                }
                QPushButton:pressed {
                    background-color: #BFBFBF;
                }
            """)

    def on_click(self):
        button = self.sender()
        current_text = self.display.text()

        if button.text() == '=':
            try:
                # Replace '×' with '*' and '÷' with '/'
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
                result = -value
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif button.text() == '%':
            try:
                value = float(current_text)
                result = value / 100
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif button.text() == '√':
            try:
                value = float(current_text)
                result = math.sqrt(value)
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        else:
            self.display.setText(current_text + button.text())

    def show_settings_menu(self):
        menu = QMenu(self)
        if self.dark_mode:
            menu.setStyleSheet("QMenu { background-color: #4D4D4D; color: white; }")
        else:
            menu.setStyleSheet("QMenu { background-color: #E6E6E6; color: black; }")
        dark_mode_action = menu.addAction("Toggle Dark Mode")
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
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

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About PyCalc")
        about_box.setText("This is a simple calculator application created with PyQt5.\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.")
        if self.dark_mode:
            about_box.setStyleSheet("QMessageBox { background-color: #2D2D2D; color: white; }")
        else:
            about_box.setStyleSheet("QMessageBox { background-color: #F2F2F2; color: black; }")
        about_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
