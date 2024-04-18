from tdd.dominio import campos_italo_bi

mapa_planilha_classe = {
    'SEMI': campos_italo_bi.DadosSemi,
    'EADC': campos_italo_bi.DadosEadc,
    'EAD2': campos_italo_bi.DadosEad2,
    'PRES': campos_italo_bi.DadosPres,
    'ACUM': campos_italo_bi.DadosPorSemestre,
    'REMA': campos_italo_bi.DadosPorSemestre,
    'INGR': campos_italo_bi.DadosPorSemestre,
    'CAPT': campos_italo_bi.DadosPorSemestre,
    'EVAS': campos_italo_bi.DadosPorSemestre
}


def converte_cabecalho(
        lista: list[dict], nome_planilha: str, formato_json: bool = False) -> list[dict]:
    ret = []

    for i in lista:
        dados = mapa_planilha_classe[nome_planilha](**i)
        ret.append(dados.model_dump(by_alias=formato_json))
    return ret


def retorno_erro_cabecalho(planilha: str) -> str:
    print(f'Erro no formato do cabeçalho da planilha: {planilha}')
    return 'Erro no formato do(s) cabeçalho(s)'


def retorno_erro_nao_numerico(planilha: str) -> str:
    print(f'Erro no formato dos dados da planilha: {planilha}')
    return 'Contém dados não numéricos'


tratamento_typeerror = {
    'must be real number, not str': retorno_erro_nao_numerico,
    'keywords must be strings': retorno_erro_cabecalho
}
