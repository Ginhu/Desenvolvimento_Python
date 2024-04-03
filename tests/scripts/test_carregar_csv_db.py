from tdd.scripts.carrega_csv_db import carrega_csv_mongodb, consulta_db


def test_carrega_csv_mongo():
    retorno = carrega_csv_mongodb(
        'tests/dados_teste/teste_mongo1.csv',
        'mongodb://localhost:27023/', 'teste_csv_2', 'teste_3')
    assert len(retorno.inserted_ids) > 0


def test_consulta_db():
    retorno = consulta_db('mongodb://localhost:27023/', 'teste_csv_2', 'teste_3')
    assert retorno is False
