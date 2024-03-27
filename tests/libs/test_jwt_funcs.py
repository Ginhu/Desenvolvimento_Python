from datetime import datetime
import jwt
from tdd.libs.jwt_funcs import gera_jwt, descriptografa_jwt


def test_gera_jwt_sem_dh(meu_dict):
    """Testa geração do JWT sem o parâmetro dh"""
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21lIjoiU2VyZ2lvIiwiaWRhZGUiOjM3fQ.'\
            'JLCj4hpHaxDMmFoI8BqXtV69PhoELkAKmXoDJPXApFQ'

    retorno = gera_jwt(meu_dict)
    assert retorno == token


def test_gera_jwt_com_dh(meu_dict):
    """Testa a geração do JWT com o paramêtro dh = True"""
    # Verifica se a chave 'criado_em' existe dentro do dict
    token_retorno = gera_jwt(meu_dict, True)
    dict_jwt_descript = jwt.decode(token_retorno, 'key', algorithms='HS256')
    del meu_dict['criado_em']
    assert 'criado_em' in dict_jwt_descript.keys()

    # Verifica se a diferença entre o datetime.now e o valor da chave 'criado_em'
    data_retorno = datetime.fromisoformat(dict_jwt_descript['criado_em'])
    data_nova = datetime.now().astimezone()
    assert (data_nova - data_retorno).seconds < 1

    # Verifica se os o dicionário retornado é igual usado para criar o token
    del dict_jwt_descript['criado_em']
    assert dict_jwt_descript == {'nome': 'Sergio', 'idade': 37}


def test_descriptografa_jwt_expira_em_default(meu_dict):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21lIjoiU2VyZ2lvIiwiaWRhZGUiOjM3fQ.'\
        'JLCj4hpHaxDMmFoI8BqXtV69PhoELkAKmXoDJPXApFQ'
    retorno_jwt_descript = descriptografa_jwt(token)
    assert retorno_jwt_descript == {'nome': 'Sergio', 'idade': 37}


def test_descriptografa_jwt_expira_em_60(meu_dict):
    timeout = 60
    token = gera_jwt(meu_dict, True)
    retorno = descriptografa_jwt(token, timeout)
    assert 'criado_em' in retorno.keys()

    datetime_atual = datetime.now().astimezone()
    criado_em = datetime.fromisoformat(retorno['criado_em'])
    assert (datetime_atual - criado_em).seconds < timeout
