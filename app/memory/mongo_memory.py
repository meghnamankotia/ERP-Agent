#to store chat history
from pymongo import MongoClient

def make_connection():
    print("making connection")
    uri="mongodb+srv://meghnamankotia_db_user:pw4chat@chat-history.jd70bfh.mongodb.net/"
    client= MongoClient(uri)
    database= client["test"]
    collection= database["chat_history"]
    return collection

def get_student_data():
    client= MongoClient("mongodb+srv://meghnamankotia_db_user:pw4chat@chat-history.jd70bfh.mongodb.net/")
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