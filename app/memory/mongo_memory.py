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

def make_connection():
    client= get_client()
    database= client["test"]
    collection= database["chat_history"]
    return collection

def get_student_data():
    client= get_client()
    database= client["test"]
    collection= database["studentdatas"]
    return collection

def store_chat_history(messages:list):
    collection= make_connection()
    #store messages in db
    collection.insert_one({"messages":messages})
    return

def get_chat_history():
    pass
