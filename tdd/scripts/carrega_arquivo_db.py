import pandas as pd
from pydantic_core import ValidationError

from tdd.libs.conecta_db import conecta_mongo_db
from tdd.libs.arquivos import le_arquivo_csv, le_arquivo_xls
from tdd.dominio import campos_italo_bi
from tdd import config


def carrega_csv_mongodb(nome_arquivo: str, nome_db: str, nome_collection: str,
                        caminho_mongo: str = config.mongo_db):
    collection = conecta_mongo_db(nome_db, nome_collection, caminho_mongo)

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


def converte_cabecalho(
        lista: list[dict], nome_planilha: str, formato_json: bool = False) -> list[dict]:
    if nome_planilha == 'SEMI':
        for i in range(len(lista)):
            dados = campos_italo_bi.DadosSemi(**lista[i])
            lista[i] = dados.model_dump(by_alias=formato_json)
        return lista

    if nome_planilha == 'EADC':
        for i in range(len(lista)):
            dados = campos_italo_bi.DadosEadc(**lista[i])
            lista[i] = dados.model_dump(by_alias=formato_json)
        return lista

    if nome_planilha == 'EAD2':
        for i in range(len(lista)):
            dados = campos_italo_bi.DadosEad2(**lista[i])
            lista[i] = dados.model_dump(by_alias=formato_json)
        return lista

    if nome_planilha == 'PRES':
        for i in range(len(lista)):
            dados = campos_italo_bi.DadosPres(**lista[i])
            lista[i] = dados.model_dump(by_alias=formato_json)
        return lista

    for i in range(len(lista)):
        dados = campos_italo_bi.DadosPorSemestre(**lista[i])
        lista[i] = dados.model_dump(by_alias=formato_json)

    return lista


def consulta_db_mongo(nome_db: str, nome_collection: str, caminho_mongo: str = config.mongo_local):
    collection = conecta_mongo_db(nome_db, nome_collection, caminho_mongo)
    consulta = list(collection.find(projection={'_id': False}))

    retorno = converte_cabecalho(consulta, nome_collection.upper(), True)
    return retorno


def carrega_xls_mongo(nome_arquivo: str, nome_db: str, caminho_mongo: str = config.mongo_local):

    nome_planilhas = le_arquivo_xls(nome_arquivo).sheet_names
    resp = {}

    for planilha in nome_planilhas:
        if planilha == 'Notas':
            continue

        dados_planilha = pd.read_excel(nome_arquivo, planilha).to_dict('records')

        try:
            dados_planilha_padronizados = converte_cabecalho(dados_planilha, planilha)
        except TypeError:
            print(f'Erro no formato do cabeçalho na planilha: {planilha}')
            resp[planilha] = 'Erro no formato do cabeçalho'
            continue
        except ValidationError:
            print(f'Erro encontrado nos valores das tabelas {planilha}')
            resp[planilha] = 'Erro encontrado: valores da tabela'
            continue

        collection = conecta_mongo_db(nome_db, planilha.lower(), caminho_mongo)
        collection.drop()
        collection.insert_many(dados_planilha_padronizados)
        resp[planilha] = 'Adicionada com sucesso no banco'

    return resp


if __name__ == '__main__':
    pass
