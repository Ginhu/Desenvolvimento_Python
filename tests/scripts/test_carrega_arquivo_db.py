from tdd.scripts.carrega_arquivo_db import (carrega_csv_mongodb,
                                            carrega_xls_mongo, consulta_db,
                                            transforma_em_inteiro_ou_zero)


def test_carrega_csv_mongo():
    retorno = carrega_csv_mongodb(
        'tests/dados_teste/teste_mongo1.csv', 'teste_csv_2', 'teste_3')
    assert len(retorno.inserted_ids) > 0


def test_consulta_db():
    retorno = consulta_db('teste_csv_2', 'teste_3')
    assert len(retorno) > 0


def test_transforma_em_inteiro_ou_zero():
    assert transforma_em_inteiro_ou_zero('1') == 1
    assert transforma_em_inteiro_ou_zero('') == 0
    transforma_em_inteiro_ou_zero('abc') == 0


def test_carrega_xls_mongo():
    carrega_xls_mongo('dados/Series Acumuladas1.xlsx', 'db_teste_xls')
    assert True
