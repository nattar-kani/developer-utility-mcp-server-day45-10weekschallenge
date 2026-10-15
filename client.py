import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_path = Path(__file__).parent / "server.py"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)]
    )

    async with stdio_client(server_params) as (read_stream,write_stream):
        async with ClientSession(read_stream,write_stream) as session:

            await session.initialize()
            print("Connected to MCP server")

            tools_result = await session.list_tools()

            print("Available MCP tools:")
            for tool in tools_result.tools:
                print(f"-> {tool.name}: {tool.description}")

            print("Calling calculate")
            result = await session.call_tool(
                "calculate",
                {"expression": "5*17+9"}
            )
            print("calculate",result)

            """print("Calling calculate")
            result = await session.call_tool(
                "calculate",
                {"expression": "2 ** 3"}
            )
            print("calculate", result) 
            FOR TESTING TOOL FAILURE ONLY"""

            print("Calling convert temperature")
            result = await session.call_tool(
                "convert_temperature",
                {
                    "value": 100,
                    "from_unit": "C",
                    "to_unit": "F",
                }
            )
            print("convert_temperature", result)

            print("Calling count_words...")
            result = await session.call_tool(
                "count_words",
                {"text": "MCP connects clients with useful tools."},
            )
            print("count_words", result)

            print("Calling format_json...")
            result = await session.call_tool(
                "format_json",
                {
                    "json_text": '{"name":"Maya","role":"AI Engineer"}'
                },
            )
            print("format_json", result.content)

            print("Calling get_timestamp...")
            result = await session.call_tool(
                "get_timestamp",
                {},
            )
            print("get_timestamp", result)


def print_tool_result(name, result):

    print(f"{name}")

    if result.isError:
        print("Tool execution failed:")
    else:
        print("Result:")

    for item in result.content:
        if hasattr(item, "text"):
            print(item.text)
        else:
            print(item)



if __name__ == "__main__":
    asyncio.run(main())
