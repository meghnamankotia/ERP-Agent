from mcp.server.fastmcp import FastMCP
from services.query_builder import build_query
from services.metadata_registry import schema_search

mcp=FastMCP("MCP Server-ERP")

mcp.add_tool(build_query)
mcp.add_tool(schema_search)