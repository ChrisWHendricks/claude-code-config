"""Tests for MCP server merge functionality."""

import pytest
from pathlib import Path

from claude_setup.merge import merge_settings, _merge_mcp_servers


def test_merge_mcp_servers_empty():
    """Test merging when both source and target have no MCP servers."""
    source = {}
    target = {}
    result = _merge_mcp_servers(source, target)
    assert result == {}


def test_merge_mcp_servers_source_only():
    """Test merging when only source has MCP servers."""
    source = {
        "playwright": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-playwright"],
            "env": {}
        }
    }
    target = {}
    result = _merge_mcp_servers(source, target)

    assert "playwright" in result
    assert result["playwright"]["command"] == "npx"


def test_merge_mcp_servers_target_only():
    """Test merging when only target has MCP servers."""
    source = {}
    target = {
        "my-server": {
            "command": "python",
            "args": ["server.py"],
            "env": {}
        }
    }
    result = _merge_mcp_servers(source, target)

    assert "my-server" in result
    assert result["my-server"]["command"] == "python"


def test_merge_mcp_servers_union():
    """Test merging creates union of team and user servers."""
    source = {
        "playwright": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-playwright"],
            "env": {}
        }
    }
    target = {
        "my-server": {
            "command": "python",
            "args": ["server.py"],
            "env": {}
        }
    }
    result = _merge_mcp_servers(source, target)

    assert "playwright" in result
    assert "my-server" in result


def test_merge_mcp_servers_team_overwrites():
    """Test team servers overwrite user servers with same name."""
    source = {
        "playwright": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-playwright"],
            "env": {}
        }
    }
    target = {
        "playwright": {
            "command": "node",
            "args": ["old-config"],
            "env": {}
        }
    }
    result = _merge_mcp_servers(source, target)

    assert result["playwright"]["command"] == "npx"
    assert result["playwright"]["args"] == ["-y", "@modelcontextprotocol/server-playwright"]


def test_merge_settings_with_mcp_servers():
    """Test full settings merge includes MCP servers."""
    source = {
        "model": "sonnet",
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-playwright"],
                "env": {}
            }
        }
    }
    target = {
        "model": "opus",
        "feedbackSurveyState": "dismissed",
        "mcpServers": {
            "my-server": {
                "command": "python",
                "args": ["server.py"],
                "env": {}
            }
        }
    }
    result = merge_settings(source, target)

    # Model should be overwritten (team standard)
    assert result["model"] == "sonnet"

    # feedbackSurveyState should be preserved (user-specific)
    assert result["feedbackSurveyState"] == "dismissed"

    # MCP servers should be union (both present)
    assert "playwright" in result["mcpServers"]
    assert "my-server" in result["mcpServers"]


def test_merge_settings_mcp_servers_only_source():
    """Test merge when only source has MCP servers."""
    source = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-playwright"],
                "env": {}
            }
        }
    }
    target = {}
    result = merge_settings(source, target)

    assert "mcpServers" in result
    assert "playwright" in result["mcpServers"]


def test_merge_settings_mcp_servers_only_target():
    """Test merge when only target has MCP servers."""
    source = {}
    target = {
        "mcpServers": {
            "my-server": {
                "command": "python",
                "args": ["server.py"],
                "env": {}
            }
        }
    }
    result = merge_settings(source, target)

    assert "mcpServers" in result
    assert "my-server" in result["mcpServers"]
