import pytest
from tdd import config
from tdd.libs.autenticacao import autentica_token


@pytest.mark.parametrize(
        'token, resultado', [('', False), ('Bearer TokenFalso', False),
                             (f'Bearer {config.token_acesso}', True)])
def test_autentica_token(token, resultado):
    assert autentica_token(token) == resultado
