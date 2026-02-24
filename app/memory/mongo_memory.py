#to store chat history
from pymongo import MongoClient
uri="SET_URI_STRING"
def make_connection():
    print("making connection")
    client= MongoClient(uri)
    database= client["test"]
    collection= database["chat_history"]
    return collection

def get_student_data():
    client= MongoClient(uri)
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
