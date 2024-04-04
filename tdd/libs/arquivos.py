import csv

from pathlib import Path

from tdd.erros import NaoEncontrado


def le_arquivo_csv(nome_arquivo: str, separador: str = ';') -> list[dict]:
    try:
        with open(nome_arquivo, 'r', encoding='ISO-8859-1') as arquivo_aberto:
            conteudo_csv = list(csv.DictReader(arquivo_aberto, delimiter=separador))
    except FileNotFoundError:
        raise NaoEncontrado(f'Arquivo não encontrado: {nome_arquivo}')

    return conteudo_csv


def gera_novo_nome_arquivo(nome_arquivo: str) -> str:
    path = Path(nome_arquivo)
    # nome_do_arquivo = 'novo_' + path.name
    # caminho_arquivo = str(path.parent) + '/novos_dados'
    novo_arquivo = path.parent / 'novos_dados' / ('novo_' + path.name)

    return str(novo_arquivo)


def gera_novo_arquivo(nome_arquivo: str, data: list[dict]):
    nome_arquivo_novo = gera_novo_nome_arquivo(nome_arquivo)

    try:
        with open(nome_arquivo_novo, 'w', encoding='ISO-8859-1') as novo:

            nomes_campos = data[0].keys()
            escritor_dict = csv.DictWriter(
                novo, fieldnames=nomes_campos, delimiter=';')

            escritor_dict.writeheader()
            escritor_dict.writerows(data)

    except FileExistsError:
        raise NaoEncontrado(f'Arquivo não encontrado: {nome_arquivo_novo}')
