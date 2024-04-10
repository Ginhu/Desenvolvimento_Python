from pymongo import MongoClient


def conecta_mongo_db(
        nome_db: str, nome_collection: str, caminho_mongo):
    client = MongoClient(caminho_mongo)
    db = client[nome_db]
    return db[nome_collection]
