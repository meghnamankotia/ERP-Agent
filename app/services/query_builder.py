#mongo query building tool
import requests
from memory.mongo_memory import get_student_data
from schemas.base import Student,FindQueryInput, UpdateQueryInput

BACKEND_URL="http://localhost:5000/api/v1/school/addStudent"

def find_query(find_query_input: FindQueryInput):
    """An MCP tool to execute a mongo db find query in the student data inorder to find desired records. The input contains the filters({"name":"priya"}) and also includes sorting, limiting and skipping parameters to enable more complex read operations. The output is the records returned from the query execution. Find one style of queries can be handle by setting limit to 1.
    """
    if "_id" in find_query_input.filters:
        from bson import ObjectId
        if "$eq" in find_query_input.filters["_id"]:
            find_query_input.filters["_id"]= ObjectId(find_query_input.filters["_id"]["$eq"])
        elif "$in" in find_query_input.filters["_id"]:
            for i in find_query_input.filters["_id"]["$in"]:
                find_query_input.filters["_id"]["$in"]= ObjectId(i)
        elif type(find_query_input.filters["_id"])==str:
            find_query_input.filters["_id"]= ObjectId(find_query_input.filters["_id"])

    collection= get_student_data()
    response=collection.find(find_query_input.filters)

    if find_query_input.sort:
        response= response.sort(find_query_input.sort[0], find_query_input.sort[1])
    if find_query_input.skip:
        response= response.skip(find_query_input.skip)
    if find_query_input.limit:
        response= response.limit(find_query_input.limit)

    results= list(response)
    for doc in results:
        doc["_id"]= str(doc["_id"])
    return results

def create_query(new_student: Student):
    """An MCP tool to create a mongo db query for creating a new student document in the students collection. The input is the details of the student to be created, and the output is the result of the query execution."""
    #response=requests.post(BACKEND_URL, json=new_student.model_dump(mode="json"))
    collection= get_student_data()
    response=collection.insert_one(new_student.model_dump(mode="json"))
    return {"inserted_id": str(response.inserted_id)}

def update_query(update_query_input: UpdateQueryInput):
    """An MCP tool to execute a mongo db update query in the student data inorder to update desired records. The input contains the filters({"name":"priya"}) to identify the records to be updated and the update parameter which specifies the update operation to be performed on the matching records. The output is the result of the query execution.    
    Update-query input format (for update_query tool):
    - filters: dictionary (MongoDB-compatible)
    - update: dictionary (MongoDB update operators)
    """
    collection= get_student_data()

    if "_id" in update_query_input.filters:
        from bson import ObjectId
        if "$eq" in update_query_input.filters["_id"]:
            update_query_input.filters["_id"]["$eq"]= ObjectId(update_query_input.filters["_id"]["$eq"])
        elif "$in" in update_query_input.filters["_id"]:
            for i in update_query_input.filters["_id"]["$in"]:
                update_query_input.filters["_id"]["$in"]= ObjectId(i)
        elif type(update_query_input.filters["_id"])==str:
            update_query_input.filters["_id"]= ObjectId(update_query_input.filters["_id"])

    docs = collection.find(
        update_query_input.filters,
        {"_id": 1}
    )
    ids = [doc["_id"] for doc in docs]

    response = collection.update_many(
        {"_id": {"$in": ids}},
        update_query_input.update
    )

    response= collection.update_many(update_query_input.filters, update_query_input.update)
    return {"matched_count": response.matched_count, "modified_count": response.modified_count, "ids": ids}

def delete_query():
    pass

def aggregation_query():
    pass