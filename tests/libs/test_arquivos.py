from tdd.libs.arquivos import (gera_novo_arquivo,
                               gera_novo_nome_arquivo,
                               le_arquivo_csv,
                               le_arquivo_xls,
                               faz_upload_arquivo)


def test_le_arquivo_csv():
    retorno_esperado = [{'Nome': 'Sergio', 'Telefone': '119876543210'},
                        {'Nome': 'Flavio', 'Telefone': '34999999999'}]
    conteudo_arquivo = le_arquivo_csv('tests/dados_teste/teste_le_arquivo.csv')

    assert retorno_esperado == conteudo_arquivo


def test_gera_novo_nome_arquivo():
    caminho_relativo = 'tests/dados_teste/'
    nome_arquivo_teste = f'{caminho_relativo}arquivo_de_teste.csv'
    retorno_esperado = f'{caminho_relativo}novos_dados/novo_arquivo_de_teste.csv'

    nome_gerado = gera_novo_nome_arquivo(nome_arquivo_teste)
    assert retorno_esperado == nome_gerado


def test_gera_novo_arquivo():
    dados_de_teste = [{
        'Telefones': '(11) 9876543210',
        'fone_limpo': '119876543210'}]
    caminho_relativo = 'tests/dados_teste/'
    gera_novo_arquivo(f'{caminho_relativo}arquivo_gerar_novo_arquivo.csv', dados_de_teste)
    lista_dados_arquivo_gerado = le_arquivo_csv(
        f'{caminho_relativo}novos_dados/novo_arquivo_gerar_novo_arquivo.csv')

    assert dados_de_teste == lista_dados_arquivo_gerado


def test_le_arquivo_xls():
    conteudo_xls = le_arquivo_xls('tests/dados_teste/Series Acumuladas.xlsx')
    assert conteudo_xls.sheet_names == ['ACUM', 'REMA', 'INGR', 'CAPT', 'EVAS', 'SEMI', 'EADC',
                                        'EAD2', 'PRES', 'Notas']


# def test_salva_arquivo_upload():
#     class Arquivo():
#         def save():
#             return True

#         def filename():
#             return 'Series Acumuladas.xlsx'
#     faz_upload_arquivo(Arquivo, 'upload')
#     assert le_arquivo_xls(
#         'upload/Series Acumuladas.xlsx').sheet_names == ['ACUM', 'REMA', 'INGR', 'CAPT', 'EVAS',
#                                                          'SEMI', 'EADC', 'EAD2', 'PRES', 'Notas']
