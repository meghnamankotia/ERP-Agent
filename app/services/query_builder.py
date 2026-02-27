#mongo query building tool
import requests
from memory.mongo_memory import make_connection
from schemas.base import Student,FindQueryInput, UpdateQueryInput,CreateQueryInput

BACKEND_URL="http://localhost:5000/api/v1/school/addStudent"

def find_query(find_query_input: FindQueryInput):
    """An MCP tool to execute a mongo db find query in the student data inorder to find desired records. The input contains the filters({"name":"priya"}) and also includes sorting, limiting and skipping parameters to enable more complex read operations as well as the collection/index where the data is to be found. The output is the records returned from the query execution. Find one style of queries can be handle by setting limit to 1.
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

    collection= make_connection(find_query_input.idx_name)
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

def create_query(new_record: CreateQueryInput):
    """An MCP tool to create a mongo db query for creating a new document in a collection. The input is the details of the record to be created in a dictionary format as well as the name of collection/index in which they are to be added, and the output is the result of the query execution.
    eg- "idx_name": "teachers"
        "data": {"name": "Smita Rani",
                 "class_teacher": 3
                }
    """
    print(new_record.data)
    collection= make_connection(new_record.idx_name)
    response=collection.insert_one(new_record.data)
    return {"inserted_id": str(response.inserted_id)}

def update_query(update_query_input: UpdateQueryInput):
    """An MCP tool to execute a mongo db update query in the student data inorder to update desired records. The input contains the index/collection to update, the filters({"name":"priya"}) to identify the records to be updated and the update parameter which specifies the update operation to be performed on the matching records. The output is the result of the query execution.    
    Update-query input format (for update_query tool):
    - filters: dictionary (MongoDB-compatible)
    - update: dictionary (MongoDB update operators)
    """
    collection= make_connection(update_query_input.idx_name)

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

    response= collection.update_many(update_query_input.filters, update_query_input.update)
    print("called update query for", ids, "\nand filters, ", update_query_input.filters, "\nand update param",update_query_input.update )
    return {"matched_count": response.matched_count, "modified_count": response.modified_count, "ids": ids}

def delete_query(filters: dict, index:str):
    """An MCP tool to perform delete operations for desired Mongo db records. The input consists of the filter({"_id": ObjectId}, etc) as well as the name of the collection/table from which we're deleting. The output is the ids of the records deleted."""
    if "_id" in filters:
        from bson import ObjectId
        if "$eq" in filters["_id"]:
            filters["_id"]= ObjectId(filters["_id"]["$eq"])
        elif "$in" in filters["_id"]:
            for i in filters["_id"]["$in"]:
                filters["_id"]["$in"]= ObjectId(i)
        elif type(filters["_id"])==str:
            filters["_id"]= ObjectId(filters["_id"])

    collection= make_connection(index)
    response=collection.find(filters)
    print("for filter", filters, "\n records returned-", response)
    ids=[str(doc["_id"]) for doc in response]
    print(ids)

    collection.delete_many(filters)
    return {"deleted records": ids}