import time

import pytest

from tdd.erros import ImpossivelVerificarTimeout, JwtExpirado, TokenFornecidoInvalido
from tdd.libs import tokens_jwt


def test_gera_jwt_sem_dh(dados_jwt: dict):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21lIjoiU2VyZ2lvIiwiaWRhZGUiOjM3fQ.'\
            'JLCj4hpHaxDMmFoI8BqXtV69PhoELkAKmXoDJPXApFQ'

    retorno = tokens_jwt.gera_jwt(dados_jwt, chave='key')
    assert retorno == token


def test_gera_jwt_com_dh(dados_jwt: dict):
    # Verifica se a chave 'criado_em' existe dentro do dict
    token_retorno = tokens_jwt.gera_jwt(dados_jwt, True)
    dict_jwt_descript = tokens_jwt.descriptografa_jwt(token_retorno)
    assert 'criado_em' in dict_jwt_descript

    # Verifica se a diferença entre o datetime.now e o valor da chave 'criado_em'
    tokens_jwt.descriptografa_jwt(token_retorno, 1)

    # Verifica se os o dicionário retornado é igual usado para criar o token
    del dict_jwt_descript['criado_em']
    assert dict_jwt_descript == dados_jwt


def test_descriptografa_jwt_sem_expiracao(dados_jwt):
    token = tokens_jwt.gera_jwt(dados_jwt)
    retorno_jwt_descript = tokens_jwt.descriptografa_jwt(token)
    assert retorno_jwt_descript == dados_jwt


def test_descriptografa_jwt_invalido_gera_erro(dados_jwt: dict):
    token = tokens_jwt.gera_jwt(dados_jwt) + 't'
    with pytest.raises(TokenFornecidoInvalido) as exinfo:
        tokens_jwt.descriptografa_jwt(token)
    assert str(exinfo.value) == 'Token fornecido não é válido'


def test_descriptografa_jwt_erro_impossivel_verificar_timeout(dados_jwt: dict):
    token = tokens_jwt.gera_jwt(dados_jwt)
    with pytest.raises(ImpossivelVerificarTimeout) as exinfo:
        tokens_jwt.descriptografa_jwt(token, 30)
    assert str(exinfo.value) == 'Não é possível verificar timeout'


def test_descriptografa_jwt_gera_erro_quando_token_expirou(dados_jwt: dict):
    token = tokens_jwt.gera_jwt(dados_jwt, True)
    time.sleep(0.1)
    with pytest.raises(JwtExpirado) as exinfo:
        tokens_jwt.descriptografa_jwt(token, 0.05)
    assert str(exinfo.value) == 'Tempo de uso do token expirou'


def test_descriptografa_jwt_expiracao_valida(dados_jwt: dict):
    timeout = 1
    token = tokens_jwt.gera_jwt(dados_jwt, True)
    retorno = tokens_jwt.descriptografa_jwt(token, timeout)
    retorno.pop('criado_em')
    assert retorno == dados_jwt
