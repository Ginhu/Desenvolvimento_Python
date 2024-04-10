from tdd.libs.conecta_db import conecta_mongo_db
from tdd import config


def test_conecta_db():
    colecao = conecta_mongo_db('banco_teste', 'semi', config.mongo_local)
    resp = list(colecao.find())
    assert len(resp) > 0


# def test_falha_conecta_db():
#     colecao = conecta_mongo_db('italo_bi', 'semi', 'mongodb://localhost:21015/')
#     assert colecao == '123'
