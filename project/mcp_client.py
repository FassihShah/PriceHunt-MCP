import os
from dotenv import load_dotenv
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_core.tools import Tool 


load_dotenv()



class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.memory = []
        self.MAX_HISTORY = 20

    async def connect_to_server(self, server_script_path: str):
        """Connects to the MCP server via stdio."""

        command = "python" if server_script_path.endswith(".py") else "node"

        server_params = StdioServerParameters(command=command, args=[server_script_path])

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        tools = await self.session.list_tools()
        self.tools = tools.tools
        print("Connected to server with tools:", [t.name for t in self.tools])


    async def run_chat(self, query: str):
        """Handles the prompt flow with Gemini and tools."""
        tools_schema = [
                Tool(
                    name=tool.name,
                    description=tool.description,
                    args_schema=tool.inputSchema,
                    func=lambda args, name=tool.name: self.session.call_tool(name, args)
                    )
                for tool in self.tools]


        system_prompt = (
            "You are an intelligent assistant that helps find the minimum priced product "
            "from Pakistani e-commerce sites using the available tools.\n"
            "Your goal is to find the **original product** the user is searching for — not any accessory, fake, or unrelated item.\n"
            "Use the tools to query product listings and return the product with the lowest price that matches the **actual product name** (e.g., if the user asks for 'iPhone 13', don't return cases or chargers).\n"
            "If the tools return irrelevant items, you can ignore them."
        )

        messages = [SystemMessage(content=system_prompt)] + self.memory
        messages.append(HumanMessage(content=query))

        while True:
            response = await self.llm.ainvoke(messages, tools=tools_schema)
            messages.append(response)

            if not hasattr(response, "tool_calls") or not response.tool_calls:
                break

            for tool_call in response.tool_calls:
                print(f"⚙️ Calling tool: {tool_call['name']} with args: {tool_call['args']}")
                result = await self.session.call_tool(tool_call["name"], tool_call["args"])
                print(f"🛠 Tool Response: {result.content}")
                messages.append(
                    ToolMessage(content=result.content, tool_call_id=tool_call["id"])
                )

        self.memory.append(HumanMessage(query))
        self.memory.append(AIMessage(response.content))
        self.memory = self.memory[-self.MAX_HISTORY:]

        print("\nGemini's Final Response:")
        print(response.content)

    async def cleanup(self):
        await self.exit_stack.aclose()
