# Example Custom MCP Server

This is an example custom MCP server that demonstrates how to create organization-specific MCP servers for Claude Code.

## What is an MCP Server?

MCP (Model Context Protocol) servers provide Claude with access to external tools and services. Custom MCP servers allow you to:

- Integrate with internal APIs and databases
- Provide company-specific tools and data
- Create custom workflows and automations
- Connect to proprietary systems

## Structure

```
example-server/
├── server.py           # Main server implementation
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## How It Works

1. **Server Implementation** (`server.py`):
   - Reads JSON-RPC requests from stdin
   - Handles `tools/list` to advertise available tools
   - Handles `tools/call` to execute tool requests
   - Returns results as JSON

2. **Configuration** (in `core/settings.json`):
   ```json
   {
     "mcpServers": {
       "example-server": {
         "command": "python",
         "args": ["{{HOME}}/.claude/mcp-servers/example-server/server.py"],
         "env": {}
       }
     }
   }
   ```

3. **Installation**:
   - Files copied to `~/.claude/mcp-servers/example-server/`
   - Configuration merged into `settings.json`
   - Claude can now use the server's tools

## Creating Your Own MCP Server

### Python Server

1. **Copy this template** as a starting point
2. **Implement your tools** in `handle_request()`
3. **Add dependencies** to `requirements.txt`
4. **Configure in settings.json**:
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["{{HOME}}/.claude/mcp-servers/my-server/server.py"],
         "env": {
           "API_KEY": "{{API_KEY}}"
         }
       }
     }
   }
   ```

### Node.js Server

For Node.js servers:
```json
{
  "mcpServers": {
    "my-node-server": {
      "command": "node",
      "args": ["{{HOME}}/.claude/mcp-servers/my-node-server/index.js"],
      "env": {}
    }
  }
}
```

### Other Languages

Any language that can:
- Read JSON from stdin
- Write JSON to stdout
- Implement the MCP protocol

## Example Use Cases

- **Internal API Access**: Query company databases or services
- **Custom Code Generators**: Generate boilerplate for your stack
- **Security Scanning**: Check code against company policies
- **Data Transformations**: Convert between internal formats
- **Infrastructure Tools**: Deploy, monitor, or manage systems

## MCP Protocol Basics

Your server should handle these methods:

1. **tools/list**: Return available tools
   ```json
   {
     "tools": [
       {
         "name": "tool_name",
         "description": "What it does",
         "inputSchema": { /* JSON Schema */ }
       }
     ]
   }
   ```

2. **tools/call**: Execute a tool
   ```json
   {
     "content": [
       {
         "type": "text",
         "text": "Tool result"
       }
     ]
   }
   ```

## Testing

1. Install dependencies: `pip install -r requirements.txt`
2. Test locally: `echo '{"method":"tools/list","params":{}}' | python server.py`
3. Add to config and run: `claude-setup install --category mcp-servers-custom`
4. Use in Claude Code

## Resources

- MCP Protocol Specification: https://modelcontextprotocol.io
- Example MCP Servers: https://github.com/modelcontextprotocol/servers
- Claude Code MCP Integration: See plugin-dev:mcp-integration skill
