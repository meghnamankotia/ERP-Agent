#design client 
from app.config.llm_config import llm
from mcp.client.streamable_http import streamable_http_client,StreamableHTTPTransport
from mcp import ClientSession
import asyncio
from app.utils.test_intent import inputHandler

#mcp server url
url="http://127.0.0.1:8000/mcp"

async def run_agent(query:str)->list:
    #initialize client session
    async with streamable_http_client(url) as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream=read_stream, write_stream=write_stream) as client:
            await client.initialize()

            #list available tools on server and bind them to the agent
            tools= await client.list_tools()
            print("this is all tools present ", tools)
            tools=tools.tools
            tool_list=[
                {
                    "type":"function",
                    "function": {
                        "name":tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    },
                } for tool in tools
            ]
            bound_llm=llm.bind_tools(tool_list)
            
            
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": query}
                    ]
                }]
            
            #invoke llm until query results are found
            while True:
                response=bound_llm.invoke(messages)
                messages.append({
                    "role": "assistant",
                    "content": response.content,
                    "tool_calls": response.tool_calls
                })
                if not response.tool_calls:
                    break

                for tool in response.tool_calls:
                    tool_response=await client.call_tool(tool["name"], tool["args"])
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tool["id"],
                        "content": [
                            {   
                                "type": "text",
                                "text": tool_response.content[0].text
                            }
                        ]
                    })
            return messages

# print(asyncio.run(run_agent("Add a student named Alan with roll no 2 in class 10 having bld grp A+. He is 15 years old and lives at 775 road and his parents can be contacted at 9980836133."))[-1]["content"])

print(asyncio.run(run_agent(inputHandler("D:\\codes\\mcp-erp\\test\\test-pic.jpeg")))[-1]["content"])