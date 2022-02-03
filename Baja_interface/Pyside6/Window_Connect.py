# import serial
import sys
import serial.tools.list_ports
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox


class Window_Connect(QWidget):
    def __init__(self):
        super(Window_Connect, self).__init__()
        self.setWindowTitle("Serial Communication")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        self.setGeometry(500, 300, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        # def create_widgets(self):
        refresh = QPushButton("Refresh")
        refresh.setStyleSheet('background-color: #ffd700')
        # refresh.setGeometry(500, 20, 80, 30)
        refresh.clicked.connect(self.clicked_refresh)

        global connect
        connect = QPushButton("Connect")
        connect.setStyleSheet('background-color: #ffd700')
        connect.clicked.connect(self.clicked_connect)

        label1 = QLabel("Available Port(s): ")
        label1.setStyleSheet('color: #ffd700')
        # label.setGeometry(20, 20, 100, 30)
        # label.setFont(QFont="")  # Fonte

        label2 = QLabel("Baude Rate: ")
        label2.setStyleSheet('color: #ffd700')

        global clicked_com, ports, coms
        clicked_com = QComboBox()
        clicked_com.setStyleSheet('color: #ffd700')
        self.value_com = clicked_com.currentText()
        clicked_bd = QComboBox()
        bds = ["9600", "115200"]
        for i in bds:
            clicked_bd.addItem(i)
        clicked_bd.setStyleSheet('color: #ffd700')
        self.value_bds = clicked_bd.currentText()

        grid = QGridLayout()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(connect, 1, 2)
        grid.addWidget(refresh, 0, 2)
        grid.addWidget(clicked_com, 0, 1)
        grid.addWidget(clicked_bd, 1, 1)
        self.setLayout(grid)

    # def connect_check(self, args):
    #     if "-" == self.value_com:
    #         connect.setEnabled(False)
    #     else:
    #         connect.setEnabled(True)

    def clicked_refresh(self):
        ports = serial.tools.list_ports.comports()
        coms = [com[0] for com in ports]
        for c in coms:
            clicked_com.addItem(c)

    def clicked_connect(self):
        # ser = serial.Serial(self.value_com, self.value_bds, timeout=1)
        self.w = MainWindow()
        self.w.show()
        self.hide()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Data visualization")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        # self.setGeometry(100, 100, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window_Connect()
    window.show()
    sys.exit(app.exec())
