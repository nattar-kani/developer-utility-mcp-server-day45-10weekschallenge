
# Day 45 — Model Context Protocol (MCP)

A Developer Utility MCP Server built with Python and the MCP SDK. It exposes five custom tools through the Model Context Protocol and connects to them using an MCP client over standard input/output (stdio).

## Features

- Safe arithmetic calculator
- Word, character, and sentence counter
- Celsius, Fahrenheit, and Kelvin converter
- JSON validator and formatter
- UTC and Unix timestamp generator
- Client-side tool discovery and invocation
- Tool result and error display

## Project Structure

```text
Day 45/
├── server.py
├── client.py
├── requirements.txt
├── README.md
└── tests/
    └── test_tools.py
```

## Architecture

The MCP server registers the five tools. The client launches the server
as a subprocess and communicates with it over stdio using the MCP protocol.

The client does not import the tool functions directly. It discovers
available tools through the protocol and invokes them by name.

## MCP Protocol Flow

1. The client launches the server process using `StdioServerParameters`.
2. `stdio_client` establishes communication over standard input/output.
3. `ClientSession` sends the MCP initialization request.
4. The server responds with its protocol and capability information.
5. The client completes initialization.
6. The client sends a `tools/list` request to discover available tools.
7. The server returns tool names, descriptions, and input schemas.
8. The client sends a `tools/call` request with a tool name and arguments.
9. The server executes the registered function.
10. The server returns the tool result or an error result.
11. The client displays the result and closes the session.


### Protocol Messages

MCP uses JSON-RPC 2.0 messages to exchange requests and responses.

- **Initialization:** The client sends `initialize`. The server responds with its protocol version and capabilities. The client then sends `notifications/initialized`.
- **Tool discovery:** The client sends `tools/list`. The server responds with the available tools, their descriptions, and input schemas.
- **Tool execution:** The client sends `tools/call`, including the tool name and arguments. The server executes the registered function and returns a result.
- **Error handling:** Invalid tool inputs can produce an error result. The client checks the result's `isError` property and displays the returned content.

The Python MCP SDK handles the protocol messages, serialization, and transport. The application code uses methods such as `session.initialize()`, `session.list_tools()`, and `session.call_tool()` instead of constructing JSON-RPC messages manually.

## Tools

| Tool | Purpose |
|---|---|
| `calculate` | Evaluate basic arithmetic |
| `count_words` | Count words, characters, and sentences |
| `convert_temperature` | Convert between C, F, and K |
| `format_json` | Validate and format JSON |
| `get_timestamp` | Return UTC and Unix timestamps |

## Running the Project

```powershell
python client.py
```

The client launches the MCP server automatically, discovers its tools,
and demonstrates tool calls.

## Running Tests

```powershell
python -m pytest tests/test_tools.py -v
```

## Transport

This project uses stdio transport. The client and server communicate through the subprocess's standard input and output. Avoid printing
debug messages directly to stdout in the server because stdout carries
the MCP protocol messages.
