#mongo query building tool
import requests
from memory.mongo_memory import get_student_data
from schemas.base import Student,FindQueryInput

BACKEND_URL="http://localhost:5000/api/v1/school/addStudent"

def request_query(query_input: FindQueryInput):
    """An MCP tool to execute a mongo db find query in the student data inorder to find desired records. The input contains the filters({"name":"priya"}) and also includes sorting, limiting and skipping parameters to enable more complex read operations. The output is the records returned from the query execution. Find one style of queries can be handle by setting limit to 1."""

    collection= get_student_data()
    response=collection.find(query_input.filters)

    if query_input.sort:
        response= response.sort(query_input.sort[0], query_input.sort[1])
    if query_input.skip:
        response= response.skip(query_input.skip)
    if query_input.limit:
        response= response.limit(query_input.limit)

    results= list(response)
    for doc in results:
        doc["_id"]= str(doc["_id"])
    return results

def create_query(newStudent: Student):
    """An MCP tool to create a mongo db query for creating a new student document in the students collection. The input is the details of the student to be created, and the output is the result of the query execution."""
    response=requests.post(BACKEND_URL, json=newStudent.model_dump(mode="json"))
    return response.json()