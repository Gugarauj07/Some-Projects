from threading import Event, Thread
import serial
import serial.tools.list_ports
import time
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from pyqtgraph import PlotWidget, plot
from main import MainWindow


class customSerial(QObject):
    # data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.main = MainWindow()
        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5

        self.arquivo = time.strftime("%d.%m.%Y_%Hh%M")
        path = Path("Arquivos_CSV")
        path.mkdir(parents=True, exist_ok=True)
        self.file = open(f"Arquivos_CSV/{self.arquivo}.csv", "w")
        # self.file.write(f"Start!\n")
        self.file.close()

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

    def connect_serial(self):
        try:
            self.serialPort.open()
        except:
            print("ERROR SERIAL")

        if self.serialPort.is_open:
            self.start_thread()

    def read_serial(self):
        while self.alive.isSet() and self.serialPort.is_open:
            self.data = self.serialPort.readline().decode("utf-8").strip()

            self.main.labelVelocidade.setText(self.data)

            if len(self.data) > 0:
                # self.data_available.emit(self.data)
                print(self.data)

                self.file = open(f"Arquivos_CSV/{self.arquivo}.csv", "r+")
                self.file.write(f"{float(self.data)}\n")
                # self.last_lines = self.file.readlines()
                self.file.close()
                # self.main.graphVelocidade.plot(self.array)

    def start_thread(self):
        self.thread = Thread(target=self.read_serial)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
