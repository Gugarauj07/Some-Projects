from threading import Event, Thread
import serial
import serial.tools.list_ports
from time import strftime
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal
from pyqtgraph import PlotWidget, plot, mkPen
import csv
import pandas as pd


class customSerial(QObject):
    data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.velocidadeArray = list()

        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5

        self.arquivo = strftime("%d.%m.%Y_%Hh%M")
        path = Path("Arquivos_CSV")
        path.mkdir(parents=True, exist_ok=True)

        with open(f"Arquivos_CSV/{self.arquivo}.csv", 'w', newline='') as f:
            self.thewriter = csv.writer(f)
            self.thewriter.writerow(['velocidade', 'rpm'])

        self.baudratesDIC = {
            '9600': 9600,
            '19200': 19200,
            '38400': 38400,
            '57600': 57600,
            '115200': 115200
        }
        self.portList = list()

        self.thread = None
        self.alive = Event()

    def update_ports(self):
        self.portList = [port.device for port in serial.tools.list_ports.comports()]
        print(self.portList)

    def read_serial(self):
        while self.alive.isSet() and self.serialPort.is_open:

            self.data = self.serialPort.readline().decode("utf-8").strip()

            if len(self.data) > 0:

                with open(f"Arquivos_CSV/{self.arquivo}.csv", 'a+', newline='') as f:
                    self.thewriter = csv.writer(f)
                    self.thewriter.writerow([self.data])

                df = pd.read_csv(f"Arquivos_CSV/{self.arquivo}.csv").tail(100)
                self.velocidadeArray = list(df["velocidade"])

                self.window.labelVelocidade.setText(f"Velocidade: {self.data} Km/h")

                self.pen = mkPen(width=2)
                self.window.graphVelocidade.clear()
                self.window.graphVelocidade.plot(self.velocidadeArray, pen=self.pen)

    def start_thread(self):
        self.thread = Thread(target=self.read_serial)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def update_window(self, window):
        self.window = window
