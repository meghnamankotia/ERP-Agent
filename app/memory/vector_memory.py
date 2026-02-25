from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

def make_vector_connection(idx_name: str):
    pc= Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    if not pc.has_index(idx_name):
        return "Index not found"
    index= pc.Index(idx_name)
    return index
