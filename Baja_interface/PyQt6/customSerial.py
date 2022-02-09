from threading import Event, Thread
import serial
import serial.tools.list_ports
import time
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from pyqtgraph import PlotWidget, plot, mkPen


class customSerial(QObject):
    data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.velocidadeArray = list()

        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5

        self.arquivo = time.strftime("%d.%m.%Y_%Hh%M")
        path = Path("Arquivos_CSV")
        path.mkdir(parents=True, exist_ok=True)
        # self.file = open(f"Arquivos_CSV/{self.arquivo}.csv", "w")

        self.baudratesDIC = {
            '9600': 9600,
            '19200': 19200,
            '38400': 38400,
            '57600': 57600,
            '115200': 115200
        }
        self.portList = []

        self.thread = None
        self.alive = Event()

    def update_ports(self):
        self.portList = [port.device for port in serial.tools.list_ports.comports()]
        print(self.portList)

    def read_serial(self):
        while self.alive.isSet() and self.serialPort.is_open:
            self.data = self.serialPort.readline().decode("utf-8").strip()

            if len(self.data) > 0:

                self.window.labelVelocidade.setText(f"Velocidade: {self.data} Km/h")

                self.velocidadeArray.append(float(self.data))

                pen = mkPen(width=2)
                self.window.graphVelocidade.plot(self.velocidadeArray, pen=pen)

                self.file = open(f"Arquivos_CSV/{self.arquivo}.csv", "a")
                self.file.write(f"{self.data}\n")
                self.file.close()

                # self.data_available.emit(self.data)
                print(self.data)

    def start_thread(self):
        self.thread = Thread(target=self.read_serial)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def update_window(self, window):
        self.window = window
