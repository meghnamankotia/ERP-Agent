from mcp.server.fastmcp import FastMCP
from services.query_builder import find_query, create_query, update_query, delete_query
from services.metadata_registry import schema_search, create_vector, delete_vector

mcp=FastMCP("MCP Server-ERP")

#MONGO TOOLS

mcp.add_tool(
    create_query,
    name="create_query",
    description="A tool to carry out create operations for mongo db.",
    #structured_output=True
)

mcp.add_tool(
    find_query,
    name="find_query",
    description="A tool to carry out read operations for mongo db. These can include sorting, limiting and skipping records.Eg- Get the topper student of class 10.",
    #structured_output=True
)

mcp.add_tool(
    update_query,
    name="update_query",
    description="A tool to carry out update operations for mongo db.",
    #structured_output=True
)

mcp.add_tool(
    delete_query,
    name="delete_query",
    description="A tool to carry out delete operations for mongo db. The input consists of the table/collection name and the filters based on which the records are to be deleted."
)
#PINECONE VECTOR MEMORY TOOLS

mcp.add_tool(
    create_vector,
    name="create_vector",
    description="A tool to create vector data in the vector db after the data has been added to the main mongo db database. Hence this tool is only to be called after the successful execution of the create_query tool. The input consists of the index name to which the data is to be added and the corresponding data. The data dictionary includes the text that is to be embedded and the metadata fields that are to be set separately in the vector db record. ",
    #structured_output=True
)

mcp.add_tool(
    schema_search,
    name="schema_search",
    description="Perform a schema search on the vector db inorder to retrieve information relevant to create a mongo query. For eg- User ids of students who are failing.",
    #structured_output=True
)

mcp.add_tool(
    delete_vector,
    name="delete_vector",
    description="A tool to delete vectors from the vector db only after the successful deletion from the mongo db. The input consists of a list ids whose records are to be deleted as well as the name of the table/index from which they are to be deleted(string format)."
)

@mcp.resource("file://documents/{name}")
async def get_schema(name: str)-> str:
    pass

print("Starting MCP Server...")
mcp.run(transport="streamable-http")