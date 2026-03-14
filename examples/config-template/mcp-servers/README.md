# MCP Servers Configuration

This directory configures Model Context Protocol (MCP) servers for your team's Claude Code setup.

## Structure

```
mcp-servers/
├── required.json       # External MCP servers (npm/pip/docker)
├── custom/             # Custom MCP server implementations
│   └── example-server/
└── README.md
```

## External MCP Servers

**File**: `required.json`

Configure external MCP servers from npm, pip, or Docker registries.

### Example Configuration

```json
[
  {
    "name": "playwright",
    "description": "Browser automation MCP server",
    "install_method": "npm",
    "package": "@modelcontextprotocol/server-playwright",
    "config": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "env": {}
    }
  },
  {
    "name": "database",
    "description": "Database query server",
    "install_method": "npm",
    "package": "@modelcontextprotocol/server-postgres",
    "config": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "{{DATABASE_URL}}"
      }
    },
    "env_vars_required": ["DATABASE_URL"]
  }
]
```

### Schema Fields

- **name**: Server identifier (used as key in settings.json)
- **description**: Human-readable description
- **install_method**: One of "npm", "pip", "docker", or "custom"
- **package** or **image**: Package name (npm/pip) or Docker image
- **config**: Object merged into settings.json mcpServers
  - **command**: Executable (npx, python, docker, etc.)
  - **args**: Command arguments
  - **env**: Environment variables (supports {{VARIABLE}} templates)
- **env_vars_required**: List of required environment variables (optional)

### Installation Methods

**npm** (Node.js packages):
```json
{
  "install_method": "npm",
  "package": "@org/server-name",
  "config": {
    "command": "npx",
    "args": ["-y", "@org/server-name"]
  }
}
```

**pip** (Python packages):
```json
{
  "install_method": "pip",
  "package": "mcp-server-name",
  "config": {
    "command": "python",
    "args": ["-m", "mcp_server_name"]
  }
}
```

**docker**:
```json
{
  "install_method": "docker",
  "image": "org/mcp-server:latest",
  "config": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "org/mcp-server:latest"]
  }
}
```

## Custom MCP Servers

**Directory**: `custom/`

Create organization-specific MCP servers for internal tools and services.

### Structure

Each custom server is a directory with implementation files:

```
custom/
└── my-server/
    ├── server.py or index.js    # Server implementation
    ├── requirements.txt or package.json
    └── README.md
```

### Configuration

Custom servers are referenced in `core/settings.json`:

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

The `{{HOME}}` template is resolved to the user's home directory during installation.

### Installation

Custom servers are installed via the `mcp-servers-custom` category:

```bash
claude-setup install --category mcp-servers-custom
```

This copies all files from `config/mcp-servers/custom/` to `~/.claude/mcp-servers/`.

## Workflow

### For End Users

1. **Check status**: `claude-setup mcp-servers`
2. **Install external servers**: Follow instructions (npm install, pip install, etc.)
3. **Configure in Claude**: `claude-setup install --all`
4. **Verify**: Launch Claude Code and check MCP server availability

### For Admins

1. **Add external servers**: Edit `required.json`
2. **Create custom servers**: Add directories to `custom/`
3. **Configure settings**: Add mcpServers entries to `core/settings.json`
4. **Test**: Install locally and verify functionality
5. **Distribute**: Push to config repository

## Status Checking

The `claude-setup mcp-servers` command shows:

- **Configuration**: Whether server is in settings.json
- **Executable**: Whether the underlying package/command is available
- **Installation instructions**: For missing or unavailable servers

## Environment Variables

MCP servers often need environment variables for API keys, database URLs, etc.

### In required.json

```json
{
  "config": {
    "env": {
      "API_KEY": "{{API_KEY}}",
      "DATABASE_URL": "{{DATABASE_URL}}"
    }
  },
  "env_vars_required": ["API_KEY", "DATABASE_URL"]
}
```

### User Setup

Users set environment variables in their shell profile:

```bash
export API_KEY="your-key-here"
export DATABASE_URL="postgres://..."
```

Or in a `.env` file loaded by Claude Code.

## Examples

### Official MCP Servers

Browse available servers at https://github.com/modelcontextprotocol/servers

Popular options:
- `@modelcontextprotocol/server-playwright` - Browser automation
- `@modelcontextprotocol/server-filesystem` - File operations
- `@modelcontextprotocol/server-github` - GitHub integration
- `@modelcontextprotocol/server-postgres` - PostgreSQL queries

### Custom Use Cases

- Internal API clients (company data, services)
- Custom code generators (scaffolding, boilerplate)
- Security and compliance checks
- Infrastructure automation (deploy, monitor)
- Data transformations (format conversions)

## Troubleshooting

### Server not available

```bash
# For npm servers
npm install -g @modelcontextprotocol/server-name

# For pip servers
pip install mcp-server-name

# For docker servers
docker pull org/server-name
```

### Custom server not working

1. Check files copied: `ls ~/.claude/mcp-servers/my-server/`
2. Test server directly: `python ~/.claude/mcp-servers/my-server/server.py`
3. Check settings.json: `cat ~/.claude/settings.json | grep mcpServers -A 10`
4. Review Claude Code logs for errors

### Environment variables not set

Ensure variables are exported in your shell:
```bash
echo $API_KEY  # Should print your key
```

## Learn More

- MCP Protocol: https://modelcontextprotocol.io
- Plugin MCP Integration: Use `/plugin-dev:mcp-integration` skill
- Example implementations: See `custom/example-server/`
