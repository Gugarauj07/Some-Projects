import sys
from tkinter import *
import serial.tools.list_ports
import threading
import signal
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use("ggplot")


def signal_handler(signum, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


# Inicia a interface tkinter
def connect_menu_init():
    global root, connect_btn, refresh_btn, fig, ax, figure  # Define variaveis como globais
    root = Tk()
    root.title("Serial communication")  # Titulo da interface
    root.config(bg="#fafafa")  # Background da interface

    port_lable = Label(root, text="Available Port(s): ", bg="white")  # Configura o label das portas
    port_lable.grid(column=1, row=2, pady=20, padx=10)

    port_bd = Label(root, text="Baude Rate: ", bg="white")  # Configura o label do Baudrate
    port_bd.grid(column=1, row=3, pady=20, padx=10)

    refresh_btn = Button(root, text="Refresh", height=2,  # Configura o botao refresh
                         width=10, command=update_coms)
    refresh_btn.grid(column=3, row=2)

    connect_btn = Button(root, text="Connect", height=2,  # Configura o botao connect
                         width=10, state="disabled", command=connexion)
    connect_btn.grid(column=3, row=3)

    figure = Figure(figsize=(5, 4), dpi=100)
    # fig = plt.figure()
    ax = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=2, row=6)

    # # toolbar = NavigationToolbar2Tk(canvas, root)
    # # toolbar.update()
    # # canvas.get_tk_widget().grid(column=2, row=6)

    baud_select()
    update_coms()


def newWindow():
    pass


# Checa se a porta e o baudrate estao prontos
def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"


# Seleciona o baudrate desejado
def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["9600",
           "115200"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)


# Mostra as opcoes de portas COM disponiveis
def update_coms():
    global clicked_com, drop_COM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        drop_COM.destroy()
    except:
        pass
    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_COM = OptionMenu(root, clicked_com, *coms, command=connect_check)
    drop_COM.config(width=20)
    drop_COM.grid(column=2, row=2, padx=50)
    connect_check(0)


# Leitura do serial
def readSerial():
    print("thread start")
    global serialData, sensor
    while serialData:
        data = ser.readline()  # Le o serial
        if len(data) > 0:
            try:
                sensor = float(data.decode('utf8'))
                t2 = threading.Thread(target=datalogger())  # Executa o threading para o uso do datalogger em loop
                t2.deamon = True
                t2.start()
                Label(root, text=f"Distance: {sensor} cm", bg="white", font=("Verdana", "25")).grid(
                    column=2, row=5)
            except:
                pass


# Faz a conexao dos botoes com o serial
def connexion():
    global ser, serialData
    if connect_btn["text"] in "Disconnect":
        serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"

    else:
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_COM["state"] = "disable"
        port = clicked_com.get()
        baud = clicked_bd.get()
        try:
            ser = serial.Serial(port, baud, timeout=1)
        except:
            pass
        t1 = threading.Thread(target=readSerial)
        t1.deamon = True
        t1.start()


# Fecha a janela sem bugar o programa
def close_window():
    global root, serialData
    serialData = False
    root.destroy()


arquivo = time.strftime("%d.%m.%Y_%Hh%M")


# Faz a funcao de datalogger
def datalogger():
    data_decoded = str(ser.readline().decode("utf-8")).strip()
    file = open(f"{arquivo}.csv", "a")
    file.write(f"{data_decoded}\n")
    file.close()


def matplot(i):
    pass


connect_menu_init()
ani = animation.FuncAnimation(figure, matplot, interval=1000)
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()