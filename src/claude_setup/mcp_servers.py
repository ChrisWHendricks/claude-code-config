"""MCP server management functionality."""

import json
import subprocess
from pathlib import Path
from typing import Optional


class MCPServerManager:
    """Manages MCP servers (external and custom)."""

    def __init__(self, claude_dir: Path, required_servers: list[dict]):
        """Initialize MCP server manager.

        Args:
            claude_dir: Path to ~/.claude directory
            required_servers: List of required server definitions
        """
        self.claude_dir = claude_dir
        self.required_servers = required_servers
        self.settings_path = claude_dir / "settings.json"

    def check_configured(self) -> dict[str, bool]:
        """Check which servers are in settings.json mcpServers field.

        Returns:
            Dictionary mapping server name to configuration status
        """
        if not self.settings_path.exists():
            return {server["name"]: False for server in self.required_servers}

        try:
            with open(self.settings_path) as f:
                settings = json.load(f)

            mcp_servers = settings.get("mcpServers", {})
            status = {}

            for server in self.required_servers:
                server_name = server["name"]
                status[server_name] = server_name in mcp_servers

            return status
        except (json.JSONDecodeError, KeyError):
            return {server["name"]: False for server in self.required_servers}

    def check_server_executable(self, server: dict) -> tuple[bool, str]:
        """Check if server executable/package is available.

        Checks based on install method:
        - npm: Run 'npx --yes {package} --version'
        - pip: Run 'python -c "import {module}"'
        - docker: Run 'docker images -q {image}'
        - custom: Check file existence

        Args:
            server: Server definition dict

        Returns:
            Tuple of (available, message)
        """
        install_method = server.get("install_method", "custom")

        try:
            if install_method == "npm":
                package = server.get("package", "")
                if not package:
                    return False, "No package specified"

                # Try to run the package with --help or --version
                result = subprocess.run(
                    ["npx", "--yes", package, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    return True, "Available"
                else:
                    return False, f"Package not working: {result.stderr[:100]}"

            elif install_method == "pip":
                module = server.get("module", server.get("package", ""))
                if not module:
                    return False, "No module specified"

                # Try to import the module
                result = subprocess.run(
                    ["python3", "-c", f"import {module}"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    return True, "Available"
                else:
                    return False, f"Module not found"

            elif install_method == "docker":
                image = server.get("image", "")
                if not image:
                    return False, "No image specified"

                # Check if image exists locally
                result = subprocess.run(
                    ["docker", "images", "-q", image],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return True, "Available"
                else:
                    return False, "Image not found locally"

            elif install_method == "custom":
                # For custom servers, check if files exist in mcp-servers directory
                config = server.get("config", {})
                args = config.get("args", [])

                # Look for file paths in args
                for arg in args:
                    if isinstance(arg, str) and ("/.claude/mcp-servers/" in arg or "{{HOME}}" in arg):
                        # Extract the relative path
                        if "mcp-servers/" in arg:
                            rel_path = arg.split("mcp-servers/", 1)[1]
                            file_path = self.claude_dir / "mcp-servers" / rel_path
                            if file_path.exists():
                                return True, "Files exist"
                            else:
                                return False, f"File not found: {rel_path}"

                # Default to unknown for custom servers
                return False, "Cannot verify (custom server)"

            else:
                return False, f"Unknown install method: {install_method}"

        except subprocess.TimeoutExpired:
            return False, "Check timed out"
        except FileNotFoundError as e:
            return False, f"Command not found: {str(e).split()[0]}"
        except Exception as e:
            return False, f"Check failed: {e}"

    def get_missing_servers(self) -> list[dict]:
        """Get servers not configured in settings.json.

        Returns:
            List of server definitions
        """
        status = self.check_configured()
        missing = []

        for server in self.required_servers:
            if not status[server["name"]]:
                missing.append(server)

        return missing

    def get_install_instructions(self, server: dict) -> list[str]:
        """Generate installation instructions for a server.

        Args:
            server: Server definition dict

        Returns:
            List of instruction strings
        """
        install_method = server.get("install_method", "custom")
        instructions = []

        if install_method == "npm":
            package = server.get("package", "")
            instructions.append(f"Install via npm:")
            instructions.append(f"  npm install -g {package}")
            instructions.append(f"Or it will be installed automatically via npx")

        elif install_method == "pip":
            package = server.get("package", "")
            instructions.append(f"Install via pip:")
            instructions.append(f"  pip install {package}")

        elif install_method == "docker":
            image = server.get("image", "")
            instructions.append(f"Pull Docker image:")
            instructions.append(f"  docker pull {image}")

        elif install_method == "custom":
            instructions.append(f"Custom MCP server - install via:")
            instructions.append(f"  claude-setup install --category mcp-servers-custom")

        # Add environment variable setup if needed
        env_vars = server.get("env_vars_required", [])
        if env_vars:
            instructions.append("")
            instructions.append("Required environment variables:")
            for var in env_vars:
                instructions.append(f"  export {var}=<your-value>")

        # Add configuration note
        instructions.append("")
        instructions.append("Then run installation to configure:")
        instructions.append("  claude-setup install --all")

        return instructions

    def check_custom_servers_installed(self, custom_source: Optional[Path]) -> dict[str, bool]:
        """Check custom MCP servers by file presence.

        Args:
            custom_source: Path to mcp-servers/custom/ in config

        Returns:
            Dict mapping server name to installation status
        """
        if not custom_source or not custom_source.exists():
            return {}

        status = {}
        mcp_servers_dir = self.claude_dir / "mcp-servers"

        for server_dir in custom_source.iterdir():
            if not server_dir.is_dir():
                continue

            server_name = server_dir.name
            target_dir = mcp_servers_dir / server_name

            # Check if directory exists with files
            status[server_name] = target_dir.exists() and any(target_dir.iterdir())

        return status
