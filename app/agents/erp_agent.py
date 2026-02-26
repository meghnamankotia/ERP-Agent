#design client 
from app.config.llm_config import llm
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
import asyncio
from .prompt_templates import llm_prompt
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
            
            
            messages = [{"role": "system", "content": llm_prompt},
                {
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
                    tool_text = "\n".join(
                        block.text for block in tool_response.content
                        if block.type == "text"
                    )
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tool["id"],
                        "content": [
                            {   
                                "type": "text",
                                "text": tool_text
                            }
                        ]
                    })
            return messages