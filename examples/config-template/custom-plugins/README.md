# Custom Plugins

This directory contains organization-specific Claude Code plugins that are distributed through your team configuration.

## What are Custom Plugins?

Custom plugins are full Claude Code plugins (with `.claude-plugin/plugin.json`, commands, hooks, skills, agents) that your organization creates and maintains. They get installed to `~/.claude/plugins/` alongside marketplace plugins.

## Directory Structure

```
custom-plugins/
├── example-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json       # Required: Plugin manifest
│   ├── commands/              # Optional: Slash commands
│   ├── agents/                # Optional: Subagents
│   ├── skills/                # Optional: Skills
│   ├── hooks/                 # Optional: Event hooks
│   └── README.md
└── your-plugin/
    └── ...
```

## Creating a Custom Plugin

### 1. Create Plugin Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands
mkdir -p my-plugin/agents
mkdir -p my-plugin/skills
mkdir -p my-plugin/hooks
```

### 2. Create Plugin Manifest

**File**: `my-plugin/.claude-plugin/plugin.json`

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Description of your plugin",
  "author": "Your Organization",
  "commands": true,
  "agents": false,
  "skills": false,
  "hooks": false
}
```

Set flags to `true` for component types your plugin includes.

### 3. Add Components

**Commands** (`commands/*.md`):
```markdown
---
description: "Command description"
---

# Command Instructions

Your command implementation here.
```

**Agents** (`agents/*.md`):
```markdown
---
description: "Agent description"
color: "blue"
---

# Agent System Prompt

Your agent instructions here.
```

**Skills** (`skills/*.md`):
```markdown
---
description: "Skill description"
trigger: "when user mentions X"
---

# Skill Content

Your skill implementation here.
```

**Hooks** (`hooks/*.md` or `hooks/*.js`):
```markdown
---
event: "PreToolUse"
---

# Hook Logic

Your hook implementation here.
```

### 4. Test Locally

Copy to your plugins directory:
```bash
cp -r my-plugin ~/.claude/plugins/
```

Launch Claude Code and test your plugin.

### 5. Distribute

Add to your config repository's `custom-plugins/` directory:
```bash
cp -r my-plugin /path/to/config/custom-plugins/
git add custom-plugins/my-plugin
git commit -m "Add my-plugin"
```

## Installation

Team members install custom plugins via:

```bash
claude-setup install --category custom-plugins
```

This copies all plugins from `config/custom-plugins/` to `~/.claude/plugins/`.

## Plugin Status

Check custom plugin status:

```bash
claude-setup plugins
```

Shows both external (npm) and custom (team) plugins.

## Example Use Cases

### Company-Specific Commands

Create slash commands for your organization:
- `/deploy` - Deploy to your infrastructure
- `/scaffold` - Generate boilerplate for your stack
- `/security-check` - Run company security scans
- `/docs` - Search internal documentation

### Internal Tool Integration

Connect to company services:
- CRM or customer data systems
- Internal APIs and databases
- CI/CD pipelines
- Monitoring and alerting

### Workflow Automation

Automate common tasks:
- Code review checklists
- Testing workflows
- Release procedures
- Onboarding tasks

### Code Standards

Enforce company standards:
- Architecture patterns
- Security requirements
- Performance guidelines
- Documentation templates

## Best Practices

### Plugin Design

- **Single Responsibility**: Each plugin should focus on one area
- **Clear Naming**: Use descriptive names (e.g., `acme-deploy`, `acme-security`)
- **Version Control**: Increment version in plugin.json for changes
- **Documentation**: Include comprehensive README.md

### Component Guidelines

**Commands**:
- Use YAML frontmatter for metadata
- Include usage examples
- Document required arguments
- Provide clear error messages

**Agents**:
- Specify tools the agent needs
- Define clear triggering conditions
- Set appropriate colors for UI
- Include examples in description

**Skills**:
- Define specific trigger conditions
- Use progressive disclosure (overview → details)
- Include actionable content
- Test trigger phrases

**Hooks**:
- Validate inputs carefully
- Provide helpful error messages
- Document event types handled
- Test thoroughly before distributing

### Security

- **Never commit secrets**: Use environment variables
- **Validate inputs**: Prevent command injection
- **Limit permissions**: Request minimum required tools
- **Review dependencies**: Audit any external packages

### Maintenance

- **Track issues**: Use GitHub Issues or similar
- **Version updates**: Communicate changes to team
- **Test thoroughly**: Before distributing updates
- **Gather feedback**: From team members using plugins

## Plugin Components Reference

### Commands (commands/*.md)

Slash commands users can invoke:

```markdown
---
description: "Brief description"
args:
  - name: "arg_name"
    description: "Argument description"
    required: true
---

# Command Implementation

Instructions for Claude when executing this command.
```

### Agents (agents/*.md)

Autonomous subagents for specific tasks:

```markdown
---
description: "Agent description (when to use)"
color: "blue|green|red|yellow|purple|orange|gray"
tools:
  - Read
  - Write
  - Bash
---

# System Prompt

Agent instructions and context.
```

### Skills (skills/*.md)

Reusable workflows triggered by context:

```markdown
---
description: "Skill description (triggering conditions)"
trigger: "when user asks to X"
---

# Overview

Brief summary of what this skill does.

## Details

Detailed implementation steps.
```

### Hooks (hooks/*.md or hooks/*.js)

Event-driven automation:

```markdown
---
event: "PreToolUse|PostToolUse|Stop|SessionStart|..."
tool: "Bash|Read|Write|..."  # Optional: filter by tool
---

# Hook Logic

Validation, transformation, or notification logic.
```

## Development Resources

### Claude Code Plugin Skills

Use these skills for plugin development help:
- `/plugin-dev:plugin-structure` - Overall plugin architecture
- `/plugin-dev:command-development` - Creating commands
- `/plugin-dev:agent-development` - Creating agents
- `/plugin-dev:skill-development` - Creating skills
- `/plugin-dev:hook-development` - Creating hooks
- `/plugin-dev:mcp-integration` - Integrating MCP servers
- `/plugin-dev:create-plugin` - Guided plugin creation

### Example Plugin

See `example-plugin/` for a complete working example with:
- Proper plugin.json structure
- Example command implementation
- Comprehensive README

### Plugin Discovery

When Claude Code starts, it scans `~/.claude/plugins/` and loads all plugins with valid `.claude-plugin/plugin.json` files.

## Troubleshooting

### Plugin not recognized

1. Check plugin.json exists: `ls ~/.claude/plugins/my-plugin/.claude-plugin/plugin.json`
2. Validate JSON syntax
3. Restart Claude Code
4. Check Claude Code logs

### Component not loading

1. Verify file naming: `commands/my-command.md` (lowercase, hyphens)
2. Check YAML frontmatter syntax
3. Ensure file is in correct directory
4. Review component flags in plugin.json

### Updates not applying

1. Remove old version: `rm -rf ~/.claude/plugins/my-plugin`
2. Reinstall: `claude-setup install --category custom-plugins`
3. Restart Claude Code

## Contributing

When contributing plugins to your team config:

1. **Test thoroughly** on multiple projects
2. **Document clearly** in plugin README
3. **Request feedback** from team members
4. **Submit PR** with description of changes
5. **Update version** in plugin.json

## Learn More

- Plugin Development Guide: Use `/plugin-dev:create-plugin` skill
- Claude Code Documentation: https://claude.ai/docs
- Example Plugins: Browse `example-plugin/` directory
