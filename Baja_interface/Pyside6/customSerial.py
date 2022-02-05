from threading import Event, Thread
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
# from main import MainWindow


class customSerial(QObject):
    data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5

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
            data = self.serialPort.readline().decode("utf-8").split()
            if len(data) > 0:
                self.data_available.emit(data[0])
                print(data)

    def start_thread(self):
        self.thread = Thread(target=self.read_serial)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
