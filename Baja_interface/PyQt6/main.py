from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox, QTextEdit, QLCDNumber
from pyqtgraph import PlotWidget, plot
from customSerial import customSerial


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.serial = customSerial()
        self.setWindowTitle("Data visualization")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        # self.setGeometry(100, 100, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        # self.lcd = QLCDNumber(10)

        self.labelVelocidade = QLabel()
        self.labelVelocidade.setStyleSheet('color: #ffd700')

        self.labelRPM = QLabel()
        self.labelRPM.setStyleSheet('color: #ffd700')

        self.labelGPS = QLabel()
        self.labelGPS.setStyleSheet('color: #ffd700')

        self.graphVelocidade = PlotWidget()

        self.graphRPM = PlotWidget()

        grid = QGridLayout()
        grid.addWidget(self.labelVelocidade, 0, 0)
        grid.addWidget(self.labelRPM, 0, 1)
        grid.addWidget(self.labelGPS, 0, 2)
        grid.addWidget(self.graphVelocidade, 1, 0)
        grid.addWidget(self.graphRPM, 1, 1)

        self.setLayout(grid)

    def serialVisualization(self):

        self.labelVelocidade.setText(self.serial.data)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        self.graphRPM.plot(hour, temperature)