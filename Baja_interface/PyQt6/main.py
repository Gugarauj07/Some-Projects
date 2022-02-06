from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox, QTextEdit, QLCDNumber


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Data visualization")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        # self.setGeometry(100, 100, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        self.lcd = QLCDNumber()
        self.label = QLabel('10')
        self.label.setStyleSheet('color: red')

        grid = QGridLayout()
        grid.addWidget(self.lcd, 0, 0)
        grid.addWidget(self.label, 0, 1)
        self.setLayout(grid)
