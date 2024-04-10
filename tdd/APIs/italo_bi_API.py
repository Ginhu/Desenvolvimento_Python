import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import json_util

from tdd import config
from tdd.scripts.carrega_arquivo_db import consulta_db_mongo, carrega_xls_mongo

app = Flask(__name__)
CORS(app)


@app.route('/carregar/arquivo', methods=['POST'])
def carrega_xls_mongodb():
    str_token = request.headers.get('Authorization')
    if not str_token:
        return jsonify({'msg': 'Acesso negado'}), 403

    token = str_token.split(' ')[1]
    if token != config.token_acesso:
        return jsonify({'msg': 'Acesso negado'}), 403

    body = request.json

    if not body['arquivo']:
        return jsonify({'msg': 'Campo arquivo é necessário para requisição'}), 400
    retorno = carrega_xls_mongo(body['arquivo'], 'teste_API')

    if 'Erro no formato do cabeçalho' or 'Erro encontrado: valores da tabela' in retorno.values():
        return jsonify({'msg': 'Problema ao adicionar planilhas', 'relatorio': retorno}), 422

    return jsonify({'msg': 'Planilhas adicionadas com sucesso!', 'relatorio': retorno}), 201


@app.route('/consultas/tabela/<tabela>', methods=['GET'])
def consulta_db(tabela):
    str_token = request.headers.get('Authorization')
    if not str_token:
        return jsonify({'msg': 'Acesso negado'}), 403

    token = str_token.split(' ')[1]
    if token != config.token_acesso:
        return jsonify({'msg': 'Acesso negado'}), 403

    # collection = conecta_mongo_db(config.mongo_local, config.banco, tabela)
    # consulta = list(collection.find(projection={'_id': False}))
    consulta = consulta_db_mongo(config.banco, tabela)

    if not consulta:
        return jsonify({'msg': 'Tabela não encontrada'}), 400

    return json.loads(json_util.dumps(consulta)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
