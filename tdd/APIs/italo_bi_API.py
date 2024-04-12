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

    arquivo = request.files['arquivo']
    if not arquivo or arquivo.filename == '':
        return jsonify({'msg': 'Arquivo não enviado na requisição'})

    nome_arquivo = faz_upload_arquivo(arquivo, app.config['UPLOAD_FOLDER'])

    retorno = carrega_xls_mongo(nome_arquivo, 'teste_API')

    if ('Erro no formato do cabeçalho' in retorno.values()) or ('Erro encontrado: valores da tabela'
                                                                in retorno.values()):
        return jsonify({'msg': 'Problema ao adicionar planilha(s)', 'relatorio': retorno}), 422

    return jsonify({'msg': 'Planilhas adicionadas com sucesso!', 'relatorio': retorno}), 201


@app.route('/consultas/tabela/<tabela>', methods=['GET'])
def consulta_db(tabela):
    if not autentica_token(request.headers.get('Authorization')):
        return jsonify({'msg': 'Acesso negado'}), 403

    # collection = conecta_mongo_db(config.mongo_local, config.banco, tabela)
    # consulta = list(collection.find(projection={'_id': False}))
    consulta = consulta_db_mongo('banco_teste', tabela)

    if not consulta:
        return jsonify({'msg': 'Tabela não encontrada'}), 400

    return json.loads(json_util.dumps(consulta)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
