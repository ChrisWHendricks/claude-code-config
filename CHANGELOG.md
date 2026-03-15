# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2026-03-14

### Added
- **Custom Plugins Support**: New `custom-plugins` category with discover install type for managing team custom plugins
- **MCP Servers Support**: New `mcp-servers` category with JSON merge support for Model Context Protocol server configurations
- **Smart MCP Server Merging**: Intelligent merging of `mcpServers` in settings.json that preserves user's personal servers while adding team servers
- **MCP Server Management Module**: New `mcp_servers.py` module for managing MCP server configurations
- **Interactive Plugin Management**: Enhanced CLI with interactive menu options for managing both plugins and MCP servers
- **Comprehensive Test Coverage**: Added `test_custom_plugins.py` and `test_mcp_merge.py` with full test coverage for new functionality
- **Example Templates**: Added example plugin and MCP server configurations in `examples/config-template/`
- **Documentation**: Added `IMPLEMENTATION_SUMMARY.md` documenting new features and architecture

### Changed
- Updated manifest.json schema to support new categories
- Enhanced settings.json template with MCP servers support
- Improved plugin management with better detection and reporting

## [3.4.0] - 2025-XX-XX

### Added
- Beginner-friendly init wizard with 5 intuitive options
- Consistent git clone behavior for all repository types
- Admin functions separated into dedicated submenu
- Automated CI/CD with GitHub Actions

### Changed
- All git repositories cloned via wizard stored as `type: "local"` sources
- Updates use standard `git pull` on tracked local directories
- GitHub detection is informational only

## [3.3.0] - 2025-XX-XX

### Added
- Initial plugin management support
- Backup and rollback functionality
- Interactive menu system

## [3.2.0] - 2025-XX-XX

### Added
- Source-based architecture
- Support for GitHub, Zip, and Local sources
- Smart settings merge

## [3.1.0] - 2025-XX-XX

### Added
- Category-based installation
- Template variable resolution
- Version tracking

## [3.0.0] - 2025-XX-XX

### Added
- Initial release with core functionality
- Basic configuration management
- Installation and update capabilities

[4.0.0]: https://github.com/chris.hendricks/claude-code-config/compare/v3.4.0...v4.0.0
[3.4.0]: https://github.com/chris.hendricks/claude-code-config/compare/v3.3.0...v3.4.0
[3.3.0]: https://github.com/chris.hendricks/claude-code-config/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/chris.hendricks/claude-code-config/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/chris.hendricks/claude-code-config/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/chris.hendricks/claude-code-config/releases/tag/v3.0.0
