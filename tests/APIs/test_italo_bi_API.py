import pytest

from tdd.APIs.italo_bi_API import app

from tdd import config


@pytest.mark.parametrize(
        'headers, repsosta_status_code',
        [({}, 403), ({'Authorization': 'Bearer TokenErrado'}, 403),
         ({'Authorization': f'Bearer {config.token_acesso}'}, 400)])
def test_autenticacao_API_post(headers, repsosta_status_code):
    with app.test_client() as c:
        resp = c.post('/carregar/arquivo', json={}, headers=headers)
        assert resp.status_code == repsosta_status_code


@pytest.mark.parametrize(
        'arquivo, status_code', [('tests/dados_teste/Series Acumuladas.xlsx', 400)])
def test_requisicao_sem_arquivo(arquivo, status_code):
    with app.test_client() as c:
        data = {'files': (open(arquivo, 'rb'), arquivo.split('/')[2])}
        headers = {'Authorization': f'Bearer {config.token_acesso}'}
        assert c.post(
            'http://localhost:5000/carregar/arquivo', data=data,
            headers=headers).status_code == status_code
        assert c.post(
            'http://localhost:5000/carregar/arquivo', headers=headers).status_code == status_code


@pytest.mark.parametrize(
        'arquivo, status_code', [('tests/dados_teste/teste_subir_xls_erro_cabecalho.xlsx', 422),
                                 ('tests/dados_teste/teste_subir_xls_erro_dados.xlsx', 422),
                                 ('tests/dados_teste/teste_subir_xls_erro_dados2.xlsx', 422),
                                 ('tests/dados_teste/Series Acumuladas.xlsx', 201)])
def test_requisicao_com_arquivo_2(arquivo, status_code):
    with app.test_client() as c:
        headers = {'Authorization': f'Bearer {config.token_acesso}'}
        data = {'planilha': (open(arquivo, 'rb'), arquivo.split('/')[2])}
        assert c.post(
            'http://localhost:5000/carregar/arquivo',
            data=data, headers=headers).status_code == status_code


@pytest.mark.parametrize(
        'headers, repsosta_status_code',
        [({}, 403), ({'Authorization': 'Bearer TokenErrado'}, 403),
         ({'Authorization': f'Bearer {config.token_acesso}'}, 400)])
def test_autenticacao_API_get(headers, repsosta_status_code):
    with app.test_client() as c:
        assert c.get('/consultas/tabela/sens', json={},
                     headers=headers).status_code == repsosta_status_code


@pytest.mark.parametrize('tabela, status_code',
                         [('sens', 400),
                          ('pres', 200)])
def test_consulta_db(tabela, status_code):
    with app.test_client() as c:
        headers = {'Authorization': f'Bearer {config.token_acesso}'}

        assert c.get(f'http://localhost:5000/consultas/tabela/{tabela}',
                     headers=headers).status_code == status_code
