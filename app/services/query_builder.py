#mongo query building tool
import requests
from schemas.base import Student

BACKEND_URL="http://localhost:5000/api/v1/school/addStudent"

def build_query():
    pass

def create_query(newStudent: Student):
    """An MCP tool to create a mongo db query for creating a new student document in the students collection. The input is the details of the student to be created, and the output is the result of the query execution."""
    response=requests.post(BACKEND_URL, json=newStudent.model_dump(mode="json"))
    return response.json()
