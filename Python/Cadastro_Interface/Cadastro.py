from PyQt6 import QtCore, QtGui, QtWidgets
import pymysql.cursors
from contextlib import contextmanager
from Listagem import Ui_SecondWindow


@contextmanager
def conecta():
    conexao = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='password',
        db='cadastro',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        yield conexao
    finally:
        conexao.close()


class Ui_MainWindow(object):

    def Cadastrar(self):
        self.nome = self.lineEdit.text()
        self.email = self.lineEdit_2.text()
        self.telefone = self.lineEdit_3.text()

        print(self.nome, self.email, self.telefone)

        with conecta() as conexao:
            with conexao.cursor() as cursor:
                comando_SQL = "INSERT INTO register (nome, email, telefone) VALUES (%s,%s,%s)"
                cursor.execute(comando_SQL, (str(self.nome), str(self.email), str(self.telefone)))
                conexao.commit()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")

    def Listar(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)
        self.window.show()

        with conecta() as conexao:
            with conexao.cursor() as cursor:
                comando_SQL = "SELECT * FROM register"
                cursor.execute(comando_SQL)
                dados_lidos = cursor.fetchall()

                for k, v in dados_lidos[0].items():
                    print(k, v)

        self.ui.SecondWindow.setRowCount(len(dados_lidos))
        self.ui.SecondWindow.setColumnCount(4)

        try:
            for i in range(0, len(dados_lidos)):

                 self.ui.SecondWindow.setItem(i, 0, QtWidgets.QTableWidgetItem(str(dados_lidos[i]['id'])))
                 self.ui.SecondWindow.setItem(i, 1, QtWidgets.QTableWidgetItem(str(dados_lidos[i]['nome'])))
                 self.ui.SecondWindow.setItem(i, 2, QtWidgets.QTableWidgetItem(str(dados_lidos[i]['email'])))
                 self.ui.SecondWindow.setItem(i, 3, QtWidgets.QTableWidgetItem(str(dados_lidos[i]['telefone'])))
        except:
            pass

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(309, 275)
        MainWindow.setStyleSheet("background-color: rgb(44, 44, 44);\n"
                                 "color: rgb(85, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 291, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 5, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 4, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("background-color: rgb(85, 170, 255);\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(85, 170, 255);\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 309, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # FUNCTIONS
        self.pushButton.clicked.connect(self.Cadastrar)
        self.pushButton_2.clicked.connect(self.Listar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Área para Cadastro"))
        self.label_4.setText(_translate("MainWindow", "Telefone: "))
        self.label_3.setText(_translate("MainWindow", "Email: "))
        self.label_2.setText(_translate("MainWindow", "Nome: "))
        self.pushButton.setText(_translate("MainWindow", "CADASTRAR"))
        self.pushButton_2.setText(_translate("MainWindow", "LISTAR "))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
