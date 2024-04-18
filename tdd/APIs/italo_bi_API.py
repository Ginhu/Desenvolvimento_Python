import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import json_util


from tdd.libs.autenticacao import autentica_token
from tdd.scripts.carrega_arquivo_db import consulta_db_mongo, carrega_xls_mongo
from tdd.libs.arquivos import faz_upload_arquivo

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'upload'


@app.route('/carregar/arquivo', methods=['POST'])
def carrega_xls_mongodb():
    if not autentica_token(request.headers.get('Authorization')):
        return jsonify({'msg': 'Acesso negado'}), 403

    if not request.files or 'planilha' not in request.files:
        return jsonify({'msg': 'Arquivo não enviado na requisição'}), 400
    print(request.data)
    arquivo = request.files['planilha']
    nome_arquivo = faz_upload_arquivo(arquivo, app.config['UPLOAD_FOLDER'])
    retorno = carrega_xls_mongo(nome_arquivo, 'teste_API')

    erros_msg = ['Contém dados não preenchidos', 'Contém dados não numéricos',
                 'Erro no formato do(s) cabeçalho(s)']

    if any(msg in erros_msg for msg in retorno.values()):
        return jsonify({'msg': 'Problema ao adicionar planilha(s)', 'status': retorno}), 422

    return jsonify({'msg': 'Planilhas adicionadas com sucesso!', 'status': retorno}), 201


@app.route('/consultas/tabela/<tabela>', methods=['GET'])
def consulta_db(tabela):
    if not autentica_token(request.headers.get('Authorization')):
        return jsonify({'msg': 'Acesso negado'}), 403

    consulta = consulta_db_mongo('teste_API', tabela)

    if not consulta:
        return jsonify({'msg': 'Tabela não encontrada'}), 400

    return json.loads(json_util.dumps(consulta)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
