from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
    
    def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Conexão com o MongoDB bem sucedida!")
        except Exception as e:
            raise ConnectionError("Falha ao conectar com o MongoDB") from e

if __name__ == '__main__':
    uri = config("MONGODB_URI")
    db_name = "fastapi_mongodb"
    mongo_db = MongoDB(uri, db_name)

    mongo_db.ping()
