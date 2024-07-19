from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

uri = config("MONGO_DB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db
collection_name = db['todo_collection']


if __name__ == '__main__':
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)