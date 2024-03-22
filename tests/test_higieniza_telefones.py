from tdd import higieniza_telefones


def test_fixture(meu_nome: str):
    assert meu_nome == 'Sergio'


def test_adiciona_telefone_limpo():
    dados_de_teste = {'Nome': 'Sergio',
                      'Telefones': '(11) 9876543210'}

    retorno_esperado = {'Nome': 'Sergio',
                        'Telefones': '(11) 9876543210',
                        'fone_limpo': '119876543210'}

    assert retorno_esperado == higieniza_telefones.adiciona_telefone_limpo(dados_de_teste)


def test_higieniza_telefone():
    higieniza_telefones.higieniza_telefone('tests/dados_teste/arquivo_de_teste.csv')
