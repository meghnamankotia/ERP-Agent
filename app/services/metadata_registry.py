#schema search from vector db
from bson import ObjectId
from schemas.base import VectorMemoryInput, SchemaSearchInput, VectorUpdateInput
from memory.vector_memory import make_vector_connection

def schema_search(input: SchemaSearchInput):
    """An MCP tool to perform a schema search on the vector db inorder to retrieve information relevant to create a mongo query. For eg- User ids of students who are failing. The output is the relevant information retrieved from the vector db that can be used to create a mongo query(id of students).
    class SchemaSearchInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to perform the schema search on.")]
    input: Annotated[str, Field(description="The input text query for which relevant information is to be retrieved from the vector db inorder to create a mongo query.")]
    top_k: Annotated[int, Field(description="The number of top results to return from the schema search.")]
    filter: Annotated[dict, Field(description="The filter criteria to apply during the schema search.")] eg- { "class": 10} """
    idx=make_vector_connection(input.idx_name)
    query={"inputs": {"text": input.input}, "top_k": input.top_k}
    if input.filter and len(input.filter)>0:
        query["filter"]= input.filter
    responses=idx.search(namespace="__default__", query=query)

    #change id back to object id and return responses in serializable format
    results=[]
    for i in responses["result"]["hits"]:
        results.append({"_id": i["_id"], "_score": i["_score"], "fields": i["fields"]})
    return {"results": results}

def create_vector(input: VectorMemoryInput):
    """An MCP tool to create vector data in the vector db after the data has been added to the main mongo db database. Hence this tool is only to be called after the successful execution of the create_query tool.  
    class VectorMemoryInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to store the data in.")]
    data: Annotated[dict, Field(description="Text field to be embedded and each metadata field set sepearatley in the vector db record.")]
    eg- idx_name: "studentdatas"
        data: {"_id": corresponding mongo db id ,"text": "fields relevant to schema search in string format", "age": 15, "class": 10, "roll_no": 23, "blood_group": "A+" + other fields to be set in the metadata}
    The data dictionary includes the text that is to be embedded and the metadata fields that are to be set separately in the vector db record. The output is a confirmation message indicating that the vector data has been stored successfully."""
    idx= make_vector_connection(input.idx_name)
    idx.upsert_records(namespace="__default__", records=[input.data])
    return "Vector data stored successfully"

def update_vector(input: VectorUpdateInput):
    """An MCP tool to update vector data in the vector db. This tool must be called after the successful execution of the update_query tool in order to keep the vector db data in sync with the main mongo db database.
    class VectorUpdateInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to store the data in.")]
    id: Annotated[str, Field(description="The id of the vector record to be updated.")]
    metadata: Optional[dict]=Field(default_factory=dict, description="The metadata fields to be updated in the vector db record.")
    text: Optional[str]=Field(default=None, description="The text content to be updated in the vector db record.")

    pass input according to whether the field needing updating is a text field or a metadata field.
    The data dictionary includes the content that is to be changed, whether in the text of the embedding or in the metadata fields, and the id of the record that is to be updated. The output is a confirmation message indicating that the vector data has been updated successfully."""
    print("Updating vector data with input:", input)
    idx= make_vector_connection(input.idx_name)
    idx.update(namespace="__default__", id= input.id, metadata=input.metadata, text=input.text)
    return "Vector data updated successfully"

def delete_vector():
    pass