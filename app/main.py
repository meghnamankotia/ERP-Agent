from mcp.server.fastmcp import FastMCP
from services.query_builder import request_query, create_query
from services.metadata_registry import schema_search

mcp=FastMCP("MCP Server-ERP")

mcp.add_tool(
    create_query,
    name="create_query",
    description="A tool to carry out create operations for mongo db.",
    #structured_output=True
)

mcp.add_tool(
    request_query,
    name="request_query",
    description="A tool to carry out read operations for mongo db. These can include sorting, limiting and skipping records.Eg- Get the topper student of class 10.",
    #structured_output=True
)

mcp.add_tool(
    schema_search,
    name="schema_search",
    description="Perform a schema search on the vector db inorder to retrieve information relevant to create a mongo query. For eg- User ids of students who are failing.",
    #structured_output=True
)
print("Starting MCP Server...")
mcp.run(transport="streamable-http")
#after running main.py run python -m app.agents.erp_agent to test the agent