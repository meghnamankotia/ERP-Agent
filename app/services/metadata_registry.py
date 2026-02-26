#schema search from vector db
from bson import ObjectId
from schemas.base import VectorMemoryInput, SchemaSearchInput
from memory.vector_memory import make_vector_connection

def schema_search(input: SchemaSearchInput):
    """An MCP tool to perform a schema search on the vector db inorder to retrieve information relevant to create a mongo query. For eg- User ids of students who are failing. The output is the relevant information retrieved from the vector db that can be used to create a mongo query(id of students).
    class SchemaSearchInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to perform the schema search on.")]
    input: Annotated[str, Field(description="The input text query for which relevant information is to be retrieved from the vector db inorder to create a mongo query.")]
    top_k: Annotated[int, Field(description="The number of top results to return from the schema search.")]
    filters: Annotated[dict, Field(description="The filter criteria to apply during the schema search.")] eg- { "class": 10} """
    idx=make_vector_connection(input.idx_name)
    query={"inputs": {"text": input.input}, "top_k": input.top_k}
    if input.filters and len(input.filters)>0:
        query["filter"]= input.filters
    responses=idx.search(namespace="__default__", query=query)

    #change id back to object id and return responses in serializable format
    results=[]
    for i in responses["result"]["hits"]:
        results.append({"_id": i["_id"], "_score": i["_score"], "fields": i["fields"]})
    return {"results": results}

def create_vector(input: VectorMemoryInput):
    """An MCP tool to create vector data in the vector db after the data has been added to the main mongo db. Hence this tool is only to be called after the successful execution of the create_query tool or the update_query tool followed by the fetch query tool. 
    The output is a confirmation message indicating that the vector data has been stored successfully."""
    idx= make_vector_connection(input.idx_name)
    inputs= {"id": input.id, "text": input.text}
    for key,value in input.metadata.items():
        if key not in inputs:
            inputs[key]=value
    idx.upsert_records(namespace="__default__", records=[inputs])
    return "Vector data stored successfully"

def delete_vector(ids: list[str], idx_name:str):
    """An MCP tool to delete vector data in the vector db after the data has been deleted from the main mongo db. Hence this tool is only to be called after the successful execution of the delete_query tool. The output is a confirmation method that the records have been deleted successfully. The vectors can only deleted by using the id of the respective vectors."""
    idx=make_vector_connection(idx_name)
    idx.delete(ids)
    return "Records deleted"