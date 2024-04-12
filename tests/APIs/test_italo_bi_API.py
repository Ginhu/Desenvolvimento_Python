import requests
import pytest

from tdd import config


@pytest.mark.parametrize(
        'headers, repsosta_status_code',
        [({}, 403), ({'Authorization': 'Bearer TokenErrado'}, 403)])
def test_autenticacao_API(headers, repsosta_status_code):
    assert requests.post(
        'http://localhost:5000/carregar/arquivo', json={},
        headers=headers).status_code == repsosta_status_code


# @pytest.mark.parametrize('headers, body, status_code',
#                          [({'Authorization': f'Bearer {config.token_acesso}'}, {}, 400),
#                           ({'Authorization': f'Bearer {config.token_acesso}'},
#                            {'arquivo': ''}, 400),
#                           ({'Authorization': f'Bearer {config.token_acesso}'},
#                            {'arquivo': 'tests/dados_teste/teste_subir_xls_erro_cabecalho.xlsx'},
#                            422),
#                           ({'Authorization': f'Bearer {config.token_acesso}'},
#                            {'arquivo': 'tests/dados_teste/teste_subir_xls_erro_dados.xlsx'}, 422),
#                           ({'Authorization': f'Bearer {config.token_acesso}'},
#                            {'arquivo': 'tests/dados_teste/teste_subir_xls_erro_dados2.xlsx'}, 422),
#                           ({'Authorization': f'Bearer {config.token_acesso}'},
#                            {'arquivo': 'tests/dados_teste/teste_subir_xls.xlsx'}, 201)])
# def test_carrega_xls_mongo(headers, body, status_code):
#     assert requests.post(
#         'http://localhost:5000/carregar/arquivo', json=body,
#         headers=headers).status_code == status_code


@pytest.mark.parametrize('headers, tabela, status_code',
                         [({}, 'semi', 403),
                          ({'Authorization': 'Bearer TokenErrado'}, 'semi', 403),
                          ({'Authorization': f'Bearer {config.token_acesso}'}, 'sens', 400),
                          ({'Authorization': f'Bearer {config.token_acesso}'}, 'pres', 200)])
def test_consulta_db(headers, tabela, status_code):
    assert requests.get(f'http://localhost:5000/consultas/tabela/{tabela}',
                        headers=headers).status_code == status_code
