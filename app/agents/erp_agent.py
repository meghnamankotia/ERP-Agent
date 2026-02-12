#design client 
from ..config.llm_config import llm
from mcp.client.streamable_http import StreamableHTTPTransport
from mcp import ClientSession

#mcp server url
url="placeholder"

#set transport method and create client session
transport= StreamableHTTPTransport(url)
client= ClientSession(transport)

async def run_agent(query:str)->list:
    #initialize client session
    await client.initialize()

    #list available tools on server and bind them to the agent
    tools= await client.list_tools
    tool_list=[
        {
            "type":"function",
            "function": {
                "name":tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            },
        } for tool in tools
    ]
    llm.bind_tools(tool_list)
    
    #invoke llm until query results are found
    messages=[{"role":"user", "content":query}]
    while True:
        response=llm.invoke(messages)

        msg=response[0].content
        if not msg.tool_calls:
            break

        for tool in msg.tool_calls:
            tool_response=await client.call_tool(tool.name, tool.arguments)
            messages.append({
                "role":"tool",
                "tool_call_id":tool.id,
                "content": tool_response.content
            })

    return messages