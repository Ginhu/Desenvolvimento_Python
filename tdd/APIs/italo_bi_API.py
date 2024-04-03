import json

from flask import Flask
from flask_cors import CORS
from bson import json_util

from tdd.libs.conecta_db import conecta_mongo_db
from tdd.libs.arquivos import le_arquivo_csv
from tdd.scripts.carrega_csv_db import valida_e_corrige_valores_por_linha

app = Flask(__name__)
CORS(app)


@app.route('/carregar', methods=['POST'])
def carrega_csv_mongodb():
    collection = conecta_mongo_db('mongodb://localhost:27023/', 'teste_csv_2', 'teste_3')

    conteudo_arquivo = le_arquivo_csv('tests/dados_teste/teste_mongo1.csv', ',')
    conteudo_arquivo_corrigido = valida_e_corrige_valores_por_linha(conteudo_arquivo)

    collection.drop()
    return collection.insert_many(conteudo_arquivo_corrigido)


@app.route('/consultar', methods=['GET'])
def consulta_db():
    collection = conecta_mongo_db('mongodb://localhost:27023/', 'teste_csv_2', 'teste_3')
    consulta = collection.find()

    return json.loads(json_util.dumps(consulta)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
