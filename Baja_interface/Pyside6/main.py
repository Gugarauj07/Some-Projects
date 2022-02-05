from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox, QTextEdit, QLCDNumber
from customSerial import customSerial


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.serial = customSerial()
        self.setWindowTitle("Data visualization")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        # self.setGeometry(100, 100, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        velocidade = QLCDNumber()
        velocidade.display(data)

        grid = QGridLayout()
        grid.addWidget(velocidade, 0, 0)
        self.setLayout(grid)