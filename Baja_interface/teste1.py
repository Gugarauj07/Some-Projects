###################################################################################################
# Step 1 : Setup initial basic graphics
# Step 2: Update available COMs & Baude rate
# Step 3: Serial connection setup
# Step 4: Dynamic GUI update
# Step 5: Testing & Debugging
###################################################################################################

from tkinter import *
import serial.tools.list_ports
import threading
import signal


def signal_handler(signum, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


# Inicia a interface tkinter
def connect_menu_init():
    global root, connect_btn, refresh_btn, entry_arquivo, arquivo
    root = Tk()
    root.title("Serial communication")
    root.geometry("500x500")
    root.config(bg="white")

    port_lable = Label(root, text="Available Port(s): ", bg="white")
    port_lable.grid(column=1, row=2, pady=20, padx=10)

    port_bd = Label(root, text="Baude Rate: ", bg="white")
    port_bd.grid(column=1, row=3, pady=20, padx=10)

    refresh_btn = Button(root, text="Refresh", height=2,
                         width=10, command=update_coms)
    refresh_btn.grid(column=3, row=2)

    connect_btn = Button(root, text="Connect", height=2,
                         width=10, state="disabled", command=lambda: [connexion(), datalogger()])
    connect_btn.grid(column=3, row=3)

    arquivo_label = Label(root, text="File logger name: ", bg="white")
    arquivo_label.grid(column=1, row=4, pady=20, padx=10)

    entry_arquivo = Entry(root, bg="light grey", bd=5)
    entry_arquivo.config(width=25)
    entry_arquivo.grid(column=2, row=4, padx=50)

    submit_btn = Button(root, text="Submit", height=2,
                         width=10, state="active", command=get_file)
    submit_btn.grid(column=3, row=4)

    baud_select()
    update_coms()


def get_file():
    global arquivo
    arquivo = entry_arquivo.get()
    # Apaga o conteudo anterior do arquivo logger
    # with open(arquivo, 'w') as f:
    #     pass


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


def readSerial():
    print("thread start")
    global serialData, sensor
    while serialData:
        data = ser.readline()
        if len(data) > 0:
            try:
                sensor = int(data.decode('utf8'))
                # data_sensor = int(data.decode('utf8'))
                # print(sensor)
                # t2 = threading.Thread(target=readSerial)
                # t2.deamon = True
                # t2.start()
                # disp1 = Label(root, text=sensor).place(x=100, y=200)
                distance_label = Label(root, text=f"Distance: {sensor} cm", bg="white", font=("Verdana", "25")).grid(
                    column=2, row=5)
            except:
                pass


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


# Faz a funcao de datalogger
def datalogger():
    data = str(ser.readline().decode("utf-8")).strip()
    file = open(arquivo, "a")
    file.write(f"{data}\n")
    file.close()


def close_window():
    global root, serialData
    serialData = False
    root.destroy()


connect_menu_init()
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
