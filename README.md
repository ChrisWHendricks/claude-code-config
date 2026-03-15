# Claude Setup

**A flexible, organization-agnostic CLI tool for managing Claude Code team configuration.**

Perfect for teams who want to standardize their Claude Code setup across developers while keeping control of their configuration.

[![Tests](https://github.com/chris.hendricks/claude-code-config/actions/workflows/test.yml/badge.svg)](https://github.com/chris.hendricks/claude-code-config/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- ✨ **Beginner-Friendly Wizard** (v3.4.0+) - Intuitive setup with 5 simple options
- 🎨 **Interactive Menu** - Navigate all features with arrow keys
- 🔌 **Pluggable Sources** - GitHub repos, zip files, or local directories
- 📦 **Category-based Installation** - Install only what you need
- 💾 **Smart Settings Merge** - Preserve user customizations
- 🏗️ **Config Bootstrapping** - Generate config repos from existing setups with automatic team/personal settings separation
- 🔄 **Automatic Backups** - Safe, reversible updates
- 🔌 **Plugin Management** - Auto-detect and install required plugins
- 🎯 **Update Detection** - Know when new config is available
- 🎨 **Rich Terminal UI** - Beautiful, informative output
- 🧪 **Automated Testing** (v3.4.0+) - GitHub Actions CI for quality assurance

## 🚀 Quick Start

### For Team Members (Using Existing Config)

Your admin should provide you with either a setup script or source configuration.

**Option 1: Using the Interactive Wizard (Easiest - v3.4.0+)**
```bash
# 1. Install tool
git clone https://github.com/chris.hendricks/claude-code-config.git
cd claude-setup
pip install -e .

# 2. Run the beginner-friendly wizard
claude-setup init
# Or just: claude-setup (then choose "Setup Configuration")

# The wizard will guide you through:
# - Using a zip file with pre-made config
# - Cloning a git repository
# - Creating config from scratch
# - Or advanced custom setup

# 3. Install configuration
claude-setup install --all

# 4. Check plugins
claude-setup plugins
```

**Option 2: Direct command (if you know the source)**
```bash
# 1. Install tool
git clone https://github.com/chris.hendricks/claude-code-config.git
cd claude-setup
pip install -e .

# 2. Initialize with your organization's config
claude-setup init --github your-org/claude-config
# Or: claude-setup init --local /path/to/config
# Or: claude-setup init --zip https://example.com/config.zip

# 3. Install configuration
claude-setup install --all

# 4. Check plugins
claude-setup plugins
```

### For Administrators (Setting Up for Your Team)

See **[ADMIN-GUIDE.md](ADMIN-GUIDE.md)** for complete instructions.

**Quick Start:**
```bash
# Create a config from your existing setup (recommended)
claude-setup create-config --output ~/my-org-config

# Or start from template
cp -r examples/config-template/ my-org-config/
cd my-org-config/
# Customize...
```

## 📖 Usage

### Interactive Menu (Recommended)

Simply run without arguments:
```bash
claude-setup
```

Navigate with arrow keys through:
- ⚙️ **Setup Configuration** (v3.4.0+) - Beginner-friendly wizard
- 📦 Install Configuration
- 📊 Check Installation Status
- 🔌 Manage Plugins
- 💾 View Backups
- ⏮️ Rollback to Backup
- 🔄 Check for Updates
- 🔧 **Advanced/Admin Tools** (v3.4.0+) - Create config repos for sharing

### Command Line

```bash
# Run beginner-friendly wizard (v3.4.0+)
claude-setup init

# Or initialize sources directly
claude-setup init --github your-org/claude-config
claude-setup init --local /path/to/config
claude-setup init --zip https://example.com/config.zip

# Install everything
claude-setup install --all

# Check status
claude-setup status

# Update to latest
claude-setup update

# Manage plugins
claude-setup plugins

# View backups
claude-setup backups

# Rollback if needed
claude-setup rollback

# Create a config repo from your ~/.claude setup
claude-setup create-config
```

## 🏗️ Architecture

### Configuration Sources

Claude Setup doesn't include any organization-specific configuration. Instead, it fetches configuration from sources you specify:

```json
{
  "sources": [
    {
      "name": "company-config",
      "type": "github",
      "repo": "your-org/claude-config",
      "ref": "main"
    }
  ]
}
```

**Supported source types:**
- **GitHub**: Public or private repositories
- **Zip**: HTTP/HTTPS URLs to zip files
- **Local**: Local filesystem paths

### Configuration Structure

Your configuration repository should follow this structure:

```
your-org/claude-config/
├── manifest.json          # Category definitions
├── core/
│   ├── CLAUDE.md          # Main instructions
│   ├── settings.json      # Team settings
│   └── statusline.sh      # Status line script
├── agents/                # Agent definitions
├── rules/                 # Team guidelines
├── commands/              # Custom commands
└── plugins/
    └── required.json      # Required plugins
```

See `examples/config-template/` for a complete template.

## 📚 Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [README-PUBLIC.md](README-PUBLIC.md) | This file - Overview and quick start | Everyone |
| [ADMIN-GUIDE.md](ADMIN-GUIDE.md) | Complete guide for setting up sources | Administrators |
| [USAGE.md](USAGE.md) | Interactive menu guide | End users |
| [UPDATING.md](UPDATING.md) | How to receive and install updates | End users |
| [MAINTAINING.md](MAINTAINING.md) | How to maintain and distribute updates | Administrators |
| [examples/](examples/) | Templates and examples | Administrators |

## 🔧 Configuration Sources

### GitHub Repository (Recommended)

**Best for:** Version control, team collaboration, easy updates

```bash
claude-setup init --github your-org/claude-config
```

**For private repos:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
claude-setup init --github your-org/private-config
```

### Zip File

**Best for:** Simple distribution, no git required

```bash
claude-setup init --zip https://releases.example.com/claude-config.zip
```

### Local Directory

**Best for:** Development, testing, custom configs

```bash
claude-setup init --local ~/my-claude-config
```

### Multiple Sources

For advanced use cases, edit `~/.claude/sources.json`:

```json
{
  "sources": [
    {
      "name": "company-base",
      "type": "github",
      "repo": "your-org/claude-config-base",
      "ref": "main"
    },
    {
      "name": "team-overrides",
      "type": "local",
      "path": "~/team-config"
    }
  ]
}
```

## 🎓 Examples

### Example 1: Using the Template

```bash
# Use the generic template included in the repo
claude-setup init --local examples/config-template
claude-setup install --all
```

### Example 2: Creating Your Own Config

Administrators can bootstrap a config from their working setup:

```bash
# Generate config from your ~/.claude
claude-setup create-config --output ~/my-org-config

# Review and customize
cd my-org-config
# Edit CLAUDE.md, add team rules, etc.

# Push to GitHub
git remote add origin https://github.com/your-org/claude-config.git
git push -u origin main

# Team members install
claude-setup init --github your-org/claude-config
claude-setup install --all
```

See [ADMIN-GUIDE.md](ADMIN-GUIDE.md#creating-config-from-existing-setup) for detailed instructions.

### Example 3: Enterprise Setup with Zip Distribution

```bash
# Admin: Create and host config
cd my-company-config
zip -r claude-config-v1.0.0.zip config/
aws s3 cp claude-config-v1.0.0.zip s3://my-bucket/releases/

# Team members: Use it
claude-setup init --zip https://my-bucket.s3.amazonaws.com/releases/claude-config-v1.0.0.zip
claude-setup install --all
```

## 🔄 Update Workflow

### For End Users

```bash
# Check for updates
claude-setup status

# Install updates
claude-setup update

# Or interactive
claude-setup  # → Select "Check for Updates"
```

### For Administrators

```bash
# Update config
cd your-org/claude-config
vim config/rules/new-rule.md
git add config/
git commit -m "feat: add new rule"
git push

# Notify team
# "New config available! Run: claude-setup update"
```

The tool automatically detects changes and prompts users to update.

## 🛡️ Security

- ✅ No company-specific config in public repo
- ✅ Support for private GitHub repos with tokens
- ✅ HTTPS-only for zip downloads
- ✅ Local filesystem access for air-gapped environments
- ✅ Automatic backups before all changes
- ✅ Settings merge preserves user customizations

## 🤝 Contributing

This is an open-source project! Contributions welcome.

**Areas for contribution:**
- Additional source types (GitLab, Bitbucket, S3, etc.)
- YAML support for sources.json
- Configuration validation
- Additional template examples
- Documentation improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

[MIT License](LICENSE)

## 🙋 Support

**For tool issues:**
- GitHub Issues: https://github.com/chris.hendricks/claude-code-config/issues
- Documentation: README.md, ADMIN-GUIDE.md

**For your organization's config:**
- Contact your administrator
- Check your config repo's README

## 🎉 Success Stories

Organizations using Claude Setup:

- **Tyler Technologies**: Managing Claude Code config for 20+ developers across multiple teams
- **Your Company**: [Submit a PR to add yours!]

## 🚦 Status

- ✅ Production ready
- ✅ 36 passing tests
- ✅ Complete documentation
- ✅ Multi-source support
- ✅ Interactive menu
- ✅ Automatic updates

## 🙏 Credits

This project is forked from [Travis Jorge's](https://github.com/travis-jorge) original work. Special thanks to Travis for creating the foundation and architecture that made this tool possible.

---

**Made with ❤️ for teams using Claude Code**
