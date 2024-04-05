import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import json_util

from tdd import config
from tdd.libs.conecta_db import conecta_mongo_db
from tdd.libs.arquivos import le_arquivo_csv
from tdd.scripts.carrega_arquivo_db import valida_e_corrige_valores_por_linha

app = Flask(__name__)
CORS(app)


@app.route('/carregar', methods=['POST'])
def carrega_csv_mongodb():
    collection = conecta_mongo_db('mongodb://localhost:27017/', 'teste_csv_2', 'teste_3')

    conteudo_arquivo = le_arquivo_csv('tests/dados_teste/teste-semi.csv', ',')
    conteudo_arquivo_corrigido = valida_e_corrige_valores_por_linha(conteudo_arquivo)

    collection.drop()
    collection.insert_many(conteudo_arquivo_corrigido)
    response = {
        'message': 'arquivo carregado no banco de dados'
    }
    return jsonify(response), 200


@app.route('/consultas/tabela/<tabela>', methods=['GET'])
def consulta_db(tabela):
    str_token = request.headers.get('Authorization')
    if not str_token:
        return jsonify({'msg': 'Acesso negado'}), 403

    token = str_token.split(' ')[1]
    if token != config.token_acesso:
        return jsonify({'msg': 'Acesso negado'}), 403

    collection = conecta_mongo_db(config.mongo_db, config.banco, tabela)
    consulta = list(collection.find(projection={'_id': False}))

    if not consulta:
        return jsonify({'msg': 'Tabela não encontrada'}), 400

    return json.loads(json_util.dumps(consulta)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
