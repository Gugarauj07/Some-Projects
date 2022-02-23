import re
import random


def calcula_digito(cnpj, digito):
    cnpjArray = [int(x) for x in cnpj]
    regressivos = ['6', '5', '4', '3', '2', '9', '8', '7', '6', '5', '4', '3', '2']
    if digito == 1:
        soma = sum([int(x) * int(y) for x, y in zip(cnpjArray, regressivos[1:])])
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        cnpjArray.append(digito1)
        return "".join([str(num) for num in cnpjArray])

    elif digito == 2:
        soma = sum([int(x) * int(y) for x, y in zip(cnpjArray, regressivos)])
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        cnpjArray.append(digito2)
        return "".join([str(num) for num in cnpjArray])


def gera():
    novo_cnpj = ""
    for c in range(8):
        novo_cnpj += str(random.randint(0, 9))
    novo_cnpj += '0001'

    digito1 = calcula_digito(novo_cnpj, digito=1)
    cnpj = calcula_digito(digito1, digito=2)

    formatado = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    return formatado


print(gera())
