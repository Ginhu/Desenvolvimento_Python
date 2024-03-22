import re


def retorna_somente_numeros(telefone: str) -> str:
    padrao_re = r"\d+"

    lista_numeros = re.findall(padrao_re, telefone)
    somente_numeros = ''.join(lista_numeros)

    return somente_numeros
