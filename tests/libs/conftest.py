import pytest


@pytest.fixture
def dados_jwt():
    return {'nome': 'Sergio', 'idade': 37}
