#to store chat history
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(
            os.getenv("MONGO_URI"),
            serverSelectionTimeoutMS=5000,
        )
        # fail fast if connection is bad
        _client.admin.command("ping")
    return _client

def make_connection(collection_name:str):
    client= get_client()
    database= client["test"]
    collection= database[collection_name]
    return collection

def store_chat_history(messages:list):
    collection= make_connection("chat_history")
    #store messages in db
    collection.insert_one({"messages":messages})
    return

def get_chat_history():
    pass
