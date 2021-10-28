tabela = {'100': 110.88, '150': 129.38, '250': 137.00, '310': 148.32, '500': 199.24, '750': 286.66, '1000': 287.63,
          '1500': 748.55, '2000': 735.26, '3000': 2009.9, '5000': 3649.98}
contador = valor_total = 0

print(f"{'TABELA CAIXAS':^52}")
print("-" * 58)
print(f"{'TAMANHO DE UMA CAIXA':<49}VALOR")
print("-" * 58)
for chave, valor in tabela.items():
    if chave == '500' or chave == '1000':
        print(f'''CAIXA D'ÁGUA DE POLIETILENO   {chave:>5}L  +4,9%(ST)  R${valor}''')
    else:
        print(f'''CAIXA D'ÁGUA DE POLIETILENO   {chave:>5}L             R${valor}''')

print("-" * 58)
while True:
    tamanho = str(input("Digite o tamanho, em litros, da caixa desejada: "))

    if tamanho in tabela.keys():
        pass
    else:
        print("""Este valor de tamanho não foi encontrado! Cheque a tabela
para saber mais!""")
        print("-" * 58)
        continue

    qnt = int(input("Digite a quantidade de unidades desejada: "))
    print("-" * 58)
    valor = qnt * tabela[tamanho]
    valor_total += valor
    print(f"O valor de {qnt} caixas de {tamanho}L custa: {valor:.2f} reais")
    contador += 1
    if contador > 1:
        print(f"O valor total do pedido equivale a: {valor_total:.2f} reais")
    print("-" * 58)

    sair = input("Deseja escolher outro tamanho de caixa? (Sim/Nao) ").lower()
    print("-" * 58)
    sim = ['sim', 'ss', 's']
    nao = ['nao', 'nn', 'n', 'não']
    if sair in nao:
        break
    elif sair in sim:
        continue
    else:
        print('Error! Digite Sim ou Nao!')
