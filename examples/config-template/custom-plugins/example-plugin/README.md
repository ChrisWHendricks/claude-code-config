# Example Custom Plugin

This is an example custom plugin that demonstrates how to create organization-specific plugins for Claude Code.

## Structure

```
example-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (required)
├── commands/              # Custom slash commands (optional)
│   └── example.md
├── agents/                # Custom agents (optional)
├── skills/                # Custom skills (optional)
├── hooks/                 # Event hooks (optional)
└── README.md             # Documentation
```

## Creating Your Own Custom Plugin

1. **Copy this template** as a starting point
2. **Update plugin.json** with your plugin details:
   - `name`: Unique plugin identifier (lowercase, hyphens)
   - `version`: Semantic version (e.g., "1.0.0")
   - `description`: What your plugin does
   - Set flags for which components your plugin has

3. **Add your components**:
   - **Commands** (`commands/*.md`): Slash commands users can invoke
   - **Agents** (`agents/*.md`): Autonomous subagents for specific tasks
   - **Skills** (`skills/*.md`): Reusable workflows triggered by context
   - **Hooks** (`hooks/*.js` or `hooks/*.md`): Event-driven automation

4. **Test locally** by copying to `~/.claude/plugins/your-plugin-name/`

5. **Distribute** by adding to your config repo's `custom-plugins/` directory

## Learn More

See the Plugin Development documentation for detailed guidance:
- Command structure and YAML frontmatter
- Agent system prompts and triggering
- Skill progressive disclosure
- Hook events and validation

## Example Use Cases

- Company-specific code generators
- Integration with internal tools/APIs
- Custom workflows for your tech stack
- Security and compliance checks
- Project scaffolding templates
