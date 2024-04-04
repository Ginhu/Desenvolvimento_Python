from tdd.libs.conecta_db import conecta_mongo_db
from tdd.libs.arquivos import le_arquivo_csv


def carrega_csv_mongodb(nome_arquivo: str, caminho_mongo: str, nome_db: str, nome_collection: str):
    collection = conecta_mongo_db(caminho_mongo, nome_db, nome_collection)

    conteudo_arquivo = le_arquivo_csv(nome_arquivo, ',')
    conteudo_arquivo_corrigido = valida_e_corrige_valores_por_linha(conteudo_arquivo)

    collection.drop()
    return collection.insert_many(conteudo_arquivo_corrigido)


def valida_e_corrige_valores_por_linha(lista: list[dict]):
    for i in range(len(lista)):
        if '' in lista[i].values():
            print(lista[i])
        lista[i] = {k: transforma_em_inteiro_ou_zero(v) for k, v in lista[i].items()}

    return lista


def transforma_em_inteiro_ou_zero(valor):
    try:
        valor = int(valor)
    except ValueError:
        valor = 0
        pass
    return valor


def consulta_db(caminho_mongo: str, nome_db: str, nome_collection: str):
    collection = conecta_mongo_db(caminho_mongo, nome_db, nome_collection)
    consulta = collection.find()

    return list(consulta)


if __name__ == '__main__':
    pass
