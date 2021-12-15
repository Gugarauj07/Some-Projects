# pip install pyserial
# pip install windows-curses
# pip install matplotlib
# pip install drawnow

import serial
import curses
from drawnow import *
import matplotlib

matplotlib.use("TkAgg")

# Inicia o curses
stdscr = curses.initscr()
stdscr.addstr("Distance: ")

# Inicia a comunicacao serial
ser = serial.Serial('COM4', 9600, timeout=1)  # Porta, Baudrate
ser.flushInput()

# Apaga o conteudo anterior do arquivo logger
with open("logger.csv", 'w') as f:
    pass


# Faz a funcao de datalogger
def datalogger():
    data = str(ser.readline().decode("utf-8")).strip()
    file = open("logger.csv", "a")
    file.write(f"{data}\n")
    file.close()


distancia = [0]
decoded_bytes = 0  # Define variaveis


# MatPlotLib
def makeFig():  # funcao que faz o plot
    plt.ion()  # Modo interativo para plotagem de graficos
    maximo = max(distancia) * 1.2  # Maximo para o y
    minimo = min(distancia) * 1.2 if min(distancia) < 0 else min(distancia) / 1.2  # Minimo para o y
    plt.ylim(minimo, maximo)  # Valores min e max de y
    plt.title('Live streaming sensor data')  # Titulo do grafico
    plt.grid(True)  # Fundo quadriculado
    distancia.append(decoded_bytes)  # Adiciona a informacao numa array para plotar
    plt.plot(distancia, 'r-', label='distance')
    plt.legend(loc='upper left')  # Escreve o label
    if len(distancia) > 25:
        distancia.pop(0)  # plota somente os ultimos 50 dados
    plt.pause(.001)
    plt.show()


# Inicia o loop para mostrar as informacoes
while True:  # Loop infinito
    while ser.inWaiting() == 0:  # Espera chegar informacoes no serial
        ser_bytes = ser.readline()  # Le a linha de texto do serial
        if ser_bytes != '':
            decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))  # Transforma em float
        stdscr.addstr(0, 10, str(decoded_bytes))  # Mostra a informacao no terminal
        stdscr.refresh()  # Atualiza o terminal
        datalogger()  # Executa o datalogging
        drawnow(makeFig)  # Executa o plot
