"""Tests for custom plugin functionality."""

import json
import pytest
from pathlib import Path

from claude_setup.plugins import PluginManager


@pytest.fixture
def mock_custom_plugins_source(tmp_path):
    """Create mock custom plugins source directory."""
    custom_plugins = tmp_path / "custom-plugins"
    custom_plugins.mkdir()

    # Create plugin 1 with valid structure
    plugin1 = custom_plugins / "plugin1"
    plugin1.mkdir()
    plugin_json_dir = plugin1 / ".claude-plugin"
    plugin_json_dir.mkdir()
    plugin_json = plugin_json_dir / "plugin.json"
    plugin_json.write_text(json.dumps({
        "name": "plugin1",
        "version": "1.0.0",
        "description": "Test plugin 1"
    }))

    # Create plugin 2 with valid structure
    plugin2 = custom_plugins / "plugin2"
    plugin2.mkdir()
    plugin_json_dir2 = plugin2 / ".claude-plugin"
    plugin_json_dir2.mkdir()
    plugin_json2 = plugin_json_dir2 / "plugin.json"
    plugin_json2.write_text(json.dumps({
        "name": "plugin2",
        "version": "1.0.0",
        "description": "Test plugin 2"
    }))

    # Create invalid plugin (no plugin.json)
    plugin3 = custom_plugins / "plugin3"
    plugin3.mkdir()

    return custom_plugins


@pytest.fixture
def mock_claude_dir(tmp_path):
    """Create mock ~/.claude directory."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    plugins_dir = claude_dir / "plugins"
    plugins_dir.mkdir()
    return claude_dir


def test_check_custom_plugins_installed_none(mock_claude_dir):
    """Test checking custom plugins when none are configured."""
    plugin_mgr = PluginManager(mock_claude_dir, [], None)
    status = plugin_mgr.check_custom_plugins_installed()
    assert status == {}


def test_check_custom_plugins_installed_none_installed(mock_claude_dir, mock_custom_plugins_source):
    """Test checking custom plugins when none are installed."""
    plugin_mgr = PluginManager(mock_claude_dir, [], mock_custom_plugins_source)
    status = plugin_mgr.check_custom_plugins_installed()

    # All plugins should show as not installed
    assert status["plugin1"] is False
    assert status["plugin2"] is False
    assert "plugin3" in status  # Invalid plugin still detected


def test_check_custom_plugins_installed_all_installed(mock_claude_dir, mock_custom_plugins_source):
    """Test checking custom plugins when all are installed."""
    # Install plugin1
    plugin1_target = mock_claude_dir / "plugins" / "plugin1"
    plugin1_target.mkdir()
    plugin_json_dir = plugin1_target / ".claude-plugin"
    plugin_json_dir.mkdir()
    plugin_json = plugin_json_dir / "plugin.json"
    plugin_json.write_text(json.dumps({"name": "plugin1"}))

    # Install plugin2
    plugin2_target = mock_claude_dir / "plugins" / "plugin2"
    plugin2_target.mkdir()
    plugin_json_dir2 = plugin2_target / ".claude-plugin"
    plugin_json_dir2.mkdir()
    plugin_json2 = plugin_json_dir2 / "plugin.json"
    plugin_json2.write_text(json.dumps({"name": "plugin2"}))

    plugin_mgr = PluginManager(mock_claude_dir, [], mock_custom_plugins_source)
    status = plugin_mgr.check_custom_plugins_installed()

    assert status["plugin1"] is True
    assert status["plugin2"] is True


def test_check_custom_plugins_installed_partial(mock_claude_dir, mock_custom_plugins_source):
    """Test checking custom plugins when some are installed."""
    # Install only plugin1
    plugin1_target = mock_claude_dir / "plugins" / "plugin1"
    plugin1_target.mkdir()
    plugin_json_dir = plugin1_target / ".claude-plugin"
    plugin_json_dir.mkdir()
    plugin_json = plugin_json_dir / "plugin.json"
    plugin_json.write_text(json.dumps({"name": "plugin1"}))

    plugin_mgr = PluginManager(mock_claude_dir, [], mock_custom_plugins_source)
    status = plugin_mgr.check_custom_plugins_installed()

    assert status["plugin1"] is True
    assert status["plugin2"] is False


def test_check_custom_plugins_no_plugin_json(mock_claude_dir, mock_custom_plugins_source):
    """Test checking when plugin directory exists but plugin.json is missing."""
    # Create plugin1 directory but no plugin.json
    plugin1_target = mock_claude_dir / "plugins" / "plugin1"
    plugin1_target.mkdir()

    plugin_mgr = PluginManager(mock_claude_dir, [], mock_custom_plugins_source)
    status = plugin_mgr.check_custom_plugins_installed()

    # Should be False because plugin.json is missing
    assert status["plugin1"] is False


def test_get_missing_custom_plugins(mock_claude_dir, mock_custom_plugins_source):
    """Test getting list of missing custom plugins."""
    # Install only plugin1
    plugin1_target = mock_claude_dir / "plugins" / "plugin1"
    plugin1_target.mkdir()
    plugin_json_dir = plugin1_target / ".claude-plugin"
    plugin_json_dir.mkdir()
    plugin_json = plugin_json_dir / "plugin.json"
    plugin_json.write_text(json.dumps({"name": "plugin1"}))

    plugin_mgr = PluginManager(mock_claude_dir, [], mock_custom_plugins_source)
    missing = plugin_mgr.get_missing_custom_plugins()

    assert "plugin1" not in missing
    assert "plugin2" in missing
    assert "plugin3" in missing


def test_get_all_plugin_status(mock_claude_dir, mock_custom_plugins_source):
    """Test getting unified status of external and custom plugins."""
    # Setup some external plugins
    installed_plugins = {
        "plugins": {
            "external-plugin": {"version": "1.0.0"}
        }
    }
    installed_plugins_file = mock_claude_dir / "plugins" / "installed_plugins.json"
    installed_plugins_file.write_text(json.dumps(installed_plugins))

    required_plugins = [
        {"name": "external-plugin", "description": "External plugin"},
        {"name": "missing-plugin", "description": "Missing plugin"}
    ]

    # Install plugin1 custom plugin
    plugin1_target = mock_claude_dir / "plugins" / "plugin1"
    plugin1_target.mkdir()
    plugin_json_dir = plugin1_target / ".claude-plugin"
    plugin_json_dir.mkdir()
    plugin_json = plugin_json_dir / "plugin.json"
    plugin_json.write_text(json.dumps({"name": "plugin1"}))

    plugin_mgr = PluginManager(mock_claude_dir, required_plugins, mock_custom_plugins_source)
    all_status = plugin_mgr.get_all_plugin_status()

    # Check external plugins
    assert all_status["external"]["external-plugin"] is True
    assert all_status["external"]["missing-plugin"] is False

    # Check custom plugins
    assert all_status["custom"]["plugin1"] is True
    assert all_status["custom"]["plugin2"] is False


def test_empty_custom_plugins_source(mock_claude_dir, tmp_path):
    """Test handling empty custom plugins source directory."""
    empty_source = tmp_path / "empty-custom-plugins"
    empty_source.mkdir()

    plugin_mgr = PluginManager(mock_claude_dir, [], empty_source)
    status = plugin_mgr.check_custom_plugins_installed()

    assert status == {}
