import re


def remover_caracteres(cnpj):
    return re.sub(r'[^0-9]', '', cnpj)


cnpj_testado = remover_caracteres(input("Digite um cnpj: "))
cnpjArray = list(cnpj_testado[:-2])
lista1 = ['5', '4', '3', '2', '9', '8', '7', '6', '5', '4', '3', '2']
soma1 = sum([int(x) * int(y) for x, y in zip(cnpjArray, lista1)])
digito1 = 11 - (soma1 % 11)
if digito1 > 9:
    digito1 = 0
cnpjArray.append(digito1)

lista2 = ['6', '5', '4', '3', '2', '9', '8', '7', '6', '5', '4', '3', '2']
soma2 = sum([int(x) * int(y) for x, y in zip(cnpjArray, lista2)])
digito2 = 11 - (soma2 % 11)
if digito2 > 9:
    digito2 = 0
cnpjArray.append(digito2)

novo_cnpj = "".join([str(num) for num in cnpjArray])

if cnpj_testado == novo_cnpj:
    print("Valido")
else:
    print("Invalido")