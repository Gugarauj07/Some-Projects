import os


caminho_procura = rf"{input('Caminho desejado: ')}"
termo_procura = input("Termo procurado: ")


def formata_tamanho(tamanho):
    kb = 1024
    mb = kb ** 2
    gb = kb ** 3
    tb = kb ** 4
    if tamanho < kb:
        texto = "Bytes"
    elif tamanho < mb:
        tamanho /= kb
        texto = "KiloBytes"
    elif tamanho < gb:
        tamanho /= mb
        texto = "MegaBytes"
    elif tamanho < tb:
        tamanho /= gb
        texto = "GigaBytes"
    else:
        tamanho /= tb
        texto = "TeraBytes"

    tamanho_formatado = round(tamanho, 2)
    return f"{tamanho_formatado} {texto}"


counter = 0
for raiz, diretorios, arquivos in os.walk(caminho_procura):
    for arquivo in arquivos:
        if termo_procura in arquivo:
            try:
                counter += 1
                caminho_completo = os.path.join(raiz, arquivo)
                nome_arquivo, ext_arquivo = os.path.splitext(arquivo)
                tamanho = os.path.getsize(caminho_completo)
                print(f"""Nome do arquivo: {arquivo}
Caminho: {caminho_completo}
Extensao: {ext_arquivo}
Tamanho: {formata_tamanho(tamanho)}
""")
            except PermissionError as e:
                print("Sem permissao")
            except FileNotFoundError as e:
                print("Arquivo nao encontrado")
print(f"{counter} arquivos encontrados.")