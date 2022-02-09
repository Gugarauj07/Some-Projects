from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QComboBox
import sys
from customSerial import *


class Window_Connect(QWidget):
    def __init__(self):
        super(Window_Connect, self).__init__()
        self.setWindowTitle("Serial Communication")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        self.setGeometry(500, 300, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        self.serial = customSerial()  # Chama a classe customSerial para a variavel "serial"

        self.refresh = QPushButton("Refresh")  # Cria o botao refresh
        self.refresh.setStyleSheet('background-color: #ffd700')  # CSS do botao refresh
        self.refresh.clicked.connect(self.update_ports)  # Conecta o refresh com o metodo update_ports

        self.connect = QPushButton("Connect")  # Cria o botao connect
        self.connect.setStyleSheet('background-color: #ffd700')  # CSS do botao connect
        self.connect.clicked.connect(self.connect_serial)  # Conecta o botao conecte com o metodo connect_serial

        label1 = QLabel("Available Port(s): ")  # Cria o label 1
        label1.setStyleSheet('color: #ffd700')  # CSS do label 1

        label2 = QLabel("Baude Rate: ")  # Cria o label 2
        label2.setStyleSheet('color: #ffd700')  # CSS do label 2

        self.clicked_com = QComboBox()  # Cria a caixa de opcoes de portas
        self.clicked_com.setStyleSheet('color: #ffd700')  # CSS da caixa de opcoes de portas
        self.connect_check()  # Chama a funcao connect_check
        self.update_ports()  # Atualiza as portas disponiveis

        self.clicked_bd = QComboBox()  # Cria a caixa de opcoes de baudrate
        self.clicked_bd.setStyleSheet('color: #ffd700')  # CSS da caixa de opcoes de baudrate
        self.clicked_bd.addItems(self.serial.baudratesDIC.keys())  # Adiciona itens a caixa de opcao
        self.clicked_bd.setCurrentText('9600')  # Seta o baudrate default

        grid = QGridLayout()  # Cria uma grade de widgets
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.connect, 1, 2)
        grid.addWidget(self.refresh, 0, 2)
        grid.addWidget(self.clicked_com, 0, 1)
        grid.addWidget(self.clicked_bd, 1, 1)
        self.setLayout(grid)

    def connect_serial(self):
        port = self.clicked_com.currentText()  # Guarda a porta escolhida
        baud = self.clicked_bd.currentText()  # Guarda o baudrate escolhido
        self.serial.serialPort.port = port
        self.serial.serialPort.baudrate = baud

        try:
            self.serial.serialPort.open()  # Tenta abrir a porta serial
        except:
            print("ERROR SERIAL")

        if self.serial.serialPort.is_open:
            self.serial.start_thread()  # Inicia o processo de threading

        self.main = MainWindow()  # Cria a nova janela "main"
        self.serial.update_window(self.main)
        self.main.show()
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


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.serial = customSerial()
        self.setWindowTitle("Data visualization")  # Titulo
        self.setWindowIcon(QIcon("qt.png"))  # Icone
        # self.setGeometry(100, 100, 500, 100)  # Tamanho
        self.setStyleSheet('background-color: #2c2c2c')  # CSS

        # self.lcd = QLCDNumber(10)

        self.labelVelocidade = QLabel("Velocidade: ")
        self.labelVelocidade.setStyleSheet('color: #ffd700')

        self.labelRPM = QLabel("RPM do motor: ")
        self.labelRPM.setStyleSheet('color: #ffd700')

        self.labelGPS = QLabel("GPS: ")
        self.labelGPS.setStyleSheet('color: #ffd700')

        self.graphVelocidade = PlotWidget()
        self.graphVelocidade.setTitle("Velocidade")
        self.graphVelocidade.setLabel('left', 'Km/h')
        self.graphVelocidade.showGrid(x=True, y=True)

        self.graphRPM = PlotWidget()
        self.graphVelocidade.setTitle("Rotação do motor")
        self.graphVelocidade.setLabel('left', 'RPM')
        self.graphVelocidade.showGrid(x=True, y=True)

        grid = QGridLayout()
        grid.addWidget(self.labelVelocidade, 0, 0)
        grid.addWidget(self.labelRPM, 0, 1)
        grid.addWidget(self.labelGPS, 0, 2)
        grid.addWidget(self.graphVelocidade, 1, 0)
        grid.addWidget(self.graphRPM, 1, 1)

        self.setLayout(grid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_connect = Window_Connect()
    window_connect.show()
    sys.exit(app.exec())