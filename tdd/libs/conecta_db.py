from pymongo import MongoClient


def conecta_mongo_db(caminho_mongo: str, nome_db: str, nome_collection: str):
    client = MongoClient(caminho_mongo)
    db = client[nome_db]

    return db[nome_collection]
