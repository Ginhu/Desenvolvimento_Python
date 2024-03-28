from datetime import datetime
import time
import jwt
import pytest
from pytest_mock import MockerFixture
from tdd.erros import ImpossivelVerificarTimeout, JwtExpirado, TokenInvalido
from tdd.libs import jwt_funcs


def test_gera_jwt_sem_dh(meu_dict: dict, mocker: MockerFixture):
    """Testa geração do JWT sem o parâmetro dh"""
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21lIjoiU2VyZ2lvIiwiaWRhZGUiOjM3fQ.'\
            'JLCj4hpHaxDMmFoI8BqXtV69PhoELkAKmXoDJPXApFQ'

    retorno = jwt_funcs.gera_jwt(meu_dict)
    assert retorno == token


def test_gera_jwt_com_dh(meu_dict: dict, mocker: MockerFixture):
    """Testa a geração do JWT com o paramêtro dh = True"""
    # Verifica se a chave 'criado_em' existe dentro do dict
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')

    token_retorno = jwt_funcs.gera_jwt(meu_dict, True)
    dict_jwt_descript = jwt.decode(token_retorno, 'key', algorithms='HS256')
    assert 'criado_em' in dict_jwt_descript.keys()

    # Verifica se a diferença entre o datetime.now e o valor da chave 'criado_em'
    data_retorno = datetime.fromisoformat(dict_jwt_descript['criado_em'])
    data_nova = datetime.now().astimezone()
    assert (data_nova - data_retorno).seconds < 1

    # Verifica se os o dicionário retornado é igual usado para criar o token
    del dict_jwt_descript['criado_em']
    assert dict_jwt_descript == meu_dict


def test_descriptografa_jwt_expira_em_default(meu_dict, mocker: MockerFixture):
    """Teste de descriptogra JWT sem passar o parâmetro expira_em"""
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')
    token = jwt_funcs.gera_jwt(meu_dict)
    retorno_jwt_descript = jwt_funcs.descriptografa_jwt(token)
    assert retorno_jwt_descript == meu_dict


def test_descriptografa_jwt_raise_TokenInvalido(meu_dict: dict, mocker: MockerFixture):
    """Teste de descriptografar JWT enviando token inválido"""
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')
    token = jwt_funcs.gera_jwt(meu_dict) + 't'
    with pytest.raises(TokenInvalido) as exinfo:
        jwt_funcs.descriptografa_jwt(token)
    assert str(exinfo.value) == 'Token fornecido não é válido'


def test_descriptografa_jwt_raise_ImpossivelVerificarTimeout(meu_dict: dict, mocker: MockerFixture):
    """Teste de descriptografar JWT sem possibilidade de verificar timeout"""
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')
    token = jwt_funcs.gera_jwt(meu_dict)
    with pytest.raises(ImpossivelVerificarTimeout) as exinfo:
        jwt_funcs.descriptografa_jwt(token, 30)
    assert str(exinfo.value) == 'Não é possível verificar timeout'


def test_descriptografa_jwt_raise_JwtExpirado(meu_dict: dict, mocker: MockerFixture):
    """Teste de descriptografar JWT com token expirado"""
    mocker.patch('tdd.libs.jwt_funcs.key', 'key')
    token = jwt_funcs.gera_jwt(meu_dict, True)
    time.sleep(2)
    with pytest.raises(JwtExpirado) as exinfo:
        jwt_funcs.descriptografa_jwt(token, 1)
    assert str(exinfo.value) == 'Tempo de uso do link expirado, favor gerar um novo'


def test_descriptografa_jwt_expira_em_60(meu_dict: dict):
    """Teste de descriptografar JWT passando o paramêtro de expira_em = 60 segundos"""
    timeout = 60
    token = jwt_funcs.gera_jwt(meu_dict, True)
    retorno = jwt_funcs.descriptografa_jwt(token, timeout)
    assert 'criado_em' in retorno.keys()

    datetime_atual = datetime.now().astimezone()
    criado_em = datetime.fromisoformat(retorno['criado_em'])
    assert (datetime_atual - criado_em).seconds < timeout
