from tdd.libs.arquivos import gera_novo_arquivo, le_arquivo_csv
from tdd.libs.strings import retorna_somente_numeros
# 1.Abrir .csv
# 2.Campo telefones com varios registros, pegar o primeiro telefone
# 3.Limpar o numero, no final ter apenas os números.
# 4.Adicionar um campo em cada linha do .csv chamado fone_limpo e adicionar
# este numero no campo

# 5.Gravar um novo arquivo .csv com o campo fone_limpo adicionado

# 1.Fazer tudo funcionar sem testes
# 2.Criar teste para as funcionalidades desenvolvidas
CAMINHO_ARQUIVO = 'tests'


def adiciona_telefone_limpo(dado: dict) -> dict:
    telefones = dado['Telefones']
    primeiro_telefone = telefones.split(',')[0]
    dado['fone_limpo'] = retorna_somente_numeros(primeiro_telefone)
    return dado


def higieniza_telefone(nome_arquivo: str):
    dados_arquivo = le_arquivo_csv(nome_arquivo)
    for dado in dados_arquivo:
        adiciona_telefone_limpo(dado)
    return gera_novo_arquivo(nome_arquivo, dados_arquivo)


if __name__ == '__main__':
    nome_arquivo = 'dados/BaseRematricula-2024-02.csv'
    higieniza_telefone(nome_arquivo)
