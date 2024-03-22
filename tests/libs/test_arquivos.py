from tdd.libs.arquivos import gera_novo_arquivo, gera_novo_nome_arquivo, le_arquivo_csv


def test_le_arquivo_csv():
    retorno_esperado = [{'Nome': 'Sergio', 'Telefone': '119876543210'},
                        {'Nome': 'Flavio', 'Telefone': '34999999999'}]
    conteudo_arquivo = le_arquivo_csv('tests/dados/teste_le_arquivo.csv')

    assert retorno_esperado == conteudo_arquivo


def test_gera_novo_nome_arquivo():
    nome_arquivo_teste = 'tests/dados/teste.csv'
    retorno_esperado = 'tests/dados/novos_dados/novo_teste.csv'

    nome_gerado = gera_novo_nome_arquivo(nome_arquivo_teste)
    assert retorno_esperado == nome_gerado


def test_gera_novo_arquivo():
    dados_de_teste = [{
        'Telefones': '(11) 9876543210',
        'fone_limpo': '119876543210'}]

    gera_novo_arquivo(
        'tests/dados/arquivo_gerar_novo_arquivo.csv', dados_de_teste)
    lista_dados_arquivo_gerado = le_arquivo_csv(
        'tests/dados/novos_dados/novo_arquivo_gerar_novo_arquivo.csv')

    assert dados_de_teste == lista_dados_arquivo_gerado
