from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QHBoxLayout, QComboBox, \
    QVBoxLayout, QLCDNumber
import sys
from customSerial import *
from analoggaugewidget import AnalogGaugeWidget


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

        # Cria uma grade de widgets
        grid = QGridLayout()
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

    def update_ports(self):  # Da refresh nas portas disponiveis
        self.serial.update_ports()
        self.clicked_com.clear()
        self.clicked_com.addItems(self.serial.portList)
        self.connect_check()

    def connect_check(self):  # Desativa o botao connect caso nao esteja escolhido
        if len(self.serial.portList) == 0:
            self.connect.setEnabled(False)
        else:
            self.connect.setEnabled(True)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.serial = customSerial()  # Chama a classe customSerial para a variavel "serial"

        self.setWindowTitle("Data visualization")  # Titulo
        self.setStyleSheet('background-color: #2c2c2c')  # CSS
        self.resize(1200, 700)
        css = 'color: #ffd700; font-size: 24px; font: Helvetica;'  # Padrao de estilo para a janela

        self.labelVelocidade = QLabel("Velocidade: ")  # Cria a label velocidade
        self.labelVelocidade.setStyleSheet(css)  # Aplica o padrao
        self.displayVeloc = QLCDNumber()

        self.labelRPM = QLabel("Rpm do motor: ")  # Cria a label rpm
        self.labelRPM.setStyleSheet(css)  # Aplica o padrao
        self.displayRPM = QLCDNumber()

        self.labelCVT = QLabel("Temperatura da CVT: ")
        self.labelCVT.setStyleSheet(css)
        self.displayCVT = QLCDNumber()
        self.displayCVT.setStyleSheet('color: #ffd700; background-color: blue')

        self.velocimetro = AnalogGaugeWidget()
        self.velocimetro.enableBarGraph = False
        self.velocimetro.units = "Km/h"
        self.velocimetro.minValue = 0
        self.velocimetro.maxValue = 100
        self.velocimetro.scalaCount = 10
        self.velocimetro.setCustomGaugeTheme(color2='#ffd700', color1="#FFF5BA")

        self.graphRPM = PlotWidget()  # Cria o grafico de velocidade
        self.graphRPM.setTitle("Plotting RPM")  # Define o titulo do grafico
        self.graphRPM.showGrid(x=True, y=True)  # Mostra os eixos no grafico

        self.graphCVT = PlotWidget()
        self.graphCVT.setTitle("Plotting CVT temperature")  # Define o titulo do grafico
        self.graphCVT.showGrid(x=True, y=True)  # Mostra os eixos no grafico

        self.grid = QGridLayout()
        self.grid.addWidget(self.labelVelocidade, 0, 0)
        self.grid.addWidget(self.labelRPM, 1, 0)
        self.grid.addWidget(self.labelCVT, 2, 0)
        self.grid.addWidget(self.displayVeloc, 0, 1)
        self.grid.addWidget(self.displayRPM, 1, 1)
        self.grid.addWidget(self.displayCVT, 2, 1)

        self.vbox2 = QVBoxLayout()
        self.vbox2.addLayout(self.grid)
        self.vbox2.addWidget(self.velocimetro)

        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.graphRPM)
        self.vbox3.addWidget(self.graphCVT)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        self.setLayout(self.hbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_connect = Window_Connect()
    window_connect.show()
    sys.exit(app.exec())
