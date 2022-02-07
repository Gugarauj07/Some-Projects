from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox
import sys
from main import *


class Window_Connect(QWidget):
    def __init__(self):
        super(Window_Connect, self).__init__()
        self.serial = customSerial()
        self.setWindowTitle("Serial Communication")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        self.setGeometry(500, 300, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        self.refresh = QPushButton("Refresh")
        self.refresh.setStyleSheet('background-color: #ffd700')
        self.refresh.clicked.connect(self.update_ports)

        self.connect = QPushButton("Connect")
        self.connect.setStyleSheet('background-color: #ffd700')
        self.connect.clicked.connect(self.connect_serial)

        label1 = QLabel("Available Port(s): ")
        label1.setStyleSheet('color: #ffd700')
        # label.setGeometry(20, 20, 100, 30)
        # label.setFont(QFont="")  # Fonte

        label2 = QLabel("Baude Rate: ")
        label2.setStyleSheet('color: #ffd700')

        self.clicked_com = QComboBox()
        self.clicked_com.setStyleSheet('color: #ffd700')
        self.connect_check()

        self.clicked_bd = QComboBox()
        self.clicked_bd.setStyleSheet('color: #ffd700')

        self.clicked_bd.addItems(self.serial.baudratesDIC.keys())
        self.clicked_bd.setCurrentText('9600')
        self.update_ports()

        grid = QGridLayout()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.connect, 1, 2)
        grid.addWidget(self.refresh, 0, 2)
        grid.addWidget(self.clicked_com, 0, 1)
        grid.addWidget(self.clicked_bd, 1, 1)
        self.setLayout(grid)

    def connect_serial(self):
        # if self.connect.isChecked():
        port = self.clicked_com.currentText()
        baud = self.clicked_bd.currentText()
        self.serial.serialPort.port = port
        self.serial.serialPort.baudrate = baud
        self.serial.connect_serial()

        self.window = MainWindow()
        self.window.show()
        self.hide()

    def update_ports(self):
        self.serial.update_ports()
        self.clicked_com.clear()
        self.clicked_com.addItems(self.serial.portList)
        self.connect_check()

    def connect_check(self):
        if len(self.serial.portList) == 0:
            self.connect.setEnabled(False)
        else:
            self.connect.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window_Connect()
    window.show()
    sys.exit(app.exec())
