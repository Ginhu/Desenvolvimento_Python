import pytest

from tdd.scripts.carrega_arquivo_db import (carrega_csv_mongodb,
                                            carrega_xls_mongo, consulta_db_mongo,
                                            converte_cabecalho,
                                            transforma_em_inteiro_ou_zero,
                                            valida_e_corrige_valores_por_linha)


def test_carrega_csv_mongo():
    retorno = carrega_csv_mongodb(
        'tests/dados_teste/teste_mongo1.csv', 'teste_csv_2', 'teste_3')
    assert len(retorno.inserted_ids) > 0


@pytest.mark.parametrize('entrada, saida', [([{'a': ''}], [{'a': 0}]), ([{'a': 'a'}], [{'a': 0}])])
def test_valida_e_corrige_valores_por_linhas(entrada, saida):
    assert valida_e_corrige_valores_por_linha(entrada) == saida


def test_transforma_em_inteiro_ou_zero():
    assert transforma_em_inteiro_ou_zero('1') == 1
    assert transforma_em_inteiro_ou_zero('') == 0
    assert transforma_em_inteiro_ou_zero('abc') == 0


@pytest.mark.parametrize('lista, nome_planilha, formato_json, retorno', [
    ([{'18.2 SEMI CAL CAP': 0}], 'SEMI', False, 's_18_2_semi_cal_cap'),
    ([{'18.2 EADC CAL CAP': 0}], 'EADC', False, 's_18_2_eadc_cal_cap'),
    ([{'18.2 EAD2 OIN CAP': 0}], 'EAD2', False, 's_18_2_ead2_oin_cap'),
    ([{'18.2 PRES CAL CAP': 0}], 'PRES', False, 's_18_2_pres_cal_cap'),
    ([{'16.1': 0}], 'ACUM', False, 's_16_1'),
    ([{'s_18_2_semi_cal_cap': 0}], 'SEMI', True, '18.2 SEMI CAL CAP'),
    ([{'s_18_2_eadc_cal_cap': 0}], 'EADC', True, '18.2 EADC CAL CAP'),
    ([{'s_18_2_ead2_oin_cap': 0}], 'EAD2', True, '18.2 EAD2 OIN CAP'),
    ([{'s_18_2_pres_cal_cap': 0}], 'PRES', True, '18.2 PRES CAL CAP')])
def test_padroniza_cabecalho(lista, nome_planilha, formato_json, retorno):

    assert converte_cabecalho(lista, nome_planilha, formato_json)[0][retorno] == 0


def test_consulta_db_mongo():
    retorno = consulta_db_mongo('banco_teste', 'semi')
    assert len(retorno) > 0


@pytest.mark.parametrize(
        'nome_arquivo, retorno',
        [('tests/dados_teste/teste_subir_xls.xlsx', 'Adicionada com sucesso no banco'),
         ('tests/dados_teste/teste_subir_xls_erro_cabecalho.xlsx', 'Erro no formato do cabeçalho'),
         ('tests/dados_teste/teste_subir_xls_erro_dados.xlsx',
          'Erro encontrado: valores da tabela'),
         ('tests/dados_teste/teste_subir_xls_erro_dados2.xlsx',
          'Erro encontrado: valores da tabela')])
def test_carrega_xls_mongo(nome_arquivo, retorno):

    assert carrega_xls_mongo(nome_arquivo, 'banco_teste')['ACUM'] == retorno
